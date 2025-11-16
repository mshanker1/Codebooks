"""
Presenter Agent - responsible for formatting and presenting results.
"""
from typing import Optional
from datetime import datetime

from .base_agent import BaseAgent
from .models import ExtractedData, AnalysisResult, PresentationResult


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
