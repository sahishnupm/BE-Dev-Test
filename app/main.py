from fastapi import FastAPI
from app.database import init_db
from app.routers import jokes
import asyncio
from app.tasks.joke_tasks import periodic_joke_sync
from app.core.handlers import add_exception_handlers
from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()

app = FastAPI(title="Dad Jokes API")

# Add exception handlers
add_exception_handlers(app)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up application")
    await init_db()
    asyncio.create_task(periodic_joke_sync())
    logger.info("Application startup complete")

app.include_router(jokes.router, tags=["jokes"])

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Dad Jokes API!"} 