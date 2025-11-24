"""Cloud storage for processed images."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Try to import supabase (optional dependency)
try:
    from supabase import create_client, Client

    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None  # type: ignore


class CloudStorage:
    """Upload images to cloud storage (Supabase).

    This is an optional feature that requires the 'supabase' package
    and valid Supabase credentials.
    """

    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        """
        Initialize cloud storage.

        Args:
            url: Supabase project URL
            key: Supabase API key

        Note:
            If either url or key is None, or if supabase package is not installed,
            upload operations will silently return None.
        """
        self._url = url
        self._key = key
        self._client: Optional[Client] = None

        if SUPABASE_AVAILABLE and url and key:
            try:
                self._client = create_client(url, key)
                logger.info("Cloud storage initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize cloud storage: {e}")
                self._client = None
        elif not SUPABASE_AVAILABLE:
            logger.debug("Supabase package not available - cloud storage disabled")
        else:
            logger.debug("Cloud storage not configured (missing URL or key)")

    async def upload(
        self,
        image_data: bytes,
        filename: str,
        bucket: str = "logo-images",
        folder: str = "background-removed",
    ) -> Optional[str]:
        """
        Upload image to cloud storage and return public URL.

        Args:
            image_data: Raw image bytes
            filename: Desired filename
            bucket: Storage bucket name (default: "logo-images")
            folder: Folder within bucket (default: "background-removed")

        Returns:
            Public URL of uploaded image, or None if upload failed or storage not configured
        """
        if not self._client:
            logger.debug("Cloud storage not initialized - skipping upload")
            return None

        try:
            file_path = f"{folder}/{filename}"

            # Upload to Supabase storage
            self._client.storage.from_(bucket).upload(
                path=file_path, file=image_data, file_options={"content-type": "image/png"}
            )

            # Get public URL
            public_url = self._client.storage.from_(bucket).get_public_url(file_path)
            logger.info(f"Successfully uploaded to cloud: {public_url}")
            return public_url

        except Exception as e:
            logger.error(f"Failed to upload image to cloud storage: {e}")
            return None

    def is_configured(self) -> bool:
        """
        Check if cloud storage is properly configured.

        Returns:
            True if client is initialized and ready to use
        """
        return self._client is not None
