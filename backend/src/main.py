from fastapi import FastAPI

from .api import scan, files, search, stats

app = FastAPI(title="Audio Browser API", version="0.0.1")
app.include_router(scan.router, prefix="/scan", tags=["scan"])
app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(search.router, tags=["search"])  # /search
app.include_router(stats.router, tags=["stats"])    # /stats

@app.get("/health")
async def health():
    return {"status": "ok"}
