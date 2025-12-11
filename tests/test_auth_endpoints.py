import pytest
from httpx import AsyncClient
import os
import uuid

# Base URL for the Authentication microservice.
# Defaults to localhost if environment variable is not set.
BASE_URL = os.getenv("AUTHENTICATION_URL", "http://localhost:8000/authentication")

# Generate a unique email for testing to avoid conflicts with existing users
EMAIL = f"test_{uuid.uuid4()}@email.com"

# Test 1: Full register → login → validate flow
@pytest.mark.anyio
async def test_register_login_validate_flow():
    # Use asynchronous HTTP client
    async with AsyncClient(base_url=BASE_URL) as client:
        # Registration payload
        register_payload = {
            "name": "John",
            "surname": "Doe",
            "email": EMAIL,          # Unique email
            "password": "password123"
        }
        # Send POST request to /register endpoint
        response = await client.post("/register", json=register_payload)
        # Ensure registration succeeded
        assert response.status_code == 200, f"Response body: {response.text}"

        # Login payload using same credentials
        login_payload = {
            "email": EMAIL,
            "password": "password123"
        }
        # Send POST request to /login endpoint
        response = await client.post("/login", json=login_payload)
        # Ensure login succeeded
        assert response.status_code == 200, f"Response body: {response.text}"
        data = response.json()

        # Validate response contains a JWT token and success message
        assert "jwt_token" in data
        assert data["jwt_token"] != ""
        assert data["message"] == "Doctor logged in successfully"

# Test 2: Attempt to register with a duplicate email
@pytest.mark.anyio
async def test_register_duplicate_email():
    async with AsyncClient(base_url=BASE_URL) as client:
        payload = {
            "name": "John",
            "surname": "Doe",
            "email": EMAIL,          # Same email as previous test
            "password": "password123"
        }

        # Attempt to register again with the same email
        response = await client.post("/register", json=payload)
        # Expect HTTP 400 Bad Request
        assert response.status_code == 400
        # Ensure response contains error message about duplicate email
        assert "Email already registered" in response.text
