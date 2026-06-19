"""
SentimentIQ - FastAPI Application
Main entry point with all API routes for sentiment analysis.
"""

from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pathlib import Path

from app.database import get_db, init_db
from app.dependencies import get_current_user
from app.models import User, Analysis
from app.schemas import (
    UserCreate, UserLogin, UserResponse, Token,
    TextAnalysisRequest, URLAnalysisRequest, AnalysisResponse, BatchAnalysisResponse
)
from app.auth import hash_password, create_access_token
from app.services.sentiment import analyze_text
from app.services.scraper import extract_text_from_url, ScraperError
from app.services.csv_processor import process_csv, CSVProcessorError

# ── Application Setup ──────────────────────────────────────────

app = FastAPI(
    title="SentimentIQ API",
    description="AI-powered sentiment analysis platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Mount static files
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Initialize database tables on startup
@app.on_event("startup")
def startup_event():
    """Initialize database on application startup."""
    init_db()


# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health Check ──────────────────────────────────────────────

@app.get("/", tags=["Health"])
async def root():
    """Serve the web interface."""
    static_dir = Path(__file__).parent.parent / "static" / "index.html"
    if static_dir.exists():
        return FileResponse(str(static_dir))
    return {
        "message": "SentimentIQ API is running",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check."""
    return {"status": "healthy"}


# ── Authentication Routes ──────────────────────────────────────

@app.post("/auth/register", response_model=Token, tags=["Authentication"])
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.

    **Request body:**
    - username: Unique username (3-50 characters)
    - email: Valid email address
    - password: Password (minimum 6 characters)
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate access token
    access_token = create_access_token(data={"sub": new_user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "created_at": new_user.created_at
        }
    }


@app.post("/auth/login", response_model=Token, tags=["Authentication"])
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login with username and password.

    **Request body:**
    - username: Registered username
    - password: Account password

    **Returns:** JWT access token
    """
    user = db.query(User).filter(User.username == credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    from app.auth import verify_password
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_access_token(data={"sub": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at
        }
    }


@app.get("/auth/me", response_model=UserResponse, tags=["Authentication"])
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information."""
    return current_user


# ── Sentiment Analysis Routes ──────────────────────────────────

@app.post("/analyze/text", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_text_endpoint(
    request: TextAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze sentiment of provided text.

    **Request body:**
    - text: Text to analyze (1-10000 characters)

    **Returns:** Detailed sentiment analysis with TextBlob and VADER scores
    """
    # Perform sentiment analysis
    result = analyze_text(request.text)

    # Store in database
    analysis = Analysis(
        user_id=current_user.id,
        input_text=request.text,
        input_type="text",
        polarity=result.polarity,
        subjectivity=result.subjectivity,
        vader_compound=result.vader_compound,
        vader_positive=result.vader_positive,
        vader_negative=result.vader_negative,
        vader_neutral=result.vader_neutral,
        sentiment_label=result.sentiment_label,
        confidence=result.confidence
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis


@app.post("/analyze/url", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_url_endpoint(
    request: URLAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze sentiment of text extracted from a URL.

    **Request body:**
    - url: URL to scrape and analyze

    **Returns:** Sentiment analysis of extracted webpage content

    **Errors:**
    - 400: URL cannot be accessed or parsed
    """
    try:
        # Extract text from URL
        extracted_text = extract_text_from_url(request.url)
    except ScraperError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    # Perform sentiment analysis
    result = analyze_text(extracted_text)

    # Store in database
    analysis = Analysis(
        user_id=current_user.id,
        input_text=extracted_text,
        input_type="url",
        source_url=request.url,
        polarity=result.polarity,
        subjectivity=result.subjectivity,
        vader_compound=result.vader_compound,
        vader_positive=result.vader_positive,
        vader_negative=result.vader_negative,
        vader_neutral=result.vader_neutral,
        sentiment_label=result.sentiment_label,
        confidence=result.confidence
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis


@app.post("/analyze/csv", response_model=BatchAnalysisResponse, tags=["Analysis"])
async def analyze_csv_batch(
    file: UploadFile = File(..., description="CSV file with text column"),
    text_column: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Batch analyze multiple texts from a CSV file.

    **Form parameters:**
    - file: CSV file to upload
    - text_column: Optional column name containing text (auto-detects if not provided)

    **Returns:** Summary statistics of batch analysis

    **CSV Format:** Should contain a column with text data. Supported column names:
    text, content, review, comment, message, body, feedback, description

    **Errors:**
    - 400: CSV file is invalid or cannot be parsed
    """
    try:
        # Read file content
        file_content = await file.read()
        results = process_csv(file_content, text_column)
    except CSVProcessorError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    # Count sentiments
    positive_count = sum(1 for r in results if r["sentiment_label"] == "positive")
    negative_count = sum(1 for r in results if r["sentiment_label"] == "negative")
    neutral_count = sum(1 for r in results if r["sentiment_label"] == "neutral")

    # Store results in database
    for result in results:
        analysis = Analysis(
            user_id=current_user.id,
            input_text=result["text"],
            input_type="csv",
            polarity=result["polarity"],
            subjectivity=result["subjectivity"],
            vader_compound=result["vader_compound"],
            vader_positive=result["vader_positive"],
            vader_negative=result["vader_negative"],
            vader_neutral=result["vader_neutral"],
            sentiment_label=result["sentiment_label"],
            confidence=result["confidence"]
        )
        db.add(analysis)

    db.commit()

    return {
        "total_rows": len(results),
        "positive_count": positive_count,
        "negative_count": negative_count,
        "neutral_count": neutral_count
    }


# ── History & Statistics Routes ────────────────────────────────

@app.get("/analysis/history", tags=["History"])
async def get_analysis_history(
    limit: int = 50,
    skip: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's analysis history.

    **Query parameters:**
    - limit: Number of records to return (default: 50, max: 100)
    - skip: Number of records to skip (pagination)

    **Returns:** List of past analyses with all details
    """
    limit = min(limit, 100)  # Limit to prevent excessive queries

    analyses = db.query(Analysis).filter(
        Analysis.user_id == current_user.id
    ).order_by(
        Analysis.created_at.desc()
    ).offset(skip).limit(limit).all()

    return analyses


@app.get("/analysis/{analysis_id}", response_model=AnalysisResponse, tags=["History"])
async def get_analysis_detail(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get details of a specific analysis.

    **Returns:** Complete analysis record
    """
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )

    return analysis


@app.get("/analysis/stats/summary", tags=["Statistics"])
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get sentiment statistics for current user.

    **Returns:**
    - total_analyses: Total number of analyses
    - positive_count: Number of positive sentiments
    - negative_count: Number of negative sentiments
    - neutral_count: Number of neutral sentiments
    - average_confidence: Average confidence score
    - average_polarity: Average polarity score
    """
    analyses = db.query(Analysis).filter(Analysis.user_id == current_user.id).all()

    if not analyses:
        return {
            "total_analyses": 0,
            "positive_count": 0,
            "negative_count": 0,
            "neutral_count": 0,
            "average_confidence": 0.0,
            "average_polarity": 0.0
        }

    positive = sum(1 for a in analyses if a.sentiment_label == "positive")
    negative = sum(1 for a in analyses if a.sentiment_label == "negative")
    neutral = sum(1 for a in analyses if a.sentiment_label == "neutral")

    avg_confidence = sum(a.confidence for a in analyses) / len(analyses) if analyses else 0
    avg_polarity = sum(a.polarity for a in analyses) / len(analyses) if analyses else 0

    return {
        "total_analyses": len(analyses),
        "positive_count": positive,
        "negative_count": negative,
        "neutral_count": neutral,
        "average_confidence": round(avg_confidence, 4),
        "average_polarity": round(avg_polarity, 4)
    }


# ── Error Handlers ─────────────────────────────────────────────

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
