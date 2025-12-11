import pytest
from httpx import AsyncClient
import os

# Base URL for the Audit microservice.
# If the environment variable AUDIT_URL is not set, defaults to localhost.
BASE_URL = os.getenv("AUDIT_URL", "http://localhost:8001/audit")

# Test 1: Create a log entry
@pytest.mark.anyio
async def test_create_log():
    # Use an asynchronous HTTP client for the Audit API
    async with AsyncClient(base_url=BASE_URL) as client:
        payload = {
            "service": "authentication",
            "event": "login_success",
            "description": "User logged in",
            "doctor_id": 1,
            "patient_hashed_cf": None,
            "report_id": None,
            "data_id": None
        }

        # Send POST request to create a new log entry
        response = await client.post("/log", json=payload)

        # Check that the response status code is 200 (OK)
        assert response.status_code == 200, f"Body: {response.text}"

        # Parse response JSON
        data = response.json()
        # Ensure response contains 'log_id' and 'created_at'
        assert "log_id" in data
        assert "created_at" in data
        assert data["log_id"] is not None

# Test 2: Retrieve logs with filters
@pytest.mark.anyio
async def test_get_logs_with_filters():
    async with AsyncClient(base_url=BASE_URL) as client:
        # First, create a log entry to ensure there is data
        create_payload = {
            "service": "authentication",
            "event": "register_success",
            "description": "Doctor registered successfully",
            "doctor_id": 2,
            "patient_hashed_cf": None,
            "report_id": None,
            "data_id": None
        }

        create_resp = await client.post("/log", json=create_payload)
        assert create_resp.status_code == 200

        # Prepare filter payload to retrieve logs for a specific service and doctor
        filter_payload = {
            "service": "authentication",
            "doctor_id": 2,
        }

        # Send GET request with query parameters for filtering
        response = await client.get(
            f"/logs?service={filter_payload['service']}&doctor_id={filter_payload['doctor_id']}"
        )

        # Check that request succeeded
        assert response.status_code == 200, f"Body: {response.text}"

        data = response.json()
        # Ensure the response contains a 'logs' list
        assert "logs" in data
        assert isinstance(data["logs"], list)
        assert len(data["logs"]) > 0

        # Check that the first log matches the filter
        log = data["logs"][0]
        assert log["service"] == "authentication"
        assert log["doctor_id"] == 2

# Test 3: Retrieve logs with no matching results
@pytest.mark.anyio
async def test_get_logs_no_results():
    async with AsyncClient(base_url=BASE_URL) as client:
        filter_payload = {
            "service": "something_that_does_not_exist",
        }

        # Send GET request with a filter that matches nothing
        response = await client.get(f"/logs?service={filter_payload['service']}")

        # Expect successful response even if no results
        assert response.status_code == 200

        data = response.json()
        # Ensure the response contains a message and an empty logs list
        assert data["message"] == "No logs retrieved"
        assert isinstance(data["logs"], list)
        assert len(data["logs"]) == 0
