"""SQLAlchemy ORM models."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """User account model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship to analyses
    analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")


class Analysis(Base):
    """Sentiment analysis result model."""

    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Input data
    input_text = Column(Text, nullable=False)
    input_type = Column(String(20), nullable=False, default="text")  # text, url, csv
    source_url = Column(String(500), nullable=True)

    # TextBlob results
    polarity = Column(Float, nullable=False, default=0.0)
    subjectivity = Column(Float, nullable=False, default=0.0)

    # VADER results
    vader_compound = Column(Float, nullable=False, default=0.0)
    vader_positive = Column(Float, nullable=False, default=0.0)
    vader_negative = Column(Float, nullable=False, default=0.0)
    vader_neutral = Column(Float, nullable=False, default=0.0)

    # Combined results
    sentiment_label = Column(String(20), nullable=False)  # positive, negative, neutral
    confidence = Column(Float, nullable=False, default=0.0)

    # Metadata
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship
    user = relationship("User", back_populates="analyses")
