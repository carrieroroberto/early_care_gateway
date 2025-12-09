import pytest
from httpx import AsyncClient
import os

BASE_AUTH_URL = os.getenv("AUTHENTICATION_URL", "http://localhost:8000/authentication")
BASE_DATA_URL = os.getenv("DATA_PROCESSING_URL", "http://localhost:8004/data_processing")
BASE_XAI_URL = os.getenv("EXPLAINABLE_AI_URL", "http://localhost:8003/explainable_ai")

@pytest.mark.anyio
async def test_register_login_analyse_flow():
    async with AsyncClient(base_url=BASE_AUTH_URL) as auth_client, AsyncClient(base_url=BASE_DATA_URL) as data_client, AsyncClient(base_url=BASE_XAI_URL) as xai_client:
        email = "gatewaytest2@email.com"
        register_payload = {
            "name": "Alice",
            "surname": "Smith",
            "email": email,
            "password": "password123"
        }
        response = await auth_client.post("/register", json=register_payload)
        assert response.status_code == 200, f"Response body: {response.text}"
        
        login_payload = {
            "email": email,
            "password": "password123"
        }
        response = await auth_client.post("/login", json=login_payload)
        assert response.status_code == 200, f"Response body: {response.text}"
        login_data = response.json()
        assert "jwt_token" in login_data and login_data["jwt_token"] != ""

        process_payload = {
            "strategy": "numeric",
            "raw_data": "[55, 140, 250, 150, 1.5, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0]"
        }
        response = await data_client.post("/process", json=process_payload)
        assert response.status_code == 200, f"Response body: {response.text}"
        processed_data_id = response.json().get("processed_data_id")
        assert processed_data_id is not None

        response = await xai_client.post("/analyse", json={
            "doctor_id": 1,
            "patient_hashed_cf": "HASHED123",
            "strategy": process_payload["strategy"],
            "processed_data_id": processed_data_id
        })
        
        assert response.status_code == 200, f"Response body: {response.text}"
        report = response.json().get("report")
        assert report is not None
        assert report["processed_data_id"] == processed_data_id

        response = await xai_client.get(f"/reports/1")
        assert response.status_code == 200, f"Response body: {response.text}"
        reports = response.json().get("reports", [])
        assert any(r["processed_data_id"] == processed_data_id for r in reports)