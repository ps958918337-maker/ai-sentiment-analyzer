"""Tests for sentiment analysis functionality."""

import pytest
from app.services.sentiment import analyze_text, analyze_with_textblob, analyze_with_vader


class TestSentimentAnalysis:
    """Tests for core sentiment analysis functions."""

    def test_positive_sentiment(self):
        """Test positive sentiment detection."""
        result = analyze_text("I love this! It's amazing and wonderful!")
        assert result.sentiment_label == "positive"
        assert result.polarity > 0
        assert result.vader_compound > 0

    def test_negative_sentiment(self):
        """Test negative sentiment detection."""
        result = analyze_text("This is terrible and awful. I hate it.")
        assert result.sentiment_label == "negative"
        assert result.polarity < 0
        assert result.vader_compound < 0

    def test_neutral_sentiment(self):
        """Test neutral sentiment detection."""
        result = analyze_text("The weather is cloudy today.")
        assert result.sentiment_label == "neutral"

    def test_textblob_analysis(self):
        """Test TextBlob analysis."""
        polarity, subjectivity = analyze_with_textblob("Great product!")
        assert -1 <= polarity <= 1
        assert 0 <= subjectivity <= 1
        assert polarity > 0  # Should be positive

    def test_vader_analysis(self):
        """Test VADER analysis."""
        scores = analyze_with_vader("Excellent work!")
        assert "compound" in scores
        assert "pos" in scores
        assert "neg" in scores
        assert "neu" in scores
        assert -1 <= scores["compound"] <= 1

    def test_confidence_score(self):
        """Test confidence score calculation."""
        result = analyze_text("I absolutely love this product!")
        assert 0 <= result.confidence <= 1

    def test_empty_text(self):
        """Test handling of empty text."""
        result = analyze_text("")
        assert result.polarity == 0.0
        assert result.subjectivity == 0.0
        assert result.sentiment_label == "neutral"

    def test_whitespace_only_text(self):
        """Test handling of whitespace-only text."""
        result = analyze_text("   \n\t  ")
        assert result.polarity == 0.0
        assert result.sentiment_label == "neutral"

    def test_long_text(self):
        """Test analysis of longer text."""
        long_text = "This is great! " * 100
        result = analyze_text(long_text)
        assert result.polarity != 0
        assert result.sentiment_label in ["positive", "negative", "neutral"]

    def test_sarcasm_detection(self):
        """Test handling of sarcastic text."""
        # VADER is known to handle social media language better
        result = analyze_text("Yeah, that's just what I needed!")
        assert isinstance(result.polarity, float)
        assert isinstance(result.vader_compound, float)

    def test_mixed_sentiment(self):
        """Test handling of mixed sentiment."""
        result = analyze_text("I like the product but the service is terrible")
        assert result.confidence > 0
        assert result.sentiment_label in ["positive", "negative", "neutral"]

    def test_result_attributes(self):
        """Test that all required attributes are present."""
        result = analyze_text("Test")
        assert hasattr(result, 'polarity')
        assert hasattr(result, 'subjectivity')
        assert hasattr(result, 'vader_compound')
        assert hasattr(result, 'vader_positive')
        assert hasattr(result, 'vader_negative')
        assert hasattr(result, 'vader_neutral')
        assert hasattr(result, 'sentiment_label')
        assert hasattr(result, 'confidence')

    def test_all_scores_in_range(self):
        """Test that all scores are within expected ranges."""
        result = analyze_text("This is a test sentence for analysis.")
        assert -1 <= result.polarity <= 1
        assert 0 <= result.subjectivity <= 1
        assert -1 <= result.vader_compound <= 1
        assert 0 <= result.vader_positive <= 1
        assert 0 <= result.vader_negative <= 1
        assert 0 <= result.vader_neutral <= 1
        assert 0 <= result.confidence <= 1
