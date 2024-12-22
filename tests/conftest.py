import pytest
import asyncio
from httpx import AsyncClient
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models import Joke
from app.main import app



@pytest.fixture(scope="session")
def event_loop():
    """Override the default pytest-asyncio event_loop fixture to session scope."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def db():
    """Initialize database connection"""
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    client.get_io_loop = asyncio.get_running_loop
    database = client["dad_jokes_test_db"]

    # Initialize Beanie with the test database
    await init_beanie(
        database=database,
        document_models=[Joke]
    )
    await database["joke"].create_index("id")  
    yield database
    print("Cleaning up database")
    await client.drop_database("dad_jokes_test_db")
    client.close()

@pytest.fixture(autouse=True)
async def setup_db(db):
    """Setup database for each test"""
    try:
        yield
    finally:
        if db is not None:
            await Joke.delete_all()

@pytest.fixture
async def test_client(db):
    """Create test client"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        print("Test client created")
        yield client
        print("Test client teardown")
