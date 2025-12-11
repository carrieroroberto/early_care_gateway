import pytest
from httpx import AsyncClient
import os

# Base URLs for XAI and Data Processing services
BASE_XAI_URL = os.getenv("EXPLAINABLE_AI_URL", "http://localhost:8003/explainable_ai")
BASE_DATA_URL = os.getenv("DATA_PROCESSING_URL", "http://localhost:8004/data_processing")

# Test 1: Full analyse → retrieve reports flow
@pytest.mark.anyio
async def test_analyse_and_get_reports_flow():
    # Step 1: Process raw data
    async with AsyncClient(base_url=BASE_DATA_URL) as data_client:
        process_payload = {
            "strategy": "text",  # Processing strategy
            "raw_data": "This is a sample raw data for processing."
        }

        response = await data_client.post("/process", json=process_payload)
        # Ensure processing succeeded
        assert response.status_code == 200, response.text

        processed_id = response.json()["processed_data_id"]
        # Verify returned ID is positive
        assert processed_id > 0

    # Step 2: Analyse the processed data via XAI service
    async with AsyncClient(base_url=BASE_XAI_URL) as xai_client:
        analysis_payload = {
            "doctor_id": 1,
            "patient_hashed_cf": "HASH123",
            "processed_data_id": processed_id,
            "strategy": "text"
        }

        response = await xai_client.post("/analyse", json=analysis_payload)
        assert response.status_code == 200, f"Analyse response: {response.text}"

        data = response.json()
        assert "report" in data
        report = data["report"]

        # Validate report fields
        assert report["doctor_id"] == 1
        assert report["patient_hashed_cf"] == "HASH123"
        assert report["processed_data_id"] == processed_id
        assert report["strategy"] == "text"
        assert report["diagnosis"] != ""
        assert report["confidence"] is not None

        generated_report_id = report["id"]

    # Step 3: Retrieve all reports for doctor_id=1
    async with AsyncClient(base_url=BASE_XAI_URL) as xai_client:
        response = await xai_client.get("/reports/1")
        assert response.status_code == 200
        body = response.json()

        assert "reports" in body
        # Verify our generated report exists in the list
        assert any(r["id"] == generated_report_id for r in body["reports"])

    # Step 4: Retrieve reports filtered by patient_hashed_cf
    async with AsyncClient(base_url=BASE_XAI_URL) as xai_client:
        response = await xai_client.get("/reports/1?patient_hashed_cf=HASH123")
        assert response.status_code == 200
        body = response.json()

        assert "reports" in body
        assert len(body["reports"]) > 0
        assert body["reports"][0]["patient_hashed_cf"] == "HASH123"

# Test 2: Analyse with invalid strategy
@pytest.mark.anyio
async def test_analyse_invalid_strategy():
    async with AsyncClient(base_url=BASE_XAI_URL) as xai_client:
        payload = {
            "doctor_id": 1,
            "patient_hashed_cf": "HASH123",
            "processed_data_id": 1,
            "strategy": "does_not_exist"  # Invalid strategy
        }

        response = await xai_client.post("/analyse", json=payload)
        # Expect a client error: 400 Bad Request or 422 Unprocessable Entity
        assert response.status_code == 400 or response.status_code == 422

# Test 3: Retrieve reports for doctor with no reports
@pytest.mark.anyio
async def test_reports_doctor_no_reports():
    async with AsyncClient(base_url=BASE_XAI_URL) as xai_client:
        response = await xai_client.get("/reports/99999")  # Non-existent doctor
        assert response.status_code == 200

        body = response.json()
        # Check response message and ensure reports list is empty
        assert body["message"] in ("No reports retrieved", "Success")
        assert body["reports"] == []
