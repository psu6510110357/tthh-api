import pytest
import httpx


@pytest.mark.asyncio
def get_token(client, username, password):
    data = {"username": username, "password": password}
    response = client.post(
        "/auth/token",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return response.json()["accessToken"]


@pytest.mark.asyncio
async def test_read_current_user():
    base_url = "http://localhost:8000"
    # Register and authenticate user
    user_data = {
        "email": "userroute@example.com",
        "username": "userroute",
        "firstName": "User",
        "lastName": "Route",
        "password": "userpass123",
    }
    async with httpx.AsyncClient() as client:
        await client.post(f"{base_url}/register/", json=user_data)
        token_response = await client.post(
            f"{base_url}/auth/token",
            data={"username": user_data["username"], "password": user_data["password"]},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        print(f"Token response: {token_response.json()}")
        token = token_response.json()["accessToken"]
        print(f"Token: {token}")
        # Test /me
        response = await client.get(
            f"{base_url}/user/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        user = response.json()
        assert user["username"] == user_data["username"]
        assert user["email"] == user_data["email"]


@pytest.mark.asyncio
async def test_assign_province_to_user():
    base_url = "http://localhost:8000"
    # Register and authenticate user
    user_data = {
        "email": "assignprovince@example.com",
        "username": "assignprovince",
        "firstName": "Assign",
        "lastName": "Province",
        "password": "assignpass123",
    }
    async with httpx.AsyncClient() as client:
        await client.post(f"{base_url}/register/", json=user_data)
        token_response = await client.post(
            f"{base_url}/auth/token",
            data={"username": user_data["username"], "password": user_data["password"]},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token = token_response.json()["accessToken"]
        # Get a province
        provinces_response = await client.get(
            f"{base_url}/provinces/", headers={"Authorization": f"Bearer {token}"}
        )
        province = provinces_response.json()
        province_id = province["provinces"][0]["id"]
        # Assign province
        response = await client.patch(
            f"{base_url}/user/assign-province",
            json={"provinceId": province_id},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["provinceId"] == str(province_id)


@pytest.mark.asyncio
async def test_get_my_province():
    base_url = "http://localhost:8000"
    # Register and authenticate user
    user_data = {
        "email": "getprovince@example.com",
        "username": "getprovince",
        "firstName": "Get",
        "lastName": "Province",
        "password": "getpass123",
    }
    async with httpx.AsyncClient() as client:
        await client.post(f"{base_url}/register/", json=user_data)
        token_response = await client.post(
            f"{base_url}/auth/token",
            data={"username": user_data["username"], "password": user_data["password"]},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token = token_response.json()["accessToken"]
        # Get a province
        provinces_response = await client.get(
            f"{base_url}/provinces/", headers={"Authorization": f"Bearer {token}"}
        )
        province = provinces_response.json()
        province_id = province["provinces"][0]["id"]
        # Assign province
        await client.patch(
            f"{base_url}/user/assign-province",
            json={"province_id": province_id},
            headers={"Authorization": f"Bearer {token}"},
        )
        # Get my province
        response = await client.get(
            f"{base_url}/user/province",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == province_id
