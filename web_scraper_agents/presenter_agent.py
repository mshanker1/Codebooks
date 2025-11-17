"""
Presenter Agent - responsible for formatting and presenting results.
"""
from typing import Optional
from datetime import datetime

from .base_agent import BaseAgent
from .models import ExtractedData, AnalysisResult, PresentationResult, MultiPageResult


class PresenterAgent(BaseAgent):
    """Agent responsible for formatting and presenting analysis results."""

    def __init__(self, config: dict = None):
        """Initialize the presenter agent."""
        super().__init__("PresenterAgent", config)
        self.output_format = self.config.get('output_format', 'text')  # text, markdown, html

    def execute(self, extracted_data: ExtractedData, analysis: AnalysisResult) -> PresentationResult:
        """
        Format and present the analysis results.

        Args:
            extracted_data: ExtractedData object
            analysis: AnalysisResult object

        Returns:
            PresentationResult object
        """
        self.log_info(f"Formatting results for: {analysis.url}")

        if self.output_format == 'markdown':
            formatted_text = self._format_as_markdown(extracted_data, analysis)
        elif self.output_format == 'html':
            formatted_text = self._format_as_html(extracted_data, analysis)
        else:
            formatted_text = self._format_as_text(extracted_data, analysis)

        self.log_info("Presentation formatting complete")

        return PresentationResult(
            url=analysis.url,
            formatted_text=formatted_text
        )

    def execute_multi(self, multi_result: MultiPageResult) -> PresentationResult:
        """
        Format and present results from multiple pages.

        Args:
            multi_result: MultiPageResult object containing all page results

        Returns:
            PresentationResult object
        """
        self.log_info(f"Formatting multi-page results ({len(multi_result.matching_pages)} pages)")

        if self.output_format == 'markdown':
            formatted_text = self._format_multi_as_markdown(multi_result)
        elif self.output_format == 'html':
            formatted_text = self._format_multi_as_html(multi_result)
        else:
            formatted_text = self._format_multi_as_text(multi_result)

        self.log_info("Multi-page presentation formatting complete")

        return PresentationResult(
            url=multi_result.base_url,
            formatted_text=formatted_text
        )

    def _format_as_text(self, data: ExtractedData, analysis: AnalysisResult) -> str:
        """
        Format results as plain text.

        Args:
            data: ExtractedData object
            analysis: AnalysisResult object

        Returns:
            Formatted text string
        """
        lines = []
        lines.append("=" * 80)
        lines.append("WEB SCRAPER AGENT - ANALYSIS REPORT")
        lines.append("=" * 80)
        lines.append("")

        # Basic Information
        lines.append("BASIC INFORMATION")
        lines.append("-" * 80)
        lines.append(f"URL:           {analysis.url}")
        lines.append(f"Title:         {data.title}")
        lines.append(f"Content Type:  {analysis.content_type}")
        lines.append(f"Word Count:    {analysis.word_count}")
        lines.append(f"Importance:    {analysis.importance_score:.2f}/1.00")
        lines.append(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Summary
        lines.append("SUMMARY")
        lines.append("-" * 80)
        lines.append(analysis.summary)
        lines.append("")

        # Key Points
        if analysis.key_points:
            lines.append("KEY POINTS")
            lines.append("-" * 80)
            for point in analysis.key_points:
                lines.append(f"  {point}")
            lines.append("")

        # Topics
        if analysis.topics:
            lines.append("IDENTIFIED TOPICS")
            lines.append("-" * 80)
            lines.append(f"  {', '.join(analysis.topics)}")
            lines.append("")

        # Page Structure
        lines.append("PAGE STRUCTURE")
        lines.append("-" * 80)
        lines.append(f"  Headings:   {len(data.headings)}")
        lines.append(f"  Paragraphs: {len(data.paragraphs)}")
        lines.append(f"  Links:      {len(data.links)}")
        lines.append(f"  Images:     {len(data.images)}")
        lines.append("")

        # Sample Links (top 5)
        if data.links:
            lines.append("SAMPLE LINKS (Top 5)")
            lines.append("-" * 80)
            for i, link in enumerate(data.links[:5], 1):
                text = link['text'][:50] if link['text'] else 'No text'
                lines.append(f"  {i}. {text}")
                lines.append(f"     URL: {link['url']}")
            lines.append("")

        # Metadata
        if data.metadata:
            lines.append("METADATA")
            lines.append("-" * 80)
            for key, value in list(data.metadata.items())[:10]:
                # Truncate long values
                value_str = str(value)[:100]
                if len(str(value)) > 100:
                    value_str += "..."
                lines.append(f"  {key}: {value_str}")
            lines.append("")

        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)

        return "\n".join(lines)

    def _format_as_markdown(self, data: ExtractedData, analysis: AnalysisResult) -> str:
        """
        Format results as Markdown.

        Args:
            data: ExtractedData object
            analysis: AnalysisResult object

        Returns:
            Formatted markdown string
        """
        lines = []
        lines.append("# Web Scraper Agent - Analysis Report")
        lines.append("")

        # Basic Information
        lines.append("## Basic Information")
        lines.append("")
        lines.append(f"- **URL:** {analysis.url}")
        lines.append(f"- **Title:** {data.title}")
        lines.append(f"- **Content Type:** {analysis.content_type}")
        lines.append(f"- **Word Count:** {analysis.word_count}")
        lines.append(f"- **Importance Score:** {analysis.importance_score:.2f}/1.00")
        lines.append(f"- **Analysis Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(analysis.summary)
        lines.append("")

        # Key Points
        if analysis.key_points:
            lines.append("## Key Points")
            lines.append("")
            for point in analysis.key_points:
                lines.append(f"- {point}")
            lines.append("")

        # Topics
        if analysis.topics:
            lines.append("## Identified Topics")
            lines.append("")
            lines.append(f"`{' | '.join(analysis.topics)}`")
            lines.append("")

        # Page Structure
        lines.append("## Page Structure")
        lines.append("")
        lines.append(f"- **Headings:** {len(data.headings)}")
        lines.append(f"- **Paragraphs:** {len(data.paragraphs)}")
        lines.append(f"- **Links:** {len(data.links)}")
        lines.append(f"- **Images:** {len(data.images)}")
        lines.append("")

        # Sample Links
        if data.links:
            lines.append("## Sample Links (Top 5)")
            lines.append("")
            for i, link in enumerate(data.links[:5], 1):
                text = link['text'][:50] if link['text'] else 'No text'
                lines.append(f"{i}. [{text}]({link['url']})")
            lines.append("")

        # Metadata
        if data.metadata:
            lines.append("## Metadata")
            lines.append("")
            for key, value in list(data.metadata.items())[:10]:
                value_str = str(value)[:100]
                if len(str(value)) > 100:
                    value_str += "..."
                lines.append(f"- **{key}:** {value_str}")
            lines.append("")

        lines.append("---")
        lines.append("*End of Report*")

        return "\n".join(lines)

    def _format_as_html(self, data: ExtractedData, analysis: AnalysisResult) -> str:
        """
        Format results as HTML.

        Args:
            data: ExtractedData object
            analysis: AnalysisResult object

        Returns:
            Formatted HTML string
        """
        html = []
        html.append("<!DOCTYPE html>")
        html.append("<html>")
        html.append("<head>")
        html.append("    <meta charset='UTF-8'>")
        html.append("    <title>Web Scraper Analysis Report</title>")
        html.append("    <style>")
        html.append("        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }")
        html.append("        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; }")
        html.append("        h2 { color: #34495e; margin-top: 30px; border-bottom: 1px solid #bdc3c7; }")
        html.append("        .info-grid { display: grid; grid-template-columns: 200px 1fr; gap: 10px; }")
        html.append("        .info-label { font-weight: bold; color: #7f8c8d; }")
        html.append("        .topic-tag { display: inline-block; background: #3498db; color: white; ")
        html.append("                     padding: 5px 10px; margin: 5px; border-radius: 3px; }")
        html.append("        ul { list-style-type: none; padding-left: 0; }")
        html.append("        li { margin: 10px 0; padding-left: 20px; position: relative; }")
        html.append("        li:before { content: '▸'; position: absolute; left: 0; color: #3498db; }")
        html.append("    </style>")
        html.append("</head>")
        html.append("<body>")
        html.append("    <h1>Web Scraper Agent - Analysis Report</h1>")

        # Basic Information
        html.append("    <h2>Basic Information</h2>")
        html.append("    <div class='info-grid'>")
        html.append(f"        <div class='info-label'>URL:</div><div>{analysis.url}</div>")
        html.append(f"        <div class='info-label'>Title:</div><div>{data.title}</div>")
        html.append(f"        <div class='info-label'>Content Type:</div><div>{analysis.content_type}</div>")
        html.append(f"        <div class='info-label'>Word Count:</div><div>{analysis.word_count}</div>")
        html.append(f"        <div class='info-label'>Importance:</div><div>{analysis.importance_score:.2f}/1.00</div>")
        html.append(f"        <div class='info-label'>Analysis Time:</div>")
        html.append(f"        <div>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>")
        html.append("    </div>")

        # Summary
        html.append("    <h2>Summary</h2>")
        html.append(f"    <p>{analysis.summary.replace(chr(10), '<br>')}</p>")

        # Key Points
        if analysis.key_points:
            html.append("    <h2>Key Points</h2>")
            html.append("    <ul>")
            for point in analysis.key_points:
                html.append(f"        <li>{point}</li>")
            html.append("    </ul>")

        # Topics
        if analysis.topics:
            html.append("    <h2>Identified Topics</h2>")
            html.append("    <div>")
            for topic in analysis.topics:
                html.append(f"        <span class='topic-tag'>{topic}</span>")
            html.append("    </div>")

        html.append("</body>")
        html.append("</html>")

        return "\n".join(html)

    def _format_multi_as_text(self, multi_result: MultiPageResult) -> str:
        """
        Format multi-page results as plain text.

        Args:
            multi_result: MultiPageResult object

        Returns:
            Formatted text string
        """
        lines = []
        lines.append("=" * 80)
        lines.append("WEB SCRAPER AGENT - MULTI-PAGE CRAWL REPORT")
        lines.append("=" * 80)
        lines.append("")

        # Overview
        lines.append("CRAWL OVERVIEW")
        lines.append("-" * 80)
        lines.append(f"Base URL:          {multi_result.base_url}")
        if multi_result.requirement:
            lines.append(f"Search Term:       '{multi_result.requirement}'")
        lines.append(f"Pages Crawled:     {multi_result.total_pages_crawled}")
        lines.append(f"Matching Pages:    {len(multi_result.matching_pages)}")
        lines.append(f"Crawl Time:        {multi_result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Results summary
        lines.append("MATCHING PAGES (Sorted by Relevance)")
        lines.append("=" * 80)
        lines.append("")

        for i, page_result in enumerate(multi_result.matching_pages, 1):
            data = page_result.extracted_data
            analysis = page_result.analysis

            lines.append(f"[{i}] {data.title or 'No Title'}")
            lines.append("-" * 80)
            lines.append(f"URL:            {data.url}")
            lines.append(f"Content Type:   {analysis.content_type}")
            lines.append(f"Word Count:     {analysis.word_count}")
            if multi_result.requirement:
                lines.append(f"Relevance:      {analysis.relevance_score:.2f}/1.00")
            lines.append(f"Importance:     {analysis.importance_score:.2f}/1.00")
            lines.append("")

            # Key points for this page
            if analysis.key_points:
                lines.append("Key Points:")
                for point in analysis.key_points[:5]:
                    lines.append(f"  • {point}")
                lines.append("")

            # Topics
            if analysis.topics:
                lines.append(f"Topics: {', '.join(analysis.topics[:5])}")
                lines.append("")

            lines.append("")

        lines.append("=" * 80)
        lines.append("END OF MULTI-PAGE REPORT")
        lines.append("=" * 80)

        return "\n".join(lines)

    def _format_multi_as_markdown(self, multi_result: MultiPageResult) -> str:
        """
        Format multi-page results as Markdown.

        Args:
            multi_result: MultiPageResult object

        Returns:
            Formatted markdown string
        """
        lines = []
        lines.append("# Web Scraper Agent - Multi-Page Crawl Report")
        lines.append("")

        # Overview
        lines.append("## Crawl Overview")
        lines.append("")
        lines.append(f"- **Base URL:** {multi_result.base_url}")
        if multi_result.requirement:
            lines.append(f"- **Search Term:** `{multi_result.requirement}`")
        lines.append(f"- **Pages Crawled:** {multi_result.total_pages_crawled}")
        lines.append(f"- **Matching Pages:** {len(multi_result.matching_pages)}")
        lines.append(f"- **Crawl Time:** {multi_result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Table of contents
        lines.append("## Matching Pages (Sorted by Relevance)")
        lines.append("")

        for i, page_result in enumerate(multi_result.matching_pages, 1):
            data = page_result.extracted_data
            analysis = page_result.analysis

            lines.append(f"### {i}. {data.title or 'No Title'}")
            lines.append("")
            lines.append(f"- **URL:** [{data.url}]({data.url})")
            lines.append(f"- **Content Type:** {analysis.content_type}")
            lines.append(f"- **Word Count:** {analysis.word_count}")
            if multi_result.requirement:
                lines.append(f"- **Relevance Score:** {analysis.relevance_score:.2f}/1.00")
            lines.append(f"- **Importance Score:** {analysis.importance_score:.2f}/1.00")
            lines.append("")

            # Key points
            if analysis.key_points:
                lines.append("**Key Points:**")
                lines.append("")
                for point in analysis.key_points[:5]:
                    lines.append(f"- {point}")
                lines.append("")

            # Topics
            if analysis.topics:
                lines.append(f"**Topics:** `{' | '.join(analysis.topics[:5])}`")
                lines.append("")

            lines.append("---")
            lines.append("")

        lines.append("*End of Multi-Page Report*")

        return "\n".join(lines)

    def _format_multi_as_html(self, multi_result: MultiPageResult) -> str:
        """
        Format multi-page results as HTML.

        Args:
            multi_result: MultiPageResult object

        Returns:
            Formatted HTML string
        """
        html = []
        html.append("<!DOCTYPE html>")
        html.append("<html>")
        html.append("<head>")
        html.append("    <meta charset='UTF-8'>")
        html.append("    <title>Web Scraper Multi-Page Crawl Report</title>")
        html.append("    <style>")
        html.append("        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }")
        html.append("        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; }")
        html.append("        h2 { color: #34495e; margin-top: 30px; border-bottom: 1px solid #bdc3c7; }")
        html.append("        .overview { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }")
        html.append("        .page-result { border: 1px solid #bdc3c7; padding: 20px; margin: 20px 0; ")
        html.append("                       border-radius: 5px; background: #fff; }")
        html.append("        .page-result h3 { color: #2980b9; margin-top: 0; }")
        html.append("        .info-grid { display: grid; grid-template-columns: 150px 1fr; gap: 10px; margin: 15px 0; }")
        html.append("        .info-label { font-weight: bold; color: #7f8c8d; }")
        html.append("        .topic-tag { display: inline-block; background: #3498db; color: white; ")
        html.append("                     padding: 3px 8px; margin: 3px; border-radius: 3px; font-size: 0.9em; }")
        html.append("        .relevance-high { color: #27ae60; font-weight: bold; }")
        html.append("        .relevance-medium { color: #f39c12; font-weight: bold; }")
        html.append("        .relevance-low { color: #95a5a6; font-weight: bold; }")
        html.append("        ul { margin: 10px 0; padding-left: 20px; }")
        html.append("        li { margin: 5px 0; }")
        html.append("    </style>")
        html.append("</head>")
        html.append("<body>")
        html.append("    <h1>Web Scraper Agent - Multi-Page Crawl Report</h1>")

        # Overview
        html.append("    <div class='overview'>")
        html.append("        <h2>Crawl Overview</h2>")
        html.append("        <div class='info-grid'>")
        html.append(f"            <div class='info-label'>Base URL:</div><div>{multi_result.base_url}</div>")
        if multi_result.requirement:
            html.append(f"            <div class='info-label'>Search Term:</div><div><code>{multi_result.requirement}</code></div>")
        html.append(f"            <div class='info-label'>Pages Crawled:</div><div>{multi_result.total_pages_crawled}</div>")
        html.append(f"            <div class='info-label'>Matching Pages:</div><div>{len(multi_result.matching_pages)}</div>")
        html.append(f"            <div class='info-label'>Crawl Time:</div>")
        html.append(f"            <div>{multi_result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</div>")
        html.append("        </div>")
        html.append("    </div>")

        # Results
        html.append("    <h2>Matching Pages (Sorted by Relevance)</h2>")

        for i, page_result in enumerate(multi_result.matching_pages, 1):
            data = page_result.extracted_data
            analysis = page_result.analysis

            # Determine relevance class
            relevance_class = "relevance-low"
            if multi_result.requirement:
                if analysis.relevance_score >= 0.7:
                    relevance_class = "relevance-high"
                elif analysis.relevance_score >= 0.4:
                    relevance_class = "relevance-medium"

            html.append("    <div class='page-result'>")
            html.append(f"        <h3>{i}. {data.title or 'No Title'}</h3>")
            html.append("        <div class='info-grid'>")
            html.append(f"            <div class='info-label'>URL:</div>")
            html.append(f"            <div><a href='{data.url}' target='_blank'>{data.url}</a></div>")
            html.append(f"            <div class='info-label'>Content Type:</div><div>{analysis.content_type}</div>")
            html.append(f"            <div class='info-label'>Word Count:</div><div>{analysis.word_count}</div>")
            if multi_result.requirement:
                html.append(f"            <div class='info-label'>Relevance:</div>")
                html.append(f"            <div class='{relevance_class}'>{analysis.relevance_score:.2f}/1.00</div>")
            html.append(f"            <div class='info-label'>Importance:</div><div>{analysis.importance_score:.2f}/1.00</div>")
            html.append("        </div>")

            # Key points
            if analysis.key_points:
                html.append("        <h4>Key Points</h4>")
                html.append("        <ul>")
                for point in analysis.key_points[:5]:
                    html.append(f"            <li>{point}</li>")
                html.append("        </ul>")

            # Topics
            if analysis.topics:
                html.append("        <h4>Topics</h4>")
                html.append("        <div>")
                for topic in analysis.topics[:5]:
                    html.append(f"            <span class='topic-tag'>{topic}</span>")
                html.append("        </div>")

            html.append("    </div>")

        html.append("</body>")
        html.append("</html>")

        return "\n".join(html)
