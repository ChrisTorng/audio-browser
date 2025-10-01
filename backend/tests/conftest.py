import os
import asyncio
import tempfile
import shutil
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path as _P

# Ensure project root is on sys.path so 'backend' package resolves when running pytest from repo root
ROOT = _P(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.src.main import app

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop

@pytest.fixture(scope="session")
def temp_audio_dir():
    d = tempfile.mkdtemp(prefix="audio-browser-")
    try:
        yield Path(d)
    finally:
        shutil.rmtree(d, ignore_errors=True)

@pytest.fixture(scope="session", autouse=True)
def _env_setup(temp_audio_dir):
    os.environ.setdefault("ROOT_AUDIO_DIR", str(temp_audio_dir))
    os.environ.setdefault("DATABASE_URL", "test_audio.db")
    # 建立測試音檔（極小 placeholder），供掃描與波形生成測試
    samples = ["kick.mp3", "snare.wav"]
    for name in samples:
        p = temp_audio_dir / name
        if not p.exists():
            # 寫入極小內容（非有效音訊，但用於存在測試即可）
            p.write_bytes(b"TEST")

@pytest.fixture()
def client():
    return TestClient(app)
