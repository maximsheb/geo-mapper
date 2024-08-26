from fastapi import APIRouter

from app.api.endpoints import health, distance, result


api_router = APIRouter()

# non-versioned endpoints
api_router.include_router(distance.router)
api_router.include_router(result.router)
api_router.include_router(health.router)
