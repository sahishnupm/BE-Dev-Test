from fastapi import FastAPI
from app.database import init_db
import asyncio
from app.tasks.joke_tasks import periodic_joke_sync
from app.core.handlers import add_exception_handlers
from app.core.logging import setup_logging
from app.core.routers import include_routers

# Setup logging
logger = setup_logging()

app = FastAPI(title="Dad Jokes API")

add_exception_handlers(app)
include_routers(app)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up application")
    await init_db()
    asyncio.create_task(periodic_joke_sync())
    logger.info("Application startup complete")


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Dad Jokes API!"} 