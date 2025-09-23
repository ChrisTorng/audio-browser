from __future__ import annotations
import aiosqlite
import os
from typing import Optional

DB_PATH = os.environ.get("DATABASE_URL", "audio.db")

async def set_rating(file_id: str, stars: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO audio_annotation(id, star_rating) VALUES(?, ?) ON CONFLICT(id) DO UPDATE SET star_rating=excluded.star_rating, updated_at=CURRENT_TIMESTAMP", (file_id, stars))
        await db.commit()

async def set_description(file_id: str, description: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO audio_annotation(id, description) VALUES(?, ?) ON CONFLICT(id) DO UPDATE SET description=excluded.description, updated_at=CURRENT_TIMESTAMP", (file_id, description))
        await db.commit()

async def get_annotation(file_id: str) -> Optional[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT star_rating, description FROM audio_annotation WHERE id=?", (file_id,))
        row = await cur.fetchone()
        if not row:
            return None
        return {"star_rating": row[0], "description": row[1]}
