"""Core sentiment analysis engine using TextBlob and VADER."""

from dataclasses import dataclass
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER analyzer (singleton)
_vader_analyzer = SentimentIntensityAnalyzer()


@dataclass
class SentimentResult:
    """Structured sentiment analysis result from both engines."""

    # TextBlob scores
    polarity: float          # -1.0 (negative) to 1.0 (positive)
    subjectivity: float      # 0.0 (objective) to 1.0 (subjective)

    # VADER scores
    vader_compound: float    # -1.0 to 1.0
    vader_positive: float    # 0.0 to 1.0
    vader_negative: float    # 0.0 to 1.0
    vader_neutral: float     # 0.0 to 1.0

    # Combined result
    sentiment_label: str     # "positive", "negative", "neutral"
    confidence: float        # 0.0 to 1.0


def analyze_with_textblob(text: str) -> tuple[float, float]:
    """
    Analyze text using TextBlob.

    Returns:
        Tuple of (polarity, subjectivity)
        - polarity: -1.0 to 1.0
        - subjectivity: 0.0 to 1.0
    """
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity


def analyze_with_vader(text: str) -> dict:
    """
    Analyze text using VADER SentimentIntensityAnalyzer.

    Returns:
        Dict with keys: 'compound', 'pos', 'neg', 'neu'
    """
    return _vader_analyzer.polarity_scores(text)


def _determine_sentiment(combined_score: float) -> str:
    """Determine sentiment label from combined score."""
    if combined_score >= 0.05:
        return "positive"
    elif combined_score <= -0.05:
        return "negative"
    else:
        return "neutral"


def _calculate_confidence(polarity: float, vader_compound: float) -> float:
    """
    Calculate confidence based on agreement between TextBlob and VADER.

    Higher confidence when both engines agree on direction and magnitude.
    """
    # Both scores normalized to -1..1 range
    # Agreement: both same sign = higher confidence
    if (polarity >= 0 and vader_compound >= 0) or (polarity <= 0 and vader_compound <= 0):
        agreement_bonus = 0.2
    else:
        agreement_bonus = -0.1

    # Magnitude: stronger signals = higher confidence
    avg_magnitude = (abs(polarity) + abs(vader_compound)) / 2

    confidence = min(1.0, max(0.0, avg_magnitude + agreement_bonus + 0.3))
    return round(confidence, 4)


def analyze_text(text: str) -> SentimentResult:
    """
    Perform full sentiment analysis using both TextBlob and VADER.

    Combines results from both engines for a more robust analysis.

    Args:
        text: The text to analyze

    Returns:
        SentimentResult with all scores and combined label
    """
    if not text or not text.strip():
        return SentimentResult(
            polarity=0.0,
            subjectivity=0.0,
            vader_compound=0.0,
            vader_positive=0.0,
            vader_negative=0.0,
            vader_neutral=1.0,
            sentiment_label="neutral",
            confidence=0.0,
        )

    # TextBlob analysis
    polarity, subjectivity = analyze_with_textblob(text)

    # VADER analysis
    vader_scores = analyze_with_vader(text)
    vader_compound = vader_scores["compound"]
    vader_pos = vader_scores["pos"]
    vader_neg = vader_scores["neg"]
    vader_neu = vader_scores["neu"]

    # Combined score: weighted average (VADER is generally better for social media / short text)
    combined_score = (polarity * 0.4) + (vader_compound * 0.6)

    # Determine label and confidence
    sentiment_label = _determine_sentiment(combined_score)
    confidence = _calculate_confidence(polarity, vader_compound)

    return SentimentResult(
        polarity=round(polarity, 4),
        subjectivity=round(subjectivity, 4),
        vader_compound=round(vader_compound, 4),
        vader_positive=round(vader_pos, 4),
        vader_negative=round(vader_neg, 4),
        vader_neutral=round(vader_neu, 4),
        sentiment_label=sentiment_label,
        confidence=round(confidence, 4),
    )
