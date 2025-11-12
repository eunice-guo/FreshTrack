"""
Tests for user management endpoints
"""
import pytest


class TestUserEndpoints:
    """Test user-related API endpoints"""

    def test_register_user(self, client):
        """Test user registration"""
        response = client.post(
            "/api/users/register",
            json={
                "email": "newuser@test.com",
                "username": "New Test User"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@test.com"
        assert data["username"] == "New Test User"
        assert "id" in data
        assert "created_at" in data

    def test_register_user_duplicate_email(self, client, test_user):
        """Test registering with duplicate email"""
        response = client.post(
            "/api/users/register",
            json={
                "email": test_user.email,
                "username": "Duplicate User"
            }
        )

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_register_user_missing_email(self, client):
        """Test registration without email"""
        response = client.post(
            "/api/users/register",
            json={
                "username": "No Email User"
            }
        )

        assert response.status_code == 422  # Validation error

    def test_get_user_by_id(self, client, test_user):
        """Test getting user by ID"""
        response = client.get(f"/api/users/{test_user.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["email"] == test_user.email
        assert data["username"] == test_user.username

    def test_get_user_by_id_not_found(self, client):
        """Test getting non-existent user"""
        response = client.get("/api/users/99999")

        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    def test_get_user_by_email(self, client, test_user):
        """Test getting user by email"""
        response = client.get(f"/api/users/email/{test_user.email}")

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["id"] == test_user.id

    def test_get_user_by_email_not_found(self, client):
        """Test getting user with non-existent email"""
        response = client.get("/api/users/email/nonexistent@test.com")

        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    def test_root_endpoint(self, client):
        """Test root health check endpoint"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "FreshTrack API is running!"
        assert "version" in data
