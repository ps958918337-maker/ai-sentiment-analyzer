"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# ── Auth Schemas ──────────────────────────────────────────────

class UserCreate(BaseModel):
    """Schema for user registration."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ── Analysis Schemas ──────────────────────────────────────────

class TextAnalysisRequest(BaseModel):
    """Schema for text sentiment analysis."""
    text: str = Field(..., min_length=1, max_length=10000)


class URLAnalysisRequest(BaseModel):
    """Schema for URL sentiment analysis."""
    url: str = Field(..., min_length=5)


class SentimentResult(BaseModel):
    """Detailed sentiment analysis result."""
    # TextBlob
    polarity: float = Field(..., ge=-1, le=1)
    subjectivity: float = Field(..., ge=0, le=1)

    # VADER
    vader_compound: float
    vader_positive: float
    vader_negative: float
    vader_neutral: float

    # Combined
    sentiment_label: str
    confidence: float = Field(..., ge=0, le=1)

    # Input info
    input_text: str
    input_type: str
    source_url: Optional[str] = None


class AnalysisResponse(BaseModel):
    """Full analysis response including ID and timestamps."""
    id: int
    input_text: str
    input_type: str
    source_url: Optional[str] = None
    polarity: float
    subjectivity: float
    vader_compound: float
    vader_positive: float
    vader_negative: float
    vader_neutral: float
    sentiment_label: str
    confidence: float
    created_at: datetime

    class Config:
        from_attributes = True


class BatchAnalysisResponse(BaseModel):
    """Response for CSV batch analysis."""
    total_rows: int
    positive_count: int
    negative_count: int
    neutral_count: int
    average_polarity: float
    average_confidence: float
    results: list[AnalysisResponse]


# ── History Schemas ───────────────────────────────────────────

class HistoryResponse(BaseModel):
    """Paginated history response."""
    total: int
    page: int
    per_page: int
    analyses: list[AnalysisResponse]


class StatsResponse(BaseModel):
    """Aggregate statistics response."""
    total_analyses: int
    positive_count: int
    negative_count: int
    neutral_count: int
    average_polarity: float
    average_confidence: float
    most_common_sentiment: str
    analyses_today: int
    recent_trend: list[dict]  # [{date, positive, negative, neutral}]
