#!/usr/bin/env python3
"""
Web Scraper Agent System - Main Entry Point

This script provides a command-line interface for the agent-based web scraping system.
"""

import argparse
import sys
from web_scraper_agents import AgentOrchestrator


def main():
    """Main entry point for the web scraper agent system."""

    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Agent-based Web Scraping and Analysis System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Scrape and analyze a website
  python main.py https://www.example.com

  # Save results to a file
  python main.py https://www.example.com -o output.txt

  # Use markdown format
  python main.py https://www.example.com --format markdown -o report.md

  # Use HTML format
  python main.py https://www.example.com --format html -o report.html
        '''
    )

    parser.add_argument(
        'url',
        help='The URL to scrape and analyze'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file path (optional)',
        default=None
    )

    parser.add_argument(
        '--format',
        choices=['text', 'markdown', 'html'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='HTTP request timeout in seconds (default: 30)'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress agent logging output'
    )

    parser.add_argument(
        '--requirement',
        help='Specific requirement or keyword to search for across pages',
        default=None
    )

    parser.add_argument(
        '--crawl',
        action='store_true',
        help='Enable crawling to search across sub-pages'
    )

    parser.add_argument(
        '--max-depth',
        type=int,
        default=2,
        help='Maximum crawl depth for sub-pages (default: 2)'
    )

    parser.add_argument(
        '--max-pages',
        type=int,
        default=50,
        help='Maximum number of pages to crawl (default: 50)'
    )

    # Parse arguments
    args = parser.parse_args()

    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        print("Error: URL must start with http:// or https://")
        sys.exit(1)

    # Configure the orchestrator
    config = {
        'scraper': {
            'timeout': args.timeout,
            'max_depth': args.max_depth,
            'max_pages': args.max_pages
        },
        'analyzer': {
            'max_summary_sentences': 5,
            'min_topic_frequency': 3
        },
        'presenter': {
            'output_format': args.format
        }
    }

    # Suppress logging if quiet mode
    if args.quiet:
        import logging
        logging.getLogger().setLevel(logging.ERROR)

    try:
        # Create orchestrator
        orchestrator = AgentOrchestrator(config)

        # Execute the pipeline
        result = orchestrator.execute(
            args.url,
            requirement=args.requirement,
            crawl=args.crawl,
            save_to_file=args.output
        )

        # Print results to console
        print("\n")
        print(result.formatted_text)
        print("\n")

        if args.output:
            print(f"Results saved to: {args.output}")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
