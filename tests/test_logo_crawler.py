"""
Unit tests for crawl4logo.

Run with: pytest tests/
"""

import pytest
from unittest.mock import patch, MagicMock


class TestLogoCrawlerInit:
    """Test LogoCrawler initialization."""

    def test_requires_api_key(self):
        """LogoCrawler should raise ValueError without api_key."""
        from crawl4logo import LogoCrawler
        
        with pytest.raises(ValueError, match="API key is required"):
            LogoCrawler()

    def test_accepts_api_key(self):
        """LogoCrawler should accept api_key parameter."""
        from crawl4logo import LogoCrawler
        
        crawler = LogoCrawler(api_key="test-key-123")
        assert crawler.api_key == "test-key-123"

    def test_use_azure_flag(self):
        """LogoCrawler should accept use_azure flag."""
        from crawl4logo import LogoCrawler
        
        crawler = LogoCrawler(api_key="test-key", use_azure=True)
        assert crawler.use_azure is True


class TestBrowserHeaders:
    """Test browser headers are present."""

    def test_browser_headers_defined(self):
        """BROWSER_HEADERS should be defined in crawler module."""
        from crawl4logo.crawler import BROWSER_HEADERS
        
        assert "User-Agent" in BROWSER_HEADERS
        assert "Chrome" in BROWSER_HEADERS["User-Agent"]
