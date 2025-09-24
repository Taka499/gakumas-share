"""Root router exposing a simple welcome message."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary="Service welcome endpoint")
async def read_root() -> dict[str, str]:
    """Return a simple payload indicating the API is reachable."""

    return {"message": "Gakumas Share API"}
