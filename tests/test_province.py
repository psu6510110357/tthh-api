import httpx
import pytest


@pytest.mark.asyncio
async def test_read_all_provinces():
    base_url = "http://localhost:8000"
    # Register and authenticate user
    user_data = {
        "email": "provinceuser@example.com",
        "username": "provinceuser",
        "firstName": "Province",
        "lastName": "User",
        "password": "provincepass123",
    }
    async with httpx.AsyncClient() as client:
        await client.post(f"{base_url}/register/", json=user_data)
        token_response = await client.post(
            f"{base_url}/auth/token",
            data={"username": user_data["username"], "password": user_data["password"]},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token = token_response.json()["accessToken"]
        # Test /provinces/
        response = await client.get(
            f"{base_url}/provinces/",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "provinces" in data
        assert isinstance(data["provinces"], list)
