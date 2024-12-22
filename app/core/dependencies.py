from fastapi import Path
from bson import ObjectId
from bson.errors import InvalidId
from app.core.exceptions import InvalidJokeIdException, JokeNotFoundException
from app.models import Joke
from typing import Annotated

async def validate_joke_id(
    joke_id: Annotated[str, Path(description="The ID of the joke to get")]
) -> ObjectId:
    try:
        return ObjectId(joke_id)
    except InvalidId:
        raise InvalidJokeIdException()

async def get_joke_or_404(obj_id: ObjectId) -> Joke:
    joke = await Joke.get(obj_id)
    if not joke:
        raise JokeNotFoundException()
    return joke 