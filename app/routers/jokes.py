from fastapi import APIRouter, Depends, status
from typing import List
from app.models import Joke, JokeCreate, JokeUpdate
from app.services.joke_service import JokeService
from app.core.dependencies import validate_joke_id, get_joke_or_404
from bson import ObjectId
from loguru import logger

router = APIRouter(
    prefix="/jokes",
    tags=["jokes"],
)
joke_service = JokeService()

@router.post("/", response_model=Joke, status_code=status.HTTP_201_CREATED,
             summary="Create a new joke",
             description="Creates a new joke in the database with the given text and optional source ID.")
async def create_joke(joke: JokeCreate):
    logger.info("Received request to create new joke")
    return await joke_service.create_joke(
        joke_text=joke.joke_text,
        source_id=joke.source_id
    )

@router.get("/", response_model=List[Joke])
async def get_jokes():
    logger.info("Fetching all jokes")
    jokes = await Joke.find_all().to_list()
    logger.info(f"Retrieved {len(jokes)} jokes")
    return jokes

@router.get("/{joke_id}", response_model=Joke)
async def get_joke(obj_id: ObjectId = Depends(validate_joke_id)):
    logger.info(f"Fetching joke with ID: {obj_id}")
    return await get_joke_or_404(obj_id)

@router.put("/{joke_id}", response_model=Joke)
async def update_joke(
    joke_update: JokeUpdate,
    obj_id: ObjectId = Depends(validate_joke_id)
):
    logger.info(f"Updating joke with ID: {obj_id}")
    joke = await get_joke_or_404(obj_id)
    update_data = joke_update.dict(exclude_unset=True)
    return await joke_service.update_joke(joke, update_data)

@router.delete("/{joke_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_joke(obj_id: ObjectId = Depends(validate_joke_id)):
    logger.info(f"Deleting joke with ID: {obj_id}")
    joke = await get_joke_or_404(obj_id)
    await joke.delete()
    logger.info(f"Successfully deleted joke with ID: {obj_id}")

@router.post("/sync", response_model=Joke, status_code=status.HTTP_201_CREATED)
async def sync_joke():
    """Manually trigger fetching and saving a new joke"""
    logger.info("Manually syncing new joke")
    return await joke_service.fetch_and_save_joke()