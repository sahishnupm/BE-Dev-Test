import httpx
from app.models import Joke
from app.core.exceptions import DuplicateJokeException, ExternalAPIException, DatabaseException
import os
from dotenv import load_dotenv
from datetime import datetime
from loguru import logger

load_dotenv()

class JokeService:
    @staticmethod
    async def create_joke(joke_text: str, source_id: str = None) -> Joke:
        logger.info(f"Creating new joke with text: {joke_text[:30]}...")
        try:
            # Check for duplicate
            existing_joke = await Joke.find_one({"joke_text": joke_text})
            if existing_joke:
                logger.warning(f"Duplicate joke found: {joke_text[:30]}...")
                raise DuplicateJokeException()
            
            new_joke = Joke(
                joke_text=joke_text,
                source_id=source_id
            )
            await new_joke.insert()
            logger.info(f"Successfully created joke with ID: {new_joke.id}")
            return new_joke
        except DuplicateJokeException:
            raise
        except Exception as e:
            logger.error(f"An error occurred while creating a joke: {str(e)}")
            raise DatabaseException("Failed to update joke") from e

    @staticmethod
    async def update_joke(joke: Joke, update_data: dict) -> Joke:
        logger.info(f"Updating joke with ID: {joke.id}")
        try:
            if update_data:
                existing_joke = await Joke.find_one({"joke_text":update_data['joke_text']})
                if existing_joke:
                    logger.warning(f"Duplicate joke found: {update_data['joke_text'][:30]}...")
                    raise DuplicateJokeException()
                update_data["updated_at"] = datetime.now()
                await joke.update({"$set": update_data})
                logger.info(f"Successfully updated joke with ID: {joke.id}")
            return joke
        except DuplicateJokeException:
            raise
        except Exception as e:
            logger.error(f"An error occurred while updating joke with ID {joke.id}: {str(e)}")
            raise DatabaseException("Failed to update joke") from e

    @staticmethod
    async def fetch_and_save_joke():
        """Fetch a single joke from the API and save it to database"""
        logger.info("Fetching new joke from external API")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    os.getenv("DADJOKES_API_URL"),
                    headers={"Accept": "application/json"}
                )
                
                if response.status_code != 200:
                    logger.error(f"External API returned status code: {response.status_code}")
                    raise ExternalAPIException()
                
                joke_data = response.json()
                logger.debug(f"Received joke from API: {joke_data['joke'][:30]}...")
                return await JokeService.create_joke(
                    joke_text=joke_data["joke"],
                    source_id=joke_data["id"]
                )
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred while fetching joke: {str(e)}")
            raise ExternalAPIException() 