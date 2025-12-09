import pytest
from httpx import AsyncClient
import os

BASE_URL = os.getenv("AUDIT_URL", "http://localhost:8001/audit")

@pytest.mark.anyio
async def test_create_log():
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

        response = await client.post("/log", json=payload)

        assert response.status_code == 200, f"Body: {response.text}"

        data = response.json()
        assert "log_id" in data
        assert "created_at" in data
        assert data["log_id"] is not None

@pytest.mark.anyio
async def test_get_logs_with_filters():
    async with AsyncClient(base_url=BASE_URL) as client:
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

        filter_payload = {
            "service": "authentication",
            "doctor_id": 2,
        }

        response = await client.get(f"/logs?service={filter_payload['service']}&doctor_id={filter_payload['doctor_id']}")

        assert response.status_code == 200, f"Body: {response.text}"

        data = response.json()

        assert "logs" in data
        assert isinstance(data["logs"], list)
        assert len(data["logs"]) > 0

        log = data["logs"][0]
        assert log["service"] == "authentication"
        assert log["doctor_id"] == 2

@pytest.mark.anyio
async def test_get_logs_no_results():
    async with AsyncClient(base_url=BASE_URL) as client:
        filter_payload = {
            "service": "something_that_does_not_exist",
        }

        response = await client.get(f"/logs?service={filter_payload['service']}")

        assert response.status_code == 200

        data = response.json()

        assert data["message"] == "No logs retrieved"
        assert isinstance(data["logs"], list)
        assert len(data["logs"]) == 0