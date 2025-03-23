from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/health",
    tags=["health"]
)

@router.get("/liveness")
async def liveness():
    return {"status": "alive"}

@router.get("/readiness")
async def readiness():
    return {"status": "ready"}

@router.get("/metrics")
async def metrics():
    return {
        "total_requests": 0,
        "active_connections": 0,
        "error_rate": 0.0
    }
