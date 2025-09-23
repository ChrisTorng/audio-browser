from fastapi import APIRouter
from ..services import stats_service

router = APIRouter()

@router.get('/stats')
async def get_stats():
    return stats_service.compute_stats()
