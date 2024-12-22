from app.routers import jokes

def include_routers(app):
    app.include_router(jokes.router, tags=["jokes"])