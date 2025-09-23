import os
import asyncio
import tempfile
import shutil
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
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

@pytest.fixture()
def client():
    return TestClient(app)
