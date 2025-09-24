"""FastAPI application entrypoint for the MVP backend."""

from fastapi import FastAPI

from .routers import health, root


def create_app() -> FastAPI:
    """Instantiate and configure the FastAPI application."""

    app = FastAPI(
        title="Gakumas Share Backend",
        version="0.1.0",
    )

    app.include_router(root.router)
    app.include_router(health.router)

    return app


app = create_app()
