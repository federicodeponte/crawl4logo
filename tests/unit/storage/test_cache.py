"""Unit tests for ImageCache."""

import pytest
from datetime import datetime, timedelta
from fede_crawl4ai.storage.cache import ImageCache
from fede_crawl4ai.models import LogoResult


class TestImageCache:
    """Test ImageCache functionality."""

    def test_cache_initialization(self):
        """Test cache initializes with correct TTL."""
        ttl = timedelta(hours=2)
        cache = ImageCache(ttl=ttl)

        assert cache._ttl == ttl
        assert cache.size() == 0

    def test_cache_miss(self):
        """Test getting non-existent entry returns None."""
        cache = ImageCache()
        result = cache.get("nonexistent_hash")

        assert result is None

    def test_cache_hit(self):
        """Test caching and retrieving valid entry."""
        cache = ImageCache()

        logo = LogoResult(
            url="https://example.com/logo.png",
            confidence=0.95,
            description="Test logo",
            page_url="https://example.com",
            image_hash="abc123",
        )

        cache.set("abc123", logo)
        retrieved = cache.get("abc123")

        assert retrieved is not None
        assert retrieved.url == "https://example.com/logo.png"
        assert retrieved.confidence == 0.95
        assert retrieved.image_hash == "abc123"

    def test_cache_expiration(self):
        """Test cache entries expire after TTL."""
        # Create cache with 1 microsecond TTL
        cache = ImageCache(ttl=timedelta(microseconds=1))

        logo = LogoResult(
            url="https://example.com/logo.png",
            confidence=0.95,
            description="Test logo",
            page_url="https://example.com",
            image_hash="abc123",
        )

        cache.set("abc123", logo)

        # Wait for expiration (even small delay should be enough)
        import time

        time.sleep(0.001)  # 1ms = 1000 microseconds

        retrieved = cache.get("abc123")
        assert retrieved is None  # Should be expired

    def test_cache_not_expired(self):
        """Test cache entries don't expire before TTL."""
        # Create cache with long TTL
        cache = ImageCache(ttl=timedelta(hours=1))

        logo = LogoResult(
            url="https://example.com/logo.png",
            confidence=0.95,
            description="Test logo",
            page_url="https://example.com",
            image_hash="abc123",
        )

        cache.set("abc123", logo)
        retrieved = cache.get("abc123")

        assert retrieved is not None
        assert retrieved.url == "https://example.com/logo.png"

    def test_cache_set_overwrites(self):
        """Test setting same hash overwrites previous value."""
        cache = ImageCache()

        logo1 = LogoResult(
            url="https://example.com/logo1.png",
            confidence=0.8,
            description="First logo",
            page_url="https://example.com",
            image_hash="abc123",
        )

        logo2 = LogoResult(
            url="https://example.com/logo2.png",
            confidence=0.9,
            description="Second logo",
            page_url="https://example.com",
            image_hash="abc123",
        )

        cache.set("abc123", logo1)
        cache.set("abc123", logo2)  # Overwrite

        retrieved = cache.get("abc123")
        assert retrieved is not None
        assert retrieved.url == "https://example.com/logo2.png"
        assert retrieved.confidence == 0.9

    def test_cache_clear(self):
        """Test clearing all cache entries."""
        cache = ImageCache()

        logo1 = LogoResult(
            url="https://example.com/logo1.png",
            confidence=0.8,
            description="Logo 1",
            page_url="https://example.com",
            image_hash="hash1",
        )

        logo2 = LogoResult(
            url="https://example.com/logo2.png",
            confidence=0.9,
            description="Logo 2",
            page_url="https://example.com",
            image_hash="hash2",
        )

        cache.set("hash1", logo1)
        cache.set("hash2", logo2)
        assert cache.size() == 2

        cache.clear()
        assert cache.size() == 0
        assert cache.get("hash1") is None
        assert cache.get("hash2") is None

    def test_cache_size(self):
        """Test cache size tracking."""
        cache = ImageCache()
        assert cache.size() == 0

        logo = LogoResult(
            url="https://example.com/logo.png",
            confidence=0.95,
            description="Test logo",
            page_url="https://example.com",
            image_hash="abc123",
        )

        cache.set("hash1", logo)
        assert cache.size() == 1

        cache.set("hash2", logo)
        assert cache.size() == 2

        cache.clear()
        assert cache.size() == 0

    def test_cache_multiple_entries(self):
        """Test cache handles multiple different entries."""
        cache = ImageCache()

        logos = []
        for i in range(5):
            logo = LogoResult(
                url=f"https://example.com/logo{i}.png",
                confidence=0.9,
                description=f"Logo {i}",
                page_url="https://example.com",
                image_hash=f"hash{i}",
            )
            logos.append(logo)
            cache.set(f"hash{i}", logo)

        # Verify all entries retrievable
        for i in range(5):
            retrieved = cache.get(f"hash{i}")
            assert retrieved is not None
            assert retrieved.url == f"https://example.com/logo{i}.png"

        assert cache.size() == 5
