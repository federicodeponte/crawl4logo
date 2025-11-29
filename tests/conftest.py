"""Pytest configuration for crawl4logo tests."""

import pytest


@pytest.fixture
def mock_api_key():
    """Return a mock API key for testing."""
    return "test-api-key-for-testing"

