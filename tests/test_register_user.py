#!/usr/bin/env python3
"""
Script to create a test user for authentication testing
"""
import pytest
import httpx


@pytest.mark.asyncio
async def test_register_user():
    base_url = "http://localhost:8000"

    user_data = {
        "email": "test@example.com",
        "username": "string",
        "firstName": "Test",
        "lastName": "User",
        "password": "string",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/register/",  # Adjust path if needed
            json=user_data,
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code in (201, 409)
        if response.status_code == 201:
            user_response = response.json()
            assert user_response["username"] == user_data["username"]
            assert user_response["email"] == user_data["email"]
        elif response.status_code == 409:
            error_data = response.json()
            assert "already exists" in error_data.get("detail", "")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "missing_field", ["email", "username", "firstName", "lastName", "password"]
)
async def test_register_user_missing_field(missing_field):
    base_url = "http://localhost:8000"
    user_data = {
        "email": "test2@example.com",
        "username": "string2",
        "firstName": "Test2",
        "lastName": "User2",
        "password": "string2",
    }
    user_data.pop(missing_field)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/register/",
            json=user_data,
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_user_invalid_email():
    base_url = "http://localhost:8000"
    user_data = {
        "email": "not-an-email",
        "username": "string3",
        "firstName": "Test3",
        "lastName": "User3",
        "password": "string3",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/register/",
            json=user_data,
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_user_unique_constraints():
    base_url = "http://localhost:8000"
    user_data1 = {
        "email": "unique@example.com",
        "username": "uniqueuser",
        "firstName": "Unique",
        "lastName": "User",
        "password": "string",
    }
    user_data2 = {
        "email": "unique@example.com",
        "username": "anotheruser",
        "firstName": "Another",
        "lastName": "User",
        "password": "string",
    }
    user_data3 = {
        "email": "another@example.com",
        "username": "uniqueuser",
        "firstName": "Another",
        "lastName": "User",
        "password": "string",
    }
    async with httpx.AsyncClient() as client:
        # Register first user
        await client.post(
            f"{base_url}/register/",
            json=user_data1,
            headers={"Content-Type": "application/json"},
        )
        # Try to register with same email, different username
        response2 = await client.post(
            f"{base_url}/register/",
            json=user_data2,
            headers={"Content-Type": "application/json"},
        )
        assert response2.status_code == 409
        # Try to register with same username, different email
        response3 = await client.post(
            f"{base_url}/register/",
            json=user_data3,
            headers={"Content-Type": "application/json"},
        )
        assert response3.status_code == 409
