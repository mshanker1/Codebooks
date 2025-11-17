"""
Analyzer Agent - responsible for analyzing and summarizing web content.
"""
from typing import List, Dict
import re
from collections import Counter

from .base_agent import BaseAgent
from .models import ExtractedData, AnalysisResult


class AnalyzerAgent(BaseAgent):
    """Agent responsible for analyzing and summarizing extracted web data."""

    def __init__(self, config: dict = None):
        """Initialize the analyzer agent."""
        super().__init__("AnalyzerAgent", config)
        self.max_summary_sentences = self.config.get('max_summary_sentences', 5)
        self.min_topic_frequency = self.config.get('min_topic_frequency', 3)

    def execute(self, extracted_data: ExtractedData, requirement: str = None) -> AnalysisResult:
        """
        Analyze and summarize the extracted data.

        Args:
            extracted_data: ExtractedData object from the scraper
            requirement: Optional keyword/phrase for relevance scoring

        Returns:
            AnalysisResult object
        """
        self.log_info(f"Starting analysis of: {extracted_data.url}")

        # Generate summary
        summary = self._generate_summary(extracted_data, requirement)

        # Extract key points
        key_points = self._extract_key_points(extracted_data, requirement)

        # Identify topics
        topics = self._identify_topics(extracted_data)

        # Count words
        word_count = self._count_words(extracted_data)

        # Determine content type
        content_type = self._determine_content_type(extracted_data)

        # Calculate importance score
        importance_score = self._calculate_importance_score(extracted_data)

        # Calculate relevance score if requirement specified
        relevance_score = 0.0
        if requirement:
            relevance_score = self._calculate_relevance(extracted_data, requirement)
            self.log_info(f"Relevance score for '{requirement}': {relevance_score:.2f}")

        self.log_info(f"Analysis complete for: {extracted_data.url}")

        return AnalysisResult(
            url=extracted_data.url,
            summary=summary,
            key_points=key_points,
            topics=topics,
            word_count=word_count,
            content_type=content_type,
            importance_score=importance_score,
            relevance_score=relevance_score
        )

    def _generate_summary(self, data: ExtractedData, requirement: str = None) -> str:
        """
        Generate a summary of the content.

        Args:
            data: ExtractedData object
            requirement: Optional keyword/phrase to highlight

        Returns:
            Summary string
        """
        # Start with title and metadata description
        summary_parts = []

        if data.title:
            summary_parts.append(f"Page Title: {data.title}")

        # Check for meta description
        description = data.metadata.get('description', '') or data.metadata.get('og:description', '')
        if description:
            summary_parts.append(f"Description: {description}")

        # Extract first few meaningful paragraphs
        if data.paragraphs:
            meaningful_paragraphs = [p for p in data.paragraphs if len(p.split()) > 10][:3]
            if meaningful_paragraphs:
                summary_parts.append("Content Preview:")
                for para in meaningful_paragraphs:
                    # Truncate long paragraphs
                    if len(para) > 200:
                        para = para[:200] + "..."
                    summary_parts.append(f"- {para}")

        return "\n".join(summary_parts) if summary_parts else "No summary available."

    def _extract_key_points(self, data: ExtractedData, requirement: str = None) -> List[str]:
        """
        Extract key points from the content.

        Args:
            data: ExtractedData object
            requirement: Optional keyword/phrase to prioritize

        Returns:
            List of key points
        """
        key_points = []

        # If requirement specified, prioritize matching content
        if requirement:
            requirement_lower = requirement.lower()

            # Find headings that match requirement
            matching_headings = [h for h in data.headings if requirement_lower in h.lower()]
            key_points.extend(matching_headings[:5])

            # Find paragraphs that contain requirement
            matching_paras = [p for p in data.paragraphs if requirement_lower in p.lower()]
            for para in matching_paras[:3]:
                sentences = re.split(r'[.!?]+', para)
                for sentence in sentences:
                    if requirement_lower in sentence.lower():
                        key_points.append(f"• {sentence.strip()}")
                        break

        # Use headings as key points
        if data.headings:
            # Filter to main headings (H1, H2, H3)
            main_headings = [h for h in data.headings if h.startswith(('H1:', 'H2:', 'H3:'))]
            # Avoid duplicates
            for heading in main_headings[:10]:
                if heading not in key_points:
                    key_points.append(heading)

        # If not enough headings, add some key sentences from paragraphs
        if len(key_points) < 5 and data.paragraphs:
            for para in data.paragraphs[:5]:
                sentences = re.split(r'[.!?]+', para)
                if sentences:
                    first_sentence = sentences[0].strip()
                    if len(first_sentence.split()) > 5:  # Meaningful sentence
                        point = f"• {first_sentence}"
                        if point not in key_points:
                            key_points.append(point)

        return key_points[:15]  # Limit total to 15

    def _identify_topics(self, data: ExtractedData) -> List[str]:
        """
        Identify main topics from the content.

        Args:
            data: ExtractedData object

        Returns:
            List of topics
        """
        # Combine all text
        all_text = " ".join([data.title or ""] + data.headings + data.paragraphs)

        # Extract words (simple tokenization)
        words = re.findall(r'\b[a-zA-Z]{4,}\b', all_text.lower())

        # Common words to filter out (simplified stop words)
        stop_words = {
            'this', 'that', 'with', 'from', 'have', 'been', 'were', 'will',
            'would', 'could', 'should', 'their', 'about', 'which', 'there',
            'these', 'those', 'than', 'then', 'them', 'they', 'what', 'when',
            'where', 'more', 'some', 'such', 'into', 'through', 'also', 'very',
            'other', 'many', 'most', 'just', 'only', 'over', 'make', 'made',
            'year', 'years', 'page', 'site', 'website', 'home'
        }

        # Filter stop words and count frequency
        filtered_words = [w for w in words if w not in stop_words]
        word_freq = Counter(filtered_words)

        # Get most common words as topics
        topics = [word.title() for word, count in word_freq.most_common(10)
                  if count >= self.min_topic_frequency]

        return topics

    def _count_words(self, data: ExtractedData) -> int:
        """
        Count total words in the content.

        Args:
            data: ExtractedData object

        Returns:
            Word count
        """
        all_text = " ".join(data.paragraphs)
        words = re.findall(r'\b\w+\b', all_text)
        return len(words)

    def _determine_content_type(self, data: ExtractedData) -> str:
        """
        Determine the type of content.

        Args:
            data: ExtractedData object

        Returns:
            Content type string
        """
        title_lower = (data.title or "").lower()
        all_text = " ".join(data.headings + data.paragraphs[:5]).lower()

        # Simple heuristics
        if any(word in title_lower for word in ['blog', 'article', 'post']):
            return "Blog/Article"
        elif any(word in all_text for word in ['product', 'price', 'buy', 'shop', 'cart']):
            return "E-commerce"
        elif any(word in all_text for word in ['university', 'college', 'student', 'academic', 'education']):
            return "Educational/Academic"
        elif any(word in all_text for word in ['news', 'report', 'breaking']):
            return "News"
        elif any(word in all_text for word in ['about us', 'company', 'mission', 'team']):
            return "Corporate/Organization"
        else:
            return "General Website"

    def _calculate_importance_score(self, data: ExtractedData) -> float:
        """
        Calculate an importance/relevance score.

        Args:
            data: ExtractedData object

        Returns:
            Score between 0 and 1
        """
        score = 0.0

        # Has title
        if data.title:
            score += 0.2

        # Has substantial content
        if len(data.paragraphs) > 5:
            score += 0.2
        elif len(data.paragraphs) > 0:
            score += 0.1

        # Has structure (headings)
        if len(data.headings) > 5:
            score += 0.2
        elif len(data.headings) > 0:
            score += 0.1

        # Has metadata
        if data.metadata:
            score += 0.1

        # Has images
        if len(data.images) > 5:
            score += 0.1
        elif len(data.images) > 0:
            score += 0.05

        # Has links
        if len(data.links) > 10:
            score += 0.1
        elif len(data.links) > 0:
            score += 0.05

        # Word count
        word_count = self._count_words(data)
        if word_count > 1000:
            score += 0.15
        elif word_count > 300:
            score += 0.1
        elif word_count > 0:
            score += 0.05

        return min(score, 1.0)  # Cap at 1.0

    def _calculate_relevance(self, data: ExtractedData, requirement: str) -> float:
        """
        Calculate how relevant the page is to the requirement.

        Args:
            data: ExtractedData object
            requirement: Keyword/phrase to measure relevance against

        Returns:
            Relevance score between 0 and 1
        """
        score = 0.0
        requirement_lower = requirement.lower()

        # Count occurrences in different sections with different weights
        # Title matches are most important
        if data.title:
            title_matches = data.title.lower().count(requirement_lower)
            score += min(title_matches * 0.4, 0.4)

        # Heading matches are very important
        heading_matches = sum(h.lower().count(requirement_lower) for h in data.headings)
        score += min(heading_matches * 0.15, 0.3)

        # Paragraph matches (capped to avoid over-weighting)
        paragraph_matches = sum(p.lower().count(requirement_lower) for p in data.paragraphs)
        score += min(paragraph_matches * 0.05, 0.3)

        return min(score, 1.0)  # Cap at 1.0
