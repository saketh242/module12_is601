import pytest


class TestAuthenticationFlow:
    def test_register_duplicate_username(self, client, test_user):
        response = client.post(
            "/auth/register",
            json={
                "username": "testuser",
                "password": "NewPass123!",
                "confirm_password": "NewPass123!",
                "first_name": "Another",
                "last_name": "User",
                "email": "another@example.com"
            }
        )
        assert response.status_code == 400

    def test_login_invalid_password(self, client, test_user):
        response = client.post(
            "/auth/login",
            json={"username": "testuser", "password": "WrongPass123!"}
        )
        assert response.status_code == 401


class TestPageRoutes:
    def test_home_page(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "<!DOCTYPE html>" in response.text

    def test_login_page(self, client):
        response = client.get("/login")
        assert response.status_code == 200

    def test_register_page(self, client):
        response = client.get("/register")
        assert response.status_code == 200

    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
