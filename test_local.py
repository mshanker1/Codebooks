#!/usr/bin/env python3
"""
Test script for the web scraper agents using a local HTML file.
"""

from web_scraper_agents.scraper_agent import WebScraperAgent
from web_scraper_agents.analyzer_agent import AnalyzerAgent
from web_scraper_agents.presenter_agent import PresenterAgent
from web_scraper_agents.models import WebPage, ExtractedData
from bs4 import BeautifulSoup
from datetime import datetime


def load_local_html(file_path):
    """Load HTML from a local file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def main():
    print("=" * 80)
    print("WEB SCRAPER AGENTS - LOCAL FILE TEST")
    print("=" * 80)
    print()

    # Load local HTML file
    print("Loading local HTML file...")
    html_content = load_local_html('test_page.html')

    # Create a mock WebPage object
    web_page = WebPage(
        url='file://test_page.html',
        content=html_content,
        status_code=200
    )

    # Initialize the scraper agent
    scraper = WebScraperAgent()

    # Extract data using the scraper's extraction method
    print("Extracting data...")
    extracted_data = scraper._extract_data(web_page)

    # Initialize and run the analyzer
    print("Analyzing content...")
    analyzer = AnalyzerAgent()
    analysis = analyzer.execute(extracted_data)

    # Initialize and run the presenter (text format)
    print("Formatting results (text)...")
    presenter_text = PresenterAgent({'output_format': 'text'})
    result_text = presenter_text.execute(extracted_data, analysis)

    # Print the text report
    print("\n" + "=" * 80)
    print(result_text.formatted_text)
    print("=" * 80)

    # Save text report
    with open('test_report.txt', 'w', encoding='utf-8') as f:
        f.write(result_text.formatted_text)
    print("\nText report saved to: test_report.txt")

    # Generate markdown report
    print("\nGenerating markdown report...")
    presenter_md = PresenterAgent({'output_format': 'markdown'})
    result_md = presenter_md.execute(extracted_data, analysis)

    with open('test_report.md', 'w', encoding='utf-8') as f:
        f.write(result_md.formatted_text)
    print("Markdown report saved to: test_report.md")

    # Generate HTML report
    print("\nGenerating HTML report...")
    presenter_html = PresenterAgent({'output_format': 'html'})
    result_html = presenter_html.execute(extracted_data, analysis)

    with open('test_report.html', 'w', encoding='utf-8') as f:
        f.write(result_html.formatted_text)
    print("HTML report saved to: test_report.html")

    print("\n" + "=" * 80)
    print("TEST COMPLETE - All three formats generated successfully!")
    print("=" * 80)


if __name__ == '__main__':
    main()
