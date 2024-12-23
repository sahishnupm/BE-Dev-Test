from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import (
    JokeNotFoundException,
    InvalidJokeIdException,
    DuplicateJokeException,
    ExternalAPIException,
    DatabaseException
)

async def joke_not_found_handler(request: Request, exc: JokeNotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

async def invalid_joke_id_handler(request: Request, exc: InvalidJokeIdException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

async def duplicate_joke_handler(request: Request, exc: DuplicateJokeException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

async def external_api_handler(request: Request, exc: ExternalAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
async def database_exception_handler(request: Request, exc: DatabaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

def add_exception_handlers(app):
    """Register all exception handlers to the app"""
    app.add_exception_handler(JokeNotFoundException, joke_not_found_handler)
    app.add_exception_handler(InvalidJokeIdException, invalid_joke_id_handler)
    app.add_exception_handler(DuplicateJokeException, duplicate_joke_handler) 
    app.add_exception_handler(ExternalAPIException, external_api_handler) 
    app.add_exception_handler(DatabaseException, database_exception_handler) 