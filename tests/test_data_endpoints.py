import pytest
from httpx import AsyncClient
import os

BASE_URL = os.getenv("DATA_PROCESSING_URL", "http://localhost:8004/data_processing")

@pytest.mark.anyio
async def test_process_and_retrieve_flow():
    async with AsyncClient(base_url=BASE_URL) as client:
        process_payload = {
            "strategy": "text",
            "raw_data": "This is a test of the endpoint for pre-processing text data."
        }

        response = await client.post("/process", json=process_payload)
        assert response.status_code == 200, f"Process response: {response.text}"

        data = response.json()
        assert "processed_data_id" in data
        processed_id = data["processed_data_id"]
        assert processed_id > 0

        response = await client.get(f"/retrieve/{processed_id}")
        assert response.status_code == 200, f"Retrieve response: {response.text}"

        retrieved = response.json()
        assert "data" in retrieved
        assert retrieved["data"]["id"] == processed_id
        assert retrieved["data"]["type"] == "text"
        assert retrieved["data"]["data"] != ""