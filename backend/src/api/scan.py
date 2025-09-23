from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import os
from ..services import scan_service

router = APIRouter()

class ScanStartResponse(BaseModel):
    accepted: bool

@router.post('/start', response_model=ScanStartResponse, status_code=202)
async def start_scan(background: BackgroundTasks):
    root = os.environ.get('ROOT_AUDIO_DIR', '.')
    background.add_task(scan_service.start_scan, root)
    return ScanStartResponse(accepted=True)

@router.get('/status')
async def scan_status():
    return await scan_service.get_status()
