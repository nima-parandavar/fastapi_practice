from contextlib import asynccontextmanager
from fastapi import FastAPI

from config import config
from services.database import session_manager

from views.user import router as user_router


def init_app(init_db=True):
    lifespan = None

    if init_db:
        session_manager.init(config.DB_CONFIG)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if session_manager._engine is not None:
                await session_manager.close()

    server = FastAPI(title="FastAPI server", lifespan=lifespan, debug=config.DEBUG)
    server.include_router(user_router, prefix="/users", tags=["users"])

    return server


app = init_app()
