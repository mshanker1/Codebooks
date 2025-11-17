"""
Web Scraper Agent - responsible for fetching and extracting web content.
"""
from typing import Optional
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from .base_agent import BaseAgent
from .models import WebPage, ExtractedData


class WebScraperAgent(BaseAgent):
    """Agent responsible for fetching and parsing web pages."""

    def __init__(self, config: dict = None):
        """Initialize the web scraper agent."""
        super().__init__("WebScraperAgent", config)
        self.timeout = self.config.get('timeout', 30)
        self.user_agent = self.config.get(
            'user_agent',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.max_depth = self.config.get('max_depth', 2)
        self.max_pages = self.config.get('max_pages', 50)
        self.visited_urls = set()
        self.base_domain = None

    def execute(self, url: str) -> ExtractedData:
        """
        Fetch and extract data from a web page.

        Args:
            url: The URL to scrape

        Returns:
            ExtractedData object containing structured data
        """
        self.log_info(f"Starting to scrape: {url}")

        # Fetch the page
        web_page = self._fetch_page(url)

        if web_page.error:
            self.log_error(f"Failed to fetch page: {web_page.error}")
            return ExtractedData(url=url, title="Error fetching page")

        # Extract data from the page
        extracted_data = self._extract_data(web_page)

        self.log_info(f"Successfully extracted data from: {url}")
        return extracted_data

    def _fetch_page(self, url: str) -> WebPage:
        """
        Fetch a web page.

        Args:
            url: The URL to fetch

        Returns:
            WebPage object
        """
        web_page = WebPage(url=url)

        try:
            headers = {'User-Agent': self.user_agent}
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()

            web_page.content = response.text
            web_page.headers = dict(response.headers)
            web_page.status_code = response.status_code

        except requests.exceptions.RequestException as e:
            web_page.error = str(e)
            self.log_error(f"Error fetching {url}: {e}")

        return web_page

    def _extract_data(self, web_page: WebPage) -> ExtractedData:
        """
        Extract structured data from HTML content.

        Args:
            web_page: WebPage object containing HTML

        Returns:
            ExtractedData object
        """
        soup = BeautifulSoup(web_page.content, 'html.parser')

        # Extract title
        title = ""
        if soup.title:
            title = soup.title.string.strip() if soup.title.string else ""

        # Extract headings
        headings = []
        for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            for heading in soup.find_all(tag):
                text = heading.get_text(strip=True)
                if text:
                    headings.append(f"{tag.upper()}: {text}")

        # Extract paragraphs
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if text and len(text) > 20:  # Filter out very short paragraphs
                paragraphs.append(text)

        # Extract links
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text(strip=True)
            # Convert relative URLs to absolute
            absolute_url = urljoin(web_page.url, href)
            links.append({'url': absolute_url, 'text': text})

        # Extract images
        images = []
        for img in soup.find_all('img'):
            src = img.get('src', '')
            alt = img.get('alt', '')
            if src:
                absolute_url = urljoin(web_page.url, src)
                images.append({'url': absolute_url, 'alt': alt})

        # Extract metadata
        metadata = {}
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property', '')
            content = meta.get('content', '')
            if name and content:
                metadata[name] = content

        # Extract main content (attempt to get the most relevant text)
        main_content = self._extract_main_content(soup)

        return ExtractedData(
            url=web_page.url,
            title=title,
            headings=headings,
            paragraphs=paragraphs,
            links=links[:50],  # Limit to first 50 links
            images=images[:20],  # Limit to first 20 images
            metadata=metadata,
            main_content=main_content
        )

    def execute_crawl(self, start_url: str, requirement: Optional[str] = None) -> list:
        """
        Crawl website starting from start_url and optionally filter by requirement.

        Args:
            start_url: The URL to start crawling from
            requirement: Optional keyword/phrase to filter pages

        Returns:
            List of ExtractedData objects
        """
        self.log_info(f"Starting crawl from: {start_url}")
        self.base_domain = urlparse(start_url).netloc
        self.visited_urls = set()
        results = []

        def crawl_recursive(url: str, depth: int):
            """Recursively crawl pages."""
            # Check stopping conditions
            if depth > self.max_depth:
                self.log_info(f"Max depth reached at: {url}")
                return
            if len(self.visited_urls) >= self.max_pages:
                self.log_info(f"Max pages limit reached")
                return
            if url in self.visited_urls:
                return

            # Only crawl same domain
            parsed_url = urlparse(url)
            if parsed_url.netloc != self.base_domain:
                return

            # Normalize URL (remove fragments)
            normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
            if parsed_url.query:
                normalized_url += f"?{parsed_url.query}"

            if normalized_url in self.visited_urls:
                return

            self.visited_urls.add(normalized_url)
            self.log_info(f"Crawling [{len(self.visited_urls)}/{self.max_pages}]: {normalized_url}")

            # Extract data from current page
            try:
                # Add a small delay to be respectful to the server
                time.sleep(0.5)

                extracted_data = self.execute(normalized_url)

                # If requirement specified, check if page matches
                if requirement:
                    if self._matches_requirement(extracted_data, requirement):
                        self.log_info(f"✓ Match found: {normalized_url}")
                        results.append(extracted_data)
                    else:
                        self.log_info(f"✗ No match: {normalized_url}")
                else:
                    results.append(extracted_data)

                # Extract and crawl sub-pages
                for link in extracted_data.links:
                    link_url = link['url']
                    crawl_recursive(link_url, depth + 1)

            except Exception as e:
                self.log_error(f"Error crawling {normalized_url}: {str(e)}")

        # Start recursive crawl
        crawl_recursive(start_url, 0)
        self.log_info(f"Crawl complete. Visited {len(self.visited_urls)} pages, found {len(results)} matching pages")
        return results

    def _matches_requirement(self, data: ExtractedData, requirement: str) -> bool:
        """
        Check if extracted data matches the requirement.

        Args:
            data: ExtractedData object
            requirement: Keyword/phrase to search for

        Returns:
            True if requirement is found in the content
        """
        requirement_lower = requirement.lower()

        # Search in title
        if data.title and requirement_lower in data.title.lower():
            return True

        # Search in headings
        for heading in data.headings:
            if requirement_lower in heading.lower():
                return True

        # Search in paragraphs
        for para in data.paragraphs:
            if requirement_lower in para.lower():
                return True

        # Search in main content
        if data.main_content and requirement_lower in data.main_content.lower():
            return True

        return False

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """
        Extract the main content from the page.

        Args:
            soup: BeautifulSoup object

        Returns:
            Main content as string
        """
        # Try to find main content in common containers
        main_tags = soup.find_all(['main', 'article'])
        if main_tags:
            return ' '.join([tag.get_text(strip=True, separator=' ') for tag in main_tags])

        # Fallback: get all text from body
        body = soup.find('body')
        if body:
            # Remove script and style elements
            for script in body(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()
            return body.get_text(strip=True, separator=' ')

        return ""
