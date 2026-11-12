
from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "success": True,
        "message": "TradePulse API is running",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }