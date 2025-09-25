"""FastAPI application entrypoint for the MVP backend."""

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from supertokens_python.framework.fastapi import get_middleware

from .config import get_settings
from .oauth import configure_oauth
from .routers import auth, health, root
from .supertokens import init_supertokens


def create_app() -> FastAPI:
    """Instantiate and configure the FastAPI application."""

    settings = get_settings()
    configure_oauth(settings)
    init_supertokens(settings)

    app = FastAPI(
        title="Gakumas Share Backend",
        version="0.1.0",
    )

    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.session_secret_key,
        https_only=settings.cookie_secure,
        same_site="lax",
    )
    app.add_middleware(get_middleware())

    app.include_router(root.router)
    app.include_router(health.router)
    app.include_router(auth.router)

    return app


app = create_app()
