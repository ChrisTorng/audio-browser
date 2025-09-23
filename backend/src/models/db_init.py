import os
import aiosqlite

DB_PATH = os.environ.get("DATABASE_URL", "audio.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS audio_annotation (
  id TEXT PRIMARY KEY,
  star_rating INTEGER,
  description TEXT,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(SCHEMA)
        await db.commit()
