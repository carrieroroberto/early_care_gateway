import pytest
from httpx import AsyncClient
import os
import uuid

# Base URLs for different microservices
BASE_AUTH_URL = os.getenv("AUTHENTICATION_URL", "http://localhost:8000/authentication")
BASE_DATA_URL = os.getenv("DATA_PROCESSING_URL", "http://localhost:8004/data_processing")
BASE_XAI_URL = os.getenv("EXPLAINABLE_AI_URL", "http://localhost:8003/explainable_ai")

# Generate a unique email for testing
EMAIL = f"test_{uuid.uuid4()}@email.com"

# Test: Full end-to-end flow
# 1) Register a doctor
# 2) Login
# 3) Process numeric data
# 4) Analyse data via XAI service
# 5) Retrieve reports
@pytest.mark.anyio
async def test_register_login_analyse_flow():
    # Create async HTTP clients for auth, data processing, and XAI services
    async with AsyncClient(base_url=BASE_AUTH_URL) as auth_client, \
               AsyncClient(base_url=BASE_DATA_URL) as data_client, \
               AsyncClient(base_url=BASE_XAI_URL) as xai_client:

        # --- Step 1: Register a new doctor ---
        register_payload = {
            "name": "Alice",
            "surname": "Smith",
            "email": EMAIL,       # Unique test email
            "password": "password123"
        }
        response = await auth_client.post("/register", json=register_payload)
        # Ensure registration succeeded
        assert response.status_code == 200, f"Response body: {response.text}"
        
        # --- Step 2: Login ---
        login_payload = {
            "email": EMAIL,
            "password": "password123"
        }
        response = await auth_client.post("/login", json=login_payload)
        assert response.status_code == 200, f"Response body: {response.text}"
        login_data = response.json()
        # Verify JWT token returned
        assert "jwt_token" in login_data and login_data["jwt_token"] != ""

        # --- Step 3: Process numeric data ---
        process_payload = {
            "strategy": "numeric",
            "raw_data": "[55, 140, 250, 150, 1.5, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0]"
        }
        response = await data_client.post("/process", json=process_payload)
        assert response.status_code == 200, f"Response body: {response.text}"
        processed_data_id = response.json().get("processed_data_id")
        # Ensure the processed data ID is returned
        assert processed_data_id is not None

        # --- Step 4: Analyse data with XAI service ---
        response = await xai_client.post("/analyse", json={
            "doctor_id": 1,
            "patient_hashed_cf": "HASHED123",
            "strategy": process_payload["strategy"],
            "processed_data_id": processed_data_id
        })
        assert response.status_code == 200, f"Response body: {response.text}"
        report = response.json().get("report")
        # Verify the report exists and references the correct processed data
        assert report is not None
        assert report["processed_data_id"] == processed_data_id

        # --- Step 5: Retrieve reports ---
        response = await xai_client.get(f"/reports/1")
        assert response.status_code == 200, f"Response body: {response.text}"
        reports = response.json().get("reports", [])
        # Ensure at least one report corresponds to the processed data
        assert any(r["processed_data_id"] == processed_data_id for r in reports)
