import pytest
from httpx import AsyncClient
import os

BASE_URL = os.getenv("AUTHENTICATION_URL", "http://localhost:8000/authentication")

@pytest.mark.anyio
async def test_register_login_validate_flow():
    async with AsyncClient(base_url=BASE_URL) as client:
        email = "doctortest@email.com"

        register_payload = {
            "name": "John",
            "surname": "Doe",
            "email": email,
            "password": "password123"
        }
        response = await client.post("/register", json=register_payload)
        assert response.status_code == 200, f"Response body: {response.text}"

        login_payload = {
            "email": email,
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
        email = "doctortest2@email.com"

        payload = {
            "name": "John",
            "surname": "Doe",
            "email": email,
            "password": "password123"
        }

        response = await client.post("/register", json=payload)
        assert response.status_code == 200, f"Response body: {response.text}"

        response = await client.post("/register", json=payload)
        assert response.status_code == 400
        assert "Email already registered" in response.text