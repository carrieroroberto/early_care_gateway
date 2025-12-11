import pytest
from httpx import AsyncClient
import os

# Base URL for the Data Processing microservice.
# Defaults to localhost if the environment variable is not set.
BASE_URL = os.getenv("DATA_PROCESSING_URL", "http://localhost:8004/data_processing")

# Test: Full process → retrieve flow
@pytest.mark.anyio
async def test_process_and_retrieve_flow():
    # Use an asynchronous HTTP client for the data processing API
    async with AsyncClient(base_url=BASE_URL) as client:
        # Payload for processing raw text data
        process_payload = {
            "strategy": "text",  # Strategy specifies the processing type
            "raw_data": "This is a test of the endpoint for pre-processing text data."
        }

        # Send POST request to /process endpoint
        response = await client.post("/process", json=process_payload)
        # Ensure request succeeded
        assert response.status_code == 200, f"Process response: {response.text}"

        # Parse response JSON
        data = response.json()
        # Check that processed_data_id exists in the response
        assert "processed_data_id" in data
        processed_id = data["processed_data_id"]
        # Ensure the ID is a positive integer
        assert processed_id > 0

        # Retrieve the processed data using the returned ID
        response = await client.get(f"/retrieve/{processed_id}")
        # Ensure retrieval succeeded
        assert response.status_code == 200, f"Retrieve response: {response.text}"

        # Parse retrieved data
        retrieved = response.json()
        # Validate response structure
        assert "data" in retrieved
        assert retrieved["data"]["id"] == processed_id
        assert retrieved["data"]["type"] == "text"
        assert retrieved["data"]["data"] != ""  # Ensure processed data is not empty
