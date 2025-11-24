"""Unit tests for CloudStorage."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from fede_crawl4ai.storage.cloud import CloudStorage, SUPABASE_AVAILABLE


class TestCloudStorage:
    """Test CloudStorage functionality."""

    def test_initialization_without_credentials(self):
        """Test cloud storage initializes but disabled without credentials."""
        storage = CloudStorage()

        assert not storage.is_configured()

    def test_initialization_with_partial_credentials(self):
        """Test cloud storage disabled with partial credentials."""
        storage1 = CloudStorage(url="https://test.supabase.co")
        assert not storage1.is_configured()

        storage2 = CloudStorage(key="test_key")
        assert not storage2.is_configured()

    @pytest.mark.skipif(not SUPABASE_AVAILABLE, reason="Supabase not installed")
    def test_initialization_with_credentials(self):
        """Test cloud storage initializes with valid credentials."""
        with patch("fede_crawl4ai.storage.cloud.create_client") as mock_create:
            mock_client = Mock()
            mock_create.return_value = mock_client

            storage = CloudStorage(url="https://test.supabase.co", key="test_key")

            assert storage.is_configured()
            mock_create.assert_called_once_with("https://test.supabase.co", "test_key")

    @pytest.mark.skipif(not SUPABASE_AVAILABLE, reason="Supabase not installed")
    def test_initialization_handles_error(self):
        """Test cloud storage handles initialization errors gracefully."""
        with patch(
            "fede_crawl4ai.storage.cloud.create_client", side_effect=Exception("Connection error")
        ):
            storage = CloudStorage(url="https://test.supabase.co", key="test_key")

            assert not storage.is_configured()

    @pytest.mark.asyncio
    async def test_upload_without_client(self):
        """Test upload returns None when client not configured."""
        storage = CloudStorage()

        result = await storage.upload(b"fake_image_data", "test.png")

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.skipif(not SUPABASE_AVAILABLE, reason="Supabase not installed")
    async def test_upload_success(self):
        """Test successful image upload."""
        with patch("fede_crawl4ai.storage.cloud.create_client") as mock_create:
            mock_client = Mock()
            mock_storage = Mock()
            mock_bucket = Mock()

            # Setup mock chain
            mock_client.storage.from_.return_value = mock_bucket
            mock_bucket.upload.return_value = None
            mock_bucket.get_public_url.return_value = "https://storage.url/test.png"

            mock_create.return_value = mock_client

            storage = CloudStorage(url="https://test.supabase.co", key="test_key")

            result = await storage.upload(b"fake_image_data", "test.png")

            assert result == "https://storage.url/test.png"
            mock_bucket.upload.assert_called_once()
            mock_bucket.get_public_url.assert_called_once_with("background-removed/test.png")

    @pytest.mark.asyncio
    @pytest.mark.skipif(not SUPABASE_AVAILABLE, reason="Supabase not installed")
    async def test_upload_with_custom_bucket_and_folder(self):
        """Test upload with custom bucket and folder."""
        with patch("fede_crawl4ai.storage.cloud.create_client") as mock_create:
            mock_client = Mock()
            mock_bucket = Mock()

            mock_client.storage.from_.return_value = mock_bucket
            mock_bucket.upload.return_value = None
            mock_bucket.get_public_url.return_value = "https://storage.url/test.png"

            mock_create.return_value = mock_client

            storage = CloudStorage(url="https://test.supabase.co", key="test_key")

            result = await storage.upload(
                b"fake_image_data", "test.png", bucket="custom-bucket", folder="custom-folder"
            )

            assert result == "https://storage.url/test.png"
            mock_client.storage.from_.assert_called_with("custom-bucket")
            mock_bucket.get_public_url.assert_called_once_with("custom-folder/test.png")

    @pytest.mark.asyncio
    @pytest.mark.skipif(not SUPABASE_AVAILABLE, reason="Supabase not installed")
    async def test_upload_handles_error(self):
        """Test upload handles errors gracefully."""
        with patch("fede_crawl4ai.storage.cloud.create_client") as mock_create:
            mock_client = Mock()
            mock_bucket = Mock()

            mock_client.storage.from_.return_value = mock_bucket
            mock_bucket.upload.side_effect = Exception("Upload failed")

            mock_create.return_value = mock_client

            storage = CloudStorage(url="https://test.supabase.co", key="test_key")

            result = await storage.upload(b"fake_image_data", "test.png")

            assert result is None

    def test_is_configured(self):
        """Test is_configured method."""
        storage_unconfigured = CloudStorage()
        assert not storage_unconfigured.is_configured()

        if SUPABASE_AVAILABLE:
            with patch("fede_crawl4ai.storage.cloud.create_client") as mock_create:
                mock_create.return_value = Mock()
                storage_configured = CloudStorage(url="https://test.supabase.co", key="test_key")
                assert storage_configured.is_configured()
