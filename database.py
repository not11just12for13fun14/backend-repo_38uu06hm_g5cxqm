from typing import Any, Dict, Optional, List
from datetime import datetime
import os
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

MONGO_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(MONGO_URL)
        _db = _client[DB_NAME]
    return _db

async def create_document(collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
    db = await get_db()
    now = datetime.utcnow()
    data_to_insert = {**data, "created_at": now, "updated_at": now}
    res = await db[collection].insert_one(data_to_insert)
    doc = await db[collection].find_one({"_id": res.inserted_id})
    # convert ObjectId and datetimes to strings
    if doc:
        doc["_id"] = str(doc["_id"])  # type: ignore
        if isinstance(doc.get("created_at"), datetime):
            doc["created_at"] = doc["created_at"].isoformat()
        if isinstance(doc.get("updated_at"), datetime):
            doc["updated_at"] = doc["updated_at"].isoformat()
    return doc or {}

async def get_documents(collection: str, filter_dict: Dict[str, Any] | None = None, limit: int = 50) -> List[Dict[str, Any]]:
    db = await get_db()
    cursor = db[collection].find(filter_dict or {}).limit(limit)
    docs: List[Dict[str, Any]] = []
    async for d in cursor:
        d["_id"] = str(d["_id"])  # type: ignore
        if isinstance(d.get("created_at"), datetime):
            d["created_at"] = d["created_at"].isoformat()
        if isinstance(d.get("updated_at"), datetime):
            d["updated_at"] = d["updated_at"].isoformat()
        docs.append(d)
    return docs
