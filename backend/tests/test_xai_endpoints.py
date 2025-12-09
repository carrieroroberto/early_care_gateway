import pytest
from httpx import AsyncClient
import os

BASE_XAI_URL = os.getenv("EXPLAINABLE_AI_URL", "http://localhost:8003/explainable_ai")
BASE_DATA_URL = os.getenv("DATA_PROCESSING_URL", "http://localhost:8004/data_processing")

@pytest.mark.anyio
async def test_analyse_and_get_reports_flow():
    async with AsyncClient(base_url=BASE_DATA_URL) as data_client:
        process_payload = {
            "strategy": "text",
            "raw_data": "This is a sample raw data for processing."
        }

        response = await data_client.post("/process", json=process_payload)
        assert response.status_code == 200, response.text

        processed_id = response.json()["processed_data_id"]
        assert processed_id > 0

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

        assert report["doctor_id"] == 1
        assert report["patient_hashed_cf"] == "HASH123"
        assert report["processed_data_id"] == processed_id
        assert report["strategy"] == "text"
        assert report["diagnosis"] != ""
        assert report["confidence"] is not None

        generated_report_id = report["id"]

    async with AsyncClient(base_url=BASE_XAI_URL) as xai_client:
        response = await xai_client.get("/reports/1")

        assert response.status_code == 200
        body = response.json()

        assert "reports" in body
        assert any(r["id"] == generated_report_id for r in body["reports"])

    async with AsyncClient(base_url=BASE_XAI_URL) as xai_client:
        response = await xai_client.get("/reports/1?patient_hashed_cf=HASH123")

        assert response.status_code == 200
        body = response.json()

        assert "reports" in body
        assert len(body["reports"]) > 0
        assert body["reports"][0]["patient_hashed_cf"] == "HASH123"


@pytest.mark.anyio
async def test_analyse_invalid_strategy():
    async with AsyncClient(base_url=BASE_XAI_URL) as xai_client:
        payload = {
            "doctor_id": 1,
            "patient_hashed_cf": "HASH123",
            "processed_data_id": 1,
            "strategy": "does_not_exist"
        }

        response = await xai_client.post("/analyse", json=payload)
        assert response.status_code == 400 or response.status_code == 422


@pytest.mark.anyio
async def test_reports_doctor_no_reports():
    async with AsyncClient(base_url=BASE_XAI_URL) as xai_client:
        response = await xai_client.get("/reports/99999")
        assert response.status_code == 200

        body = response.json()
        assert body["message"] in ("No reports retrieved", "Success")
        assert body["reports"] == []