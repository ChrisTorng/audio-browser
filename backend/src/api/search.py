from fastapi import APIRouter
from typing import Optional
from ..services import search_service, annotation_service

router = APIRouter()

@router.get('/search')
async def search(q: str = '', minStars: Optional[int] = None):
    # Build annotation map
    # For simplicity fetch per file (could optimize)
    annotations = {}
    # (In future we can fetch all annotations with one query)
    results = search_service.search(q, min_stars=minStars, annotations=annotations)
    return {"query": q, "results": [r.dict() for r in results]}
