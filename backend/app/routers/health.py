"""Health check router for uptime monitoring."""

from datetime import datetime

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", summary="Health check")
async def health_check() -> dict[str, str]:
    """Provide a lightweight readiness response."""

    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
