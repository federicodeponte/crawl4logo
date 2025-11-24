"""Image caching for analyzed logo results."""

import logging
from typing import Optional, Dict
from datetime import datetime, timedelta
from ..models import LogoResult

logger = logging.getLogger(__name__)


class ImageCache:
    """In-memory cache for analyzed images with TTL support."""

    def __init__(self, ttl: timedelta = timedelta(days=1)):
        """
        Initialize image cache.

        Args:
            ttl: Time-to-live for cache entries (default: 1 day)
        """
        self._cache: Dict[str, LogoResult] = {}
        self._ttl = ttl
        logger.debug(f"ImageCache initialized with TTL: {ttl}")

    def get(self, image_hash: str) -> Optional[LogoResult]:
        """
        Get cached result if not expired.

        Args:
            image_hash: MD5 hash of image content

        Returns:
            Cached LogoResult if found and not expired, None otherwise
        """
        if image_hash not in self._cache:
            logger.debug(f"Cache miss for hash: {image_hash}")
            return None

        result = self._cache[image_hash]

        # Check if expired
        if datetime.now() - result.timestamp > self._ttl:
            logger.debug(f"Cache entry expired for hash: {image_hash}")
            del self._cache[image_hash]
            return None

        logger.debug(f"Cache hit for hash: {image_hash}")
        return result

    def set(self, image_hash: str, result: LogoResult) -> None:
        """
        Cache a logo analysis result.

        Args:
            image_hash: MD5 hash of image content
            result: LogoResult to cache
        """
        self._cache[image_hash] = result
        logger.debug(f"Cached result for hash: {image_hash}")

    def clear(self) -> None:
        """Clear all cached results."""
        count = len(self._cache)
        self._cache.clear()
        logger.info(f"Cleared {count} cached entries")

    def size(self) -> int:
        """
        Get number of cached entries.

        Returns:
            Number of entries in cache
        """
        return len(self._cache)
