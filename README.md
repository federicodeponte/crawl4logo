# crawl4logo

A web crawler for logo detection using gpt-4o-mini. This tool crawls websites and identifies logos using OpenAI's vision API (supports both regular OpenAI and Azure OpenAI).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/federicodeponte/crawl4logo/actions/workflows/test.yml/badge.svg)](https://github.com/federicodeponte/crawl4logo/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Development Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/federicodeponte/crawl4logo)

> **⚠️ Status: Alpha** - This project is in early development. Test coverage is currently at 22%. Use with caution in production environments.
>
> **📢 v0.2.0 Breaking Changes**: If upgrading from v0.1.x, see [CHANGELOG.md](CHANGELOG.md#020---2025-11-23) for migration guide.

## Features

- Web crawling with async support
- Logo detection using gpt-4o-mini
- SVG to PNG conversion
- Image caching
- Confidence score extraction
- Detailed logo descriptions
- JSON output format

## Installation

### System Dependencies

Before installing the Python package, you need to install some system dependencies:

#### macOS
```bash
brew install cairo
```

#### Ubuntu/Debian
```bash
sudo apt-get install libcairo2-dev
```

#### Windows
Download and install Cairo from: https://www.cairographics.org/download/

### Python Package
```bash
pip install -e .
```

## Prerequisites

Before using this tool, you need:

1. **OpenAI API Key**: Get your API key from:
   - **Regular OpenAI**: [OpenAI Platform](https://platform.openai.com/) (recommended for most users)
   - **Azure OpenAI**: [Azure Portal](https://portal.azure.com/)
2. **System Dependencies**: Install Cairo as described in the Installation section above

## Usage

### Basic Usage (Regular OpenAI)

```python
import logging
from fede_crawl4ai import LogoCrawler

# Configure logging to see output (v0.2.0+)
logging.basicConfig(level=logging.INFO)

# Create a crawler instance with your OpenAI API key
crawler = LogoCrawler(api_key="your_openai_api_key_here")

# Crawl a website for logos
results = await crawler.crawl_website("https://example.com")

# Results are saved to results.json
```

### Azure OpenAI Usage (v0.2.0+)

```python
import logging
from fede_crawl4ai import LogoCrawler

logging.basicConfig(level=logging.INFO)

# Azure OpenAI requires endpoint parameter
crawler = LogoCrawler(
    api_key="your_azure_api_key_here",
    use_azure=True,
    azure_endpoint="https://yourcompany.openai.azure.com"  # Required!
)

results = await crawler.crawl_website("https://example.com")
```

**Important**:
- You must provide your own OpenAI API key
- v0.2.0+ uses Python logging instead of print statements
- Azure users must provide `azure_endpoint` parameter

## Configuration

### Environment Variables (v0.2.0+)

You can configure the crawler using environment variables:

```bash
# For regular OpenAI
export OPENAI_API_KEY="your_api_key_here"

# For Azure OpenAI (v0.2.0+)
export AZURE_OPENAI_API_KEY="your_api_key_here"
export AZURE_OPENAI_ENDPOINT="https://yourcompany.openai.azure.com"
export AZURE_OPENAI_DEPLOYMENT="gpt-4o-mini"  # Optional, defaults to gpt-4o-mini
export AZURE_API_VERSION="2024-02-15-preview"  # Optional
```

Then use the configuration module:

```python
import logging
from fede_crawl4ai.config import LogoCrawlerConfig
from fede_crawl4ai import LogoCrawler

logging.basicConfig(level=logging.INFO)

# Load configuration from environment variables
config = LogoCrawlerConfig.from_env(use_azure=True)  # or False for regular OpenAI
crawler = LogoCrawler(config=config)
```

**Or use environment variables with manual initialization:**

```python
import os
from fede_crawl4ai import LogoCrawler

# For regular OpenAI
crawler = LogoCrawler(api_key=os.getenv("OPENAI_API_KEY"))

# For Azure OpenAI
crawler = LogoCrawler(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    use_azure=True,
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
```

See [`.env.example`](.env.example) for all available configuration options.

## Output Format

The tool generates a JSON file containing:
- Image URL
- Confidence score
- Logo description
- Source page URL
- Image hash
- Timestamp
- Rank score
- Detection scores (if available)

## Testing

This project uses pytest for testing. Current test coverage is **22%** (v0.2.0).

```bash
# Run tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=fede_crawl4ai --cov-report=term-missing
```

**Test Status:**
- ✅ Unit tests: 11 tests covering core utilities
- ✅ Integration tests: 1 test (mocked OpenAI responses)
- ⚠️ Async/OpenAI integration: Not yet tested
- ⚠️ E2E tests: Not yet implemented

Contributions to improve test coverage are especially welcome!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
