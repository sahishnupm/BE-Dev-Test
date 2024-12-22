import pytest
from app.services.joke_service import JokeService
from app.core.exceptions import DuplicateJokeException, ExternalAPIException
from unittest.mock import patch, AsyncMock

pytestmark = pytest.mark.asyncio

class TestJokeService:
    async def test_create_joke(self, db):
        """Test creating a new joke via service"""
        
        joke_service = JokeService()
        joke_text = "Why did the scarecrow win an award?"
        source_id = "test123"
        joke = await joke_service.create_joke(joke_text, source_id)

        assert joke.joke_text == joke_text
        assert joke.source_id == source_id
        assert joke.id is not None

    async def test_create_duplicate_joke(self, db):
        """Test creating a duplicate joke raises exception"""
        
        joke_service = JokeService()
        joke_text = "Why did the scarecrow win an award?"
        
        await joke_service.create_joke(joke_text, "test123")
        with pytest.raises(DuplicateJokeException):
            await joke_service.create_joke(joke_text, "test456")

    async def test_update_joke(self, db):
        """Test updating a joke"""
        
        joke_service = JokeService()
        joke = await joke_service.create_joke("Original text", "test123")
        update_data = {"joke_text": "Updated text"}
        updated_joke = await joke_service.update_joke(joke, update_data)

        assert updated_joke.joke_text == update_data["joke_text"]
        assert updated_joke.updated_at is not None

    async def test_fetch_and_save_joke(self, db):
        """Test fetching and saving a joke from external API"""
        
        mock_joke = {
            "id": "test123",
            "joke": "Test external joke",
            "status": 200
        }
        
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = lambda: mock_joke

        with patch('httpx.AsyncClient.get', return_value=mock_response):
            joke_service = JokeService()
            joke = await joke_service.fetch_and_save_joke()

        assert joke.joke_text == mock_joke["joke"]
        assert joke.source_id == mock_joke["id"]

    async def test_fetch_and_save_joke_api_error(self, db):
        """Test handling API error when fetching joke"""
        
        mock_response = AsyncMock()
        mock_response.status_code = 500

        with patch('httpx.AsyncClient.get', return_value=mock_response):
            joke_service = JokeService()
            with pytest.raises(ExternalAPIException):
                await joke_service.fetch_and_save_joke() 