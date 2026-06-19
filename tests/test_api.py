"""Tests for API endpoints."""

import json
import pytest
from tests.conftest import client


class TestAnalysisEndpoints:
    """Tests for sentiment analysis endpoints."""

    def test_analyze_text_success(self, auth_headers):
        """Test successful text analysis."""
        response = client.post(
            "/analyze/text",
            headers=auth_headers,
            json={"text": "I love this product!"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "sentiment_label" in data
        assert "confidence" in data
        assert data["input_type"] == "text"

    def test_analyze_text_without_auth(self):
        """Test text analysis without authentication."""
        response = client.post(
            "/analyze/text",
            json={"text": "Test"}
        )
        assert response.status_code == 403

    def test_analyze_text_empty(self, auth_headers):
        """Test text analysis with empty text."""
        response = client.post(
            "/analyze/text",
            headers=auth_headers,
            json={"text": ""}
        )
        # Should fail validation or handle gracefully
        assert response.status_code in [422, 400]

    def test_analyze_text_too_long(self, auth_headers):
        """Test text analysis with text exceeding limit."""
        long_text = "a" * 10001
        response = client.post(
            "/analyze/text",
            headers=auth_headers,
            json={"text": long_text}
        )
        assert response.status_code == 422

    def test_analyze_negative_text(self, auth_headers):
        """Test analysis of negative sentiment."""
        response = client.post(
            "/analyze/text",
            headers=auth_headers,
            json={"text": "This is terrible and awful!"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["sentiment_label"] == "negative"
        assert data["polarity"] < 0

    def test_analyze_positive_text(self, auth_headers):
        """Test analysis of positive sentiment."""
        response = client.post(
            "/analyze/text",
            headers=auth_headers,
            json={"text": "Excellent! I love it!"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["sentiment_label"] == "positive"
        assert data["polarity"] > 0

    def test_analysis_stored_in_db(self, auth_headers):
        """Test that analysis is stored in database."""
        # First analysis
        response1 = client.post(
            "/analyze/text",
            headers=auth_headers,
            json={"text": "First analysis"}
        )
        assert response1.status_code == 200
        analysis_id = response1.json()["id"]

        # Retrieve it
        response2 = client.get(
            f"/analysis/{analysis_id}",
            headers=auth_headers
        )
        assert response2.status_code == 200
        assert response2.json()["id"] == analysis_id


class TestHistoryEndpoints:
    """Tests for history and statistics endpoints."""

    def test_get_analysis_history(self, auth_headers):
        """Test retrieving analysis history."""
        # Create some analyses
        for i in range(3):
            client.post(
                "/analyze/text",
                headers=auth_headers,
                json={"text": f"Analysis {i}"}
            )

        response = client.get(
            "/analysis/history",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

    def test_get_analysis_history_with_pagination(self, auth_headers):
        """Test history pagination."""
        # Create 5 analyses
        for i in range(5):
            client.post(
                "/analyze/text",
                headers=auth_headers,
                json={"text": f"Analysis {i}"}
            )

        # Get with limit
        response = client.get(
            "/analysis/history?limit=2",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_analysis_detail(self, auth_headers):
        """Test getting specific analysis."""
        # Create an analysis
        create_response = client.post(
            "/analyze/text",
            headers=auth_headers,
            json={"text": "Test analysis"}
        )
        analysis_id = create_response.json()["id"]

        # Retrieve it
        response = client.get(
            f"/analysis/{analysis_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == analysis_id
        assert data["input_text"] == "Test analysis"

    def test_get_analysis_not_found(self, auth_headers):
        """Test retrieving non-existent analysis."""
        response = client.get(
            "/analysis/99999",
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_get_user_stats(self, auth_headers):
        """Test getting user statistics."""
        # Create multiple analyses
        client.post(
            "/analyze/text",
            headers=auth_headers,
            json={"text": "I love this!"}  # positive
        )
        client.post(
            "/analyze/text",
            headers=auth_headers,
            json={"text": "I hate this!"}  # negative
        )
        client.post(
            "/analyze/text",
            headers=auth_headers,
            json={"text": "Neutral text"}  # neutral
        )

        response = client.get(
            "/analysis/stats/summary",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_analyses"] == 3
        assert "positive_count" in data
        assert "negative_count" in data
        assert "neutral_count" in data
        assert "average_confidence" in data
        assert "average_polarity" in data

    def test_get_user_stats_empty(self, auth_headers):
        """Test getting stats for user with no analyses."""
        response = client.get(
            "/analysis/stats/summary",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_analyses"] == 0


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "SentimentIQ" in data["message"]

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
