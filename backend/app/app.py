from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.routers import customer, project, board, component, componentType, componentMFR
from app.config.settings import settings
from app.routers.limiter import limiter
from app.database import sessionManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await sessionManager.create_tables()
    yield
    if sessionManager._engine is not None:
        await sessionManager.close()

def initialize_app():
    app = FastAPI(
        title=settings.title,
        description=settings.description,
        lifespan=lifespan
    )

    origins = [
        "http://localhost:3000",
        "localhost:3000",
        "http://localhost:5173",
        "localhost:5173"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(customer.router)
    app.include_router(project.router)
    app.include_router(board.router)
    app.include_router(componentType.router)
    app.include_router(component.router)
    app.include_router(componentMFR.router)

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    return app

app = initialize_app()