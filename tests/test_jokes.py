import pytest
from httpx import AsyncClient
from bson import ObjectId
from unittest.mock import patch, AsyncMock


pytestmark = pytest.mark.asyncio

class TestJokeEndpoints:
    async def test_create_joke(self, test_client: AsyncClient, db):
        """Test creating a new joke"""

        joke_data = {
            "joke_text": "Why did the scarecrow win an award? He was outstanding in his field!",
            "source_id": "test123"
        }

        response = await test_client.post("/jokes/", json=joke_data)
        assert response.status_code == 201
        data = response.json()
        assert data["joke_text"] == joke_data["joke_text"]
        assert data["source_id"] == joke_data["source_id"]
        assert "_id" in data
        assert "created_at" in data

    async def test_create_duplicate_joke(self, test_client: AsyncClient):
        """Test creating a duplicate joke returns error"""
        joke_data = {
            "joke_text": "Why did the scarecrow win an award? He was outstanding in his field!",
            "source_id": "test123"
        }
        
        await test_client.post("/jokes/", json=joke_data)
        response = await test_client.post("/jokes/", json=joke_data)
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Joke already exists"

    async def test_get_all_jokes(self, test_client: AsyncClient):
        """Test retrieving all jokes"""
        jokes = [
            {"joke_text": f"Test joke {i}", "source_id": f"test{i}"}
            for i in range(3)
        ]
        for joke in jokes:
            await test_client.post("/jokes/", json=joke)

        response = await test_client.get("/jokes/")        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all(joke["joke_text"].startswith("Test joke") for joke in data)

    async def test_get_joke_by_id(self, test_client: AsyncClient):
        """Test retrieving a specific joke by ID"""
        joke_data = {
            "joke_text": "Why did the cookie go to the doctor? Because it was feeling crumbly!",
            "source_id": "test123"
        }
        create_response = await test_client.post("/jokes/", json=joke_data)
        joke_id = create_response.json()["_id"]

        response = await test_client.get(f"/jokes/{joke_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["joke_text"] == joke_data["joke_text"]
        assert data["_id"] == joke_id

    async def test_get_nonexistent_joke(self, test_client: AsyncClient):
        """Test retrieving a non-existent joke returns 404"""
        nonexistent_id = str(ObjectId())

        response = await test_client.get(f"/jokes/{nonexistent_id}")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Joke not found"

    async def test_update_joke(self, test_client: AsyncClient):
        """Test updating an existing joke"""

        joke_data = {
            "joke_text": "Original joke text",
            "source_id": "test123"
        }
        create_response = await test_client.post("/jokes/", json=joke_data)
        joke_id = create_response.json()["_id"]
        
        update_data = {"joke_text": "Updated joke text"}

        response = await test_client.put(f"/jokes/{joke_id}", json=update_data)        
        assert response.status_code == 200
        data = response.json()
        assert data["joke_text"] == update_data["joke_text"]
        assert data["updated_at"] is not None

    async def test_delete_joke(self, test_client: AsyncClient):
        """Test deleting a joke"""

        joke_data = {
            "joke_text": "Why did the math book look sad? Because it had too many problems!",
            "source_id": "test123"
        }
        create_response = await test_client.post("/jokes/", json=joke_data)
        joke_id = create_response.json()["_id"]

        delete_response = await test_client.delete(f"/jokes/{joke_id}")
        get_response = await test_client.get(f"/jokes/{joke_id}")
        
        assert delete_response.status_code == 204
        assert get_response.status_code == 404

    async def test_sync_joke(self, test_client: AsyncClient):
        """Test fetching and saving a joke from external API"""
        mock_joke = {
            "id": "test123",
            "joke": "Why don't eggs tell jokes? They'd crack up!",
            "status": 200
        }
        
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json = lambda: mock_joke

        with patch('httpx.AsyncClient.get', return_value=mock_response):
            response = await test_client.post("/jokes/sync")
        
        assert response.status_code == 201
        data = response.json()
        assert data["joke_text"] == mock_joke["joke"]
        assert data["source_id"] == mock_joke["id"]

    async def test_sync_joke_api_error(self, test_client: AsyncClient):
        """Test handling external API error during joke sync"""

        mock_response = AsyncMock()
        mock_response.status_code = 500

        with patch('httpx.AsyncClient.get', return_value=mock_response):
            response = await test_client.post("/jokes/sync")
        
        assert response.status_code == 503
        assert response.json()["detail"] == "Failed to fetch joke from external API" 


