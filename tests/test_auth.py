"""Tests for authentication functionality."""

import pytest
from tests.conftest import client


def test_register_user():
    """Test user registration."""
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data
    assert data["user"]["username"] == "newuser"


def test_register_duplicate_username():
    """Test registration with duplicate username."""
    # First registration
    client.post(
        "/auth/register",
        json={
            "username": "testuser1",
            "email": "test1@example.com",
            "password": "pass123"
        }
    )
    
    # Second registration with same username
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser1",
            "email": "test2@example.com",
            "password": "pass123"
        }
    )
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]


def test_login_success(test_user):
    """Test successful login."""
    response = client.post(
        "/auth/login",
        json={
            "username": "testuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == "testuser"


def test_login_invalid_password(test_user):
    """Test login with invalid password."""
    response = client.post(
        "/auth/login",
        json={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]


def test_login_nonexistent_user():
    """Test login with non-existent user."""
    response = client.post(
        "/auth/login",
        json={
            "username": "nonexistent",
            "password": "pass123"
        }
    )
    assert response.status_code == 401


def test_get_current_user(auth_headers):
    """Test getting current user info."""
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_get_current_user_without_token():
    """Test accessing protected endpoint without token."""
    response = client.get("/auth/me")
    assert response.status_code == 403
