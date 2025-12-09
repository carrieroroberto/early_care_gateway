import pytest
from httpx import AsyncClient
import os
import uuid

BASE_URL = os.getenv("AUTHENTICATION_URL", "http://localhost:8000/authentication")
EMAIL = f"test_{uuid.uuid4()}@email.com"

@pytest.mark.anyio
async def test_register_login_validate_flow():
    async with AsyncClient(base_url=BASE_URL) as client:
        register_payload = {
            "name": "John",
            "surname": "Doe",
            "email": EMAIL,
            "password": "password123"
        }
        response = await client.post("/register", json=register_payload)
        assert response.status_code == 200, f"Response body: {response.text}"

        login_payload = {
            "email": EMAIL,
            "password": "password123"
        }
        response = await client.post("/login", json=login_payload)
        assert response.status_code == 200, f"Response body: {response.text}"
        data = response.json()

        assert "jwt_token" in data
        assert data["jwt_token"] != ""
        assert data["message"] == "Doctor logged in successfully"

@pytest.mark.anyio
async def test_register_duplicate_email():
    async with AsyncClient(base_url=BASE_URL) as client:
        payload = {
            "name": "John",
            "surname": "Doe",
            "email": EMAIL,
            "password": "password123"
        }

        response = await client.post("/register", json=payload)
        assert response.status_code == 400
        assert "Email already registered" in response.text