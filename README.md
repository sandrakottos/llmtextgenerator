# Web Crawler and AI Summarizer

**TL;DR:** Crawls websites via sitemaps, generates AI summaries, saves to llms.txt. Install dependencies, run python Final.py, enter a URL and OpenRouter API key.

A Python tool that crawls websites using their sitemaps and generates AI-powered summaries for each page. This tool leverages the OpenRouter AI API to create concise, meaningful summaries of web content, aligning with emerging standards like llms.txt for Generative Engine Optimization (GEO).

# Context: The Evolution of Search and Crawling

Search has evolved significantly over the years. Traditional web crawlers relied on robots.txt and sitemap.xml to index content for search engines like Google. However, with the rise of AI-driven search engines (e.g., Perplexity, GPT, Claude), new mediums and methods for indexing are emerging. These engines require richer, AI-friendly context to provide meaningful results.

This is where Jeremy Howard's proposed llms.txt standard comes in. The https://llmstxt.org/ proposal introduces llms.txt (and accompanying .md files) as a structured way for websites to provide AI-readable summaries of their content. This standard is poised to become as critical as robots.txt or sitemap.xml for indexing in generative AI engines. I like to call this approach Generative Engine Optimization (GEO), though it goes by various names.

Big websites like Stripe and Anthropic are already adopting this standard. You can see examples of adoption at https://llmstxt.site/. This tool is my contribution to this evolving ecosystem, enabling anyone to generate llms.txt-style summaries for their websites.

# Features

- Recursive sitemap crawling
- Intelligent text cleaning and processing
- AI-powered content summarization using the Qwen Turbo model
- Clean output format with page titles, URLs, and summaries
- Saves results to a text file (llms.txt)
- Lightweight and efficient for small to medium websites

# Requirements

```shell
pip install asyncio crawl4ai beautifulsoup4 requests
```

You'll also need an API key from https://openrouter.ai/ to power the AI summarization.

# Usage

1. Run the script:
```shell
python llmtxtgenerator.py
```

2. Enter the website URL when prompted (e.g., example.com, with or without http:// or https://).

3. Enter your OpenRouter API key when prompted. You can get one from https://openrouter.ai/.

4. The script will:
   - Locate and crawl the website's sitemap
   - Process each URL found
   - Generate AI-powered summaries using the Qwen Turbo model
   - Save the results to llms.txt

# API and Model Choice

To use this code, you'll need an OpenRouter API key from https://openrouter.ai/. I've chosen the Qwen Turbo model for summarization because it's fast, cost-effective, and provides high-quality results. When prompted, simply input your API token, and you're good to go!

# Output Format

```text
================================================================================
LLMS.txt Page for example.com
================================================================================
Links can be found below:
[Page Title] (https://example.com/page): A concise summary of the page content.
[Another Page] (https://example.com/another): Another page summary.
```

# Notes

- The script uses the Qwen Turbo model from https://openrouter.ai/ for summarization, which is super cheap to run.
- Supports various sitemap formats and locations (e.g., sitemap.xml, sitemap_index.xml).
- Includes HTML cleaning and text normalization for better summary quality.
- Basic error handling for failed requests and processing issues.
- Best suited for smaller websites for now (see future improvements below).

# Why llms.txt Matters

The llms.txt standard is a game-changer for AI-driven search. The https://llmstxt.org/ proposal explains how it provides a simple, machine-readable format for websites to expose their content to AI engines. This tool automates the creation of such files, making it easier for websites to adopt this standard and stay relevant in the age of GEO.

# Future Plans

I have ambitious plans to enhance this tool:

- Error Handling: Add validation for invalid API keys and better recovery from failures.
- Progress Bar: Include a visual progress indicator for long-running crawls.
- Rate Limiting: Prevent overwhelming target servers with too many requests.
- Command-Line Options: Add arguments for advanced configuration (e.g., output file name, model selection).
- Robots.txt Support: Parse robots.txt to respect site crawling restrictions.
- Selective Crawling: Add options to filter sitemap links, excluding irrelevant or low-priority pages (e.g., random or auto-generated URLs).
- Improved Code Structure: Refactor for better readability and maintainability with a clear, modular flow.
- Broader Compatibility: Enhance support for larger and more complex websites with diverse sitemap structures.

For now, the tool works best for smaller websites, but these updates will make it more robust and versatile.

# Contributing

Feel free to open issues or submit pull requests for improvements!

# Installation

```bash
# Clone the repository
git clone [your-repo-url]
cd [repo-name]

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the script
python llmtxtgenerator.py
```

# Troubleshooting

- **API Key Issues**: If you get authentication errors, verify your OpenRouter API key is valid
- **Sitemap Not Found**: Try manually locating the sitemap URL and passing it directly
- **Rate Limiting**: If you hit rate limits, try reducing concurrent requests

# Version
v1.0.0

# License
MIT License - See LICENSE file for details