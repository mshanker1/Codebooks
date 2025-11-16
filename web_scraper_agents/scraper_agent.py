"""
Web Scraper Agent - responsible for fetching and extracting web content.
"""
from typing import Optional
import requests
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
