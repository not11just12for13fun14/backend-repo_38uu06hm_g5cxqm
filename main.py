from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from schemas import Portfolio, Testimonial, Inquiry, PricingTier
from database import create_document, get_documents

app = FastAPI(title="ThetaGrid Studio API", version="1.0.0")

# CORS - allow all origins for dev; in production, restrict to your domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "service": "ThetaGrid Studio API"}

@app.get("/test")
async def test_db():
    try:
        docs = await get_documents("portfolio", limit=1)
        return {"ok": True, "connected": True, "sampleCount": len(docs)}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# Portfolio endpoints
@app.post("/portfolio", response_model=dict)
async def add_portfolio(item: Portfolio):
    doc = await create_document("portfolio", item.model_dump())
    return doc

@app.get("/portfolio", response_model=List[dict])
async def list_portfolio(limit: int = 20, tag: Optional[str] = None):
    filter_dict = {"tags": {"$in": [tag]}} if tag else {}
    docs = await get_documents("portfolio", filter_dict, limit)
    return docs

# Testimonials
@app.post("/testimonials", response_model=dict)
async def add_testimonial(item: Testimonial):
    doc = await create_document("testimonial", item.model_dump())
    return doc

@app.get("/testimonials", response_model=List[dict])
async def list_testimonials(limit: int = 20):
    docs = await get_documents("testimonial", {}, limit)
    return docs

# Pricing tiers
@app.post("/pricing", response_model=dict)
async def add_pricing(item: PricingTier):
    doc = await create_document("pricingtier", item.model_dump())
    return doc

@app.get("/pricing", response_model=List[dict])
async def list_pricing():
    docs = await get_documents("pricingtier", {}, 20)
    return docs

# Inquiries
@app.post("/inquiry", response_model=dict)
async def create_inquiry(item: Inquiry):
    doc = await create_document("inquiry", item.model_dump())
    return doc
