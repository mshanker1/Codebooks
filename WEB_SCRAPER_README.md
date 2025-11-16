# Web Scraper Agent System

An intelligent, agent-based architecture for retrieving, analyzing, and presenting web content.

## Overview

This system implements a multi-agent architecture where specialized agents collaborate to scrape websites, extract meaningful data, perform analysis, and present results in a clear, formatted way.

## Architecture

The system consists of four main agents:

### 1. WebScraperAgent
**Responsibility:** Fetching and extracting content from web pages

**Features:**
- HTTP request handling with timeout support
- HTML parsing using BeautifulSoup
- Extraction of titles, headings, paragraphs, links, images
- Metadata extraction
- Main content identification

### 2. AnalyzerAgent
**Responsibility:** Analyzing and summarizing extracted content

**Features:**
- Content summarization
- Key point extraction
- Topic identification using word frequency analysis
- Word count statistics
- Content type classification (Educational, E-commerce, News, etc.)
- Importance scoring

### 3. PresenterAgent
**Responsibility:** Formatting and presenting results

**Features:**
- Multiple output formats: Text, Markdown, HTML
- Professional formatting
- Clear section organization
- Comprehensive reporting

### 4. AgentOrchestrator
**Responsibility:** Coordinating the workflow between agents

**Features:**
- Sequential workflow management
- Error handling
- Result persistence (save to file)
- Agent status monitoring

## Installation

1. **Clone or download this repository**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

Required packages:
- requests (HTTP client)
- beautifulsoup4 (HTML parsing)
- lxml (HTML parser backend)
- chardet (character encoding detection)

## Usage

### Basic Command Line Usage

```bash
# Scrape and analyze a website
python main.py https://www.example.com

# Save results to a file
python main.py https://www.example.com -o output.txt

# Use markdown format
python main.py https://www.example.com --format markdown -o report.md

# Use HTML format
python main.py https://www.example.com --format html -o report.html

# Set custom timeout
python main.py https://www.example.com --timeout 60

# Quiet mode (suppress agent logs)
python main.py https://www.example.com --quiet
```

### Python API Usage

```python
from web_scraper_agents import AgentOrchestrator

# Create orchestrator with custom configuration
config = {
    'scraper': {
        'timeout': 30,
        'user_agent': 'MyCustomBot/1.0'
    },
    'analyzer': {
        'max_summary_sentences': 5,
        'min_topic_frequency': 3
    },
    'presenter': {
        'output_format': 'markdown'  # 'text', 'markdown', or 'html'
    }
}

orchestrator = AgentOrchestrator(config)

# Execute the pipeline
result = orchestrator.execute(
    url='https://www.example.com',
    save_to_file='output.md'
)

# Access the formatted text
print(result.formatted_text)
```

### Using Individual Agents

```python
from web_scraper_agents import WebScraperAgent, AnalyzerAgent, PresenterAgent

# Use agents individually
scraper = WebScraperAgent({'timeout': 30})
analyzer = AnalyzerAgent()
presenter = PresenterAgent({'output_format': 'markdown'})

# Execute pipeline manually
extracted_data = scraper.execute('https://www.example.com')
analysis = analyzer.execute(extracted_data)
presentation = presenter.execute(extracted_data, analysis)

print(presentation.formatted_text)
```

## Output Format

The system provides comprehensive analysis including:

- **Basic Information:** URL, title, content type, word count, importance score
- **Summary:** Auto-generated summary with key insights
- **Key Points:** Main topics and highlights extracted from headings and content
- **Identified Topics:** Frequently mentioned topics derived from content analysis
- **Page Structure:** Statistics on headings, paragraphs, links, and images
- **Sample Links:** Preview of important links found on the page
- **Metadata:** SEO and social media metadata

## Example Output

### Text Format
```
================================================================================
WEB SCRAPER AGENT - ANALYSIS REPORT
================================================================================

BASIC INFORMATION
--------------------------------------------------------------------------------
URL:           https://www.example.com
Title:         Example Domain
Content Type:  General Website
Word Count:    150
Importance:    0.75/1.00
Analysis Time: 2025-11-16 15:30:45

SUMMARY
--------------------------------------------------------------------------------
Page Title: Example Domain
Description: This domain is for use in illustrative examples...
...
```

### Markdown Format
```markdown
# Web Scraper Agent - Analysis Report

## Basic Information
- **URL:** https://www.example.com
- **Title:** Example Domain
- **Content Type:** General Website
...
```

### HTML Format
Full-featured HTML report with CSS styling, suitable for viewing in a browser.

## Project Structure

```
Codebooks/
├── web_scraper_agents/
│   ├── __init__.py           # Package initialization
│   ├── base_agent.py         # Abstract base class for agents
│   ├── scraper_agent.py      # Web scraping agent
│   ├── analyzer_agent.py     # Content analysis agent
│   ├── presenter_agent.py    # Result formatting agent
│   ├── orchestrator.py       # Agent coordinator
│   └── models.py             # Data models
├── main.py                   # CLI entry point
├── requirements.txt          # Python dependencies
└── WEB_SCRAPER_README.md     # This file
```

## Configuration Options

### Scraper Agent
- `timeout`: HTTP request timeout in seconds (default: 30)
- `user_agent`: Custom user agent string

### Analyzer Agent
- `max_summary_sentences`: Maximum sentences in summary (default: 5)
- `min_topic_frequency`: Minimum word frequency to be considered a topic (default: 3)

### Presenter Agent
- `output_format`: Output format - 'text', 'markdown', or 'html' (default: 'text')

## Error Handling

The system includes comprehensive error handling:
- Network errors (timeout, connection failed)
- Invalid URLs
- HTML parsing errors
- File I/O errors

Errors are logged and a graceful error report is generated.

## Extensibility

The agent-based architecture is designed for easy extension:

1. **Add new agents:** Inherit from `BaseAgent` and implement the `execute()` method
2. **Modify existing agents:** Each agent is independent and can be enhanced
3. **Custom data models:** Add new fields to existing models in `models.py`
4. **Custom output formats:** Add new format methods to `PresenterAgent`

## Test Example

To test the system with the Maryville College website:

```bash
python main.py https://www.maryvillecollege.edu/ -o maryville_report.txt
```

Or with markdown format:
```bash
python main.py https://www.maryvillecollege.edu/ --format markdown -o maryville_report.md
```

## Best Practices

1. **Respect robots.txt:** The system doesn't automatically check robots.txt. Please respect website crawling policies.
2. **Rate limiting:** Avoid scraping the same site repeatedly in quick succession
3. **User agent:** Consider setting a custom user agent that identifies your use case
4. **Timeout:** Adjust timeout based on network conditions and site responsiveness

## Limitations

- JavaScript-heavy websites may not render correctly (considers only static HTML)
- No authentication support (public pages only)
- Does not follow pagination or multiple pages
- Text-based analysis (no AI/LLM integration for semantic understanding)

## Future Enhancements

Potential improvements:
- JavaScript rendering support (Selenium/Playwright)
- Multi-page crawling
- Authentication support
- LLM integration for semantic analysis
- Database storage for results
- Web UI dashboard
- Scheduled scraping
- Comparison of changes over time

## License

This project is provided as-is for educational and development purposes.

## Author

Created as a demonstration of agent-based architecture for web scraping and analysis.
