from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

async def init_db():
    # Create Motor client
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    
    # Initialize beanie with the Product document class
    from app.models import Joke
    await init_beanie(
        database=client[os.getenv("DATABASE_NAME")],
        document_models=[Joke]
    ) 