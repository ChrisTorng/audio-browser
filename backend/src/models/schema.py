# DB schema creation (star ratings & descriptions only for now)
from __future__ import annotations
import aiosqlite
import os

DB_PATH = os.environ.get("DATABASE_URL", "audio.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS audio_annotation (
  id TEXT PRIMARY KEY,
  star_rating INTEGER CHECK(star_rating BETWEEN 0 AND 5),
  description TEXT,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

async def ensure_schema():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(SCHEMA)
        await db.commit()
