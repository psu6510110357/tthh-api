import pytest
import httpx


@pytest.mark.asyncio
async def test_authentication_success():
    base_url = "http://localhost:8000"
    # First, register a user (if not already exists)
    user_data = {
        "email": "authuser@example.com",
        "username": "authuser",
        "firstName": "Auth",
        "lastName": "User",
        "password": "testpass123",
    }
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{base_url}/register/",
            json=user_data,
            headers={"Content-Type": "application/json"},
        )
        # Now authenticate
        data = {
            "username": user_data["username"],
            "password": user_data["password"],
        }
        response = await client.post(
            f"{base_url}/auth/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == 200
        token_response = response.json()
        assert "accessToken" in token_response
        assert token_response["tokenType"].lower() == "bearer"


@pytest.mark.asyncio
async def test_authentication_invalid_password():
    base_url = "http://localhost:8000"
    data = {
        "username": "authuser",
        "password": "wrongpassword",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/auth/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == 401
        error = response.json()
        assert "Incorrect username or password" in error.get("detail", "")


@pytest.mark.asyncio
async def test_authentication_nonexistent_user():
    base_url = "http://localhost:8000"
    data = {
        "username": "nonexistentuser",
        "password": "irrelevant",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/auth/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == 401
        error = response.json()
        assert "Incorrect username or password" in error.get("detail", "")
