from fastapi import FastAPI
from contextlib import asynccontextmanager
from .api import scan, files, search, stats
from .models.schema import ensure_schema


@asynccontextmanager
async def lifespan(app: FastAPI):  # FastAPI lifespan context replaces deprecated on_event
    await ensure_schema()
    yield


app = FastAPI(title="Audio Browser API", version="0.0.1", lifespan=lifespan)

app.include_router(scan.router, prefix="/scan", tags=["scan"])
app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(search.router, tags=["search"])  # /search
app.include_router(stats.router, tags=["stats"])    # /stats


@app.get("/health")
async def health():
    return {"status": "ok"}
