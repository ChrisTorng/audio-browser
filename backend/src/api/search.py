from fastapi import APIRouter
from typing import Optional
from ..services import search_service

router = APIRouter()


@router.get('/search')
async def search(q: str = '', minStars: Optional[int] = None):
    annotations = {}  # future optimization: bulk fetch
    results = search_service.search(q, min_stars=minStars, annotations=annotations)
    return {"query": q, "results": [r.model_dump() for r in results]}
