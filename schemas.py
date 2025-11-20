from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List

# Each model corresponds to a Mongo collection with the lowercase class name
# e.g., class Portfolio -> collection "portfolio"

class Portfolio(BaseModel):
    title: str = Field(..., min_length=2, max_length=120)
    client: str = Field(..., min_length=2, max_length=120)
    sector: Optional[str] = None
    summary: str = Field(..., min_length=10, max_length=800)
    case_study: Optional[str] = None
    image: Optional[HttpUrl] = None
    url: Optional[HttpUrl] = None
    tags: List[str] = []

class Testimonial(BaseModel):
    client: str
    role: Optional[str] = None
    logo: Optional[HttpUrl] = None
    quote: str

class Inquiry(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    message: str
    source: Optional[str] = None

class PricingTier(BaseModel):
    name: str
    price_eur: float
    features: List[str]
    cta_label: str = "Get Started"
