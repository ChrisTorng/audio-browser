from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from ..services import tree_service, playback_service, waveform_service, annotation_service, scan_service
from fastapi import HTTPException

router = APIRouter()

class FileItem(BaseModel):
    id: str
    name: str
    format: str

class RatingBody(BaseModel):
    stars: int

class DescriptionBody(BaseModel):
    description: str

@router.get('/tree')
async def get_tree(path: Optional[str] = None):
    return await tree_service.get_tree(path)

@router.get('/list', response_model=List[FileItem])
async def list_files():
    items = []
    for f in scan_service.get_scanned_files():
        items.append(FileItem(id=f.id, name=f.display_name, format=f.format))
    return items

@router.get('/{file_id}/waveform')
async def get_waveform(file_id: str):
    try:
        path = await waveform_service.get_or_generate_waveform(file_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="file_id not found")
    return {"file_id": file_id, "waveform_png_path": path}

@router.put('/{file_id}/rating')
async def set_rating(file_id: str, body: RatingBody):
    await annotation_service.set_rating(file_id, body.stars)
    return {"id": file_id, "star_rating": body.stars}

@router.put('/{file_id}/description')
async def set_description(file_id: str, body: DescriptionBody):
    await annotation_service.set_description(file_id, body.description)
    return {"id": file_id, "description": body.description}
