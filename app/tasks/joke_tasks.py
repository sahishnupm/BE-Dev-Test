import asyncio
from app.services.joke_service import JokeService

async def periodic_joke_sync():
    """Periodically fetch jokes every hour"""
    joke_service = JokeService()
    while True:
        try:
            await joke_service.fetch_and_save_joke()
        except Exception as e:
            print(f"Error in periodic sync: {e}")
        finally:
            await asyncio.sleep(3600) 