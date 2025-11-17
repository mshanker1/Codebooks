"""
Agent Orchestrator - coordinates the workflow between all agents.
"""
from typing import Dict, Any, Optional

from .base_agent import BaseAgent
from .scraper_agent import WebScraperAgent
from .analyzer_agent import AnalyzerAgent
from .presenter_agent import PresenterAgent
from .models import ExtractedData, AnalysisResult, PresentationResult, PageResult, MultiPageResult


class AgentOrchestrator(BaseAgent):
    """
    Orchestrates the workflow between scraper, analyzer, and presenter agents.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the orchestrator.

        Args:
            config: Configuration dictionary for all agents
        """
        super().__init__("AgentOrchestrator", config)

        # Initialize sub-agents
        scraper_config = self.config.get('scraper', {})
        analyzer_config = self.config.get('analyzer', {})
        presenter_config = self.config.get('presenter', {})

        self.scraper_agent = WebScraperAgent(scraper_config)
        self.analyzer_agent = AnalyzerAgent(analyzer_config)
        self.presenter_agent = PresenterAgent(presenter_config)

        self.log_info("Agent Orchestrator initialized with all sub-agents")

    def execute(self, url: str, requirement: Optional[str] = None,
                crawl: bool = False, save_to_file: Optional[str] = None) -> PresentationResult:
        """
        Execute the full web scraping and analysis pipeline.

        Args:
            url: The URL to scrape and analyze
            requirement: Optional keyword/phrase to search for
            crawl: Whether to crawl multiple pages
            save_to_file: Optional file path to save the results

        Returns:
            PresentationResult object
        """
        self.log_info(f"Starting orchestrated workflow for: {url}")
        if requirement:
            self.log_info(f"Searching for requirement: '{requirement}'")
        if crawl:
            self.log_info(f"Crawl mode enabled (max depth: {self.scraper_agent.max_depth}, max pages: {self.scraper_agent.max_pages})")
        self.log_info("=" * 80)

        try:
            if crawl:
                # Multi-page crawl mode
                self.log_info("[STEP 1/3] Initiating web crawling...")
                extracted_pages = self.scraper_agent.execute_crawl(url, requirement)

                if not extracted_pages:
                    self.log_error("No pages found matching the criteria")
                    return self._create_error_result(url, "No matching pages found")

                self.log_info(f"Found {len(extracted_pages)} matching pages")

                # Step 2: Analyze all matching pages
                self.log_info("[STEP 2/3] Analyzing extracted pages...")
                page_results = []
                for i, page_data in enumerate(extracted_pages, 1):
                    self.log_info(f"Analyzing page {i}/{len(extracted_pages)}: {page_data.url}")
                    analysis = self.analyzer_agent.execute(page_data, requirement)
                    page_results.append(PageResult(extracted_data=page_data, analysis=analysis))

                # Sort by relevance if requirement specified
                if requirement:
                    page_results.sort(key=lambda x: x.analysis.relevance_score, reverse=True)
                    self.log_info("Sorted results by relevance score")

                # Create multi-page result
                multi_result = MultiPageResult(
                    base_url=url,
                    requirement=requirement,
                    total_pages_crawled=len(self.scraper_agent.visited_urls),
                    matching_pages=page_results
                )

                # Step 3: Format and present the results
                self.log_info("[STEP 3/3] Formatting multi-page presentation...")
                presentation_result = self.presenter_agent.execute_multi(multi_result)

            else:
                # Single page mode (original behavior)
                # Step 1: Scrape the web page
                self.log_info("[STEP 1/3] Initiating web scraping...")
                extracted_data = self.scraper_agent.execute(url)

                if not extracted_data.title:
                    self.log_error("Failed to extract meaningful data from the page")
                    return self._create_error_result(url, "Failed to extract data")

                # Step 2: Analyze the extracted data
                self.log_info("[STEP 2/3] Analyzing extracted data...")
                analysis_result = self.analyzer_agent.execute(extracted_data, requirement)

                # Step 3: Format and present the results
                self.log_info("[STEP 3/3] Formatting presentation...")
                presentation_result = self.presenter_agent.execute(extracted_data, analysis_result)

            # Save to file if requested
            if save_to_file:
                self._save_to_file(presentation_result, save_to_file)

            self.log_info("=" * 80)
            self.log_info("Workflow completed successfully!")

            return presentation_result

        except Exception as e:
            self.log_error(f"Error in orchestration: {str(e)}")
            return self._create_error_result(url, str(e))

    def _save_to_file(self, result: PresentationResult, file_path: str):
        """
        Save the presentation result to a file.

        Args:
            result: PresentationResult object
            file_path: Path to save the file
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(result.formatted_text)
            self.log_info(f"Results saved to: {file_path}")
        except Exception as e:
            self.log_error(f"Failed to save to file: {str(e)}")

    def _create_error_result(self, url: str, error_message: str) -> PresentationResult:
        """
        Create an error presentation result.

        Args:
            url: The URL that was being processed
            error_message: The error message

        Returns:
            PresentationResult with error information
        """
        error_text = f"""
ERROR REPORT
{'=' * 80}
URL: {url}
Error: {error_message}
{'=' * 80}
        """
        return PresentationResult(url=url, formatted_text=error_text.strip())

    def get_agent_status(self) -> Dict[str, str]:
        """
        Get the status of all sub-agents.

        Returns:
            Dictionary with agent names and their status
        """
        return {
            'orchestrator': 'active',
            'scraper': 'active',
            'analyzer': 'active',
            'presenter': 'active'
        }
