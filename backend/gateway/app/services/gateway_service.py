# Import the os module to access environment variables (e.g., service URLs)
import os

# Import FastAPI components for handling HTTP headers and raising exceptions
from fastapi import Header, HTTPException

# Import Pydantic schemas for authentication-related requests and responses
from app.schemas.auth_schema import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse

# Import Pydantic schemas for XAI (Explainable AI) analysis requests and responses
from app.schemas.xai_schema import AnalyseRequest, AnalyseResponse, GetReportsResponse

class Gateway:
    # Service class responsible for orchestrating requests between the client
    # and the internal microservices (Authentication, Data Processing, Explainable AI).
    def __init__(self, http_client):
        # Retrieve microservice URLs from environment variables
        self.auth_url = os.getenv("AUTHENTICATION_URL")
        self.xai_url = os.getenv("EXPLAINABLE_AI_URL")
        self.data_url = os.getenv("DATA_PROCESSING_URL")
        # Injected HTTP client for making asynchronous requests
        self.http = http_client

    async def register(self, register_request: RegisterRequest) -> RegisterResponse:
        # Forwards the registration request to the Authentication service.
        # Send POST request to the Authentication service's register endpoint
        res = await self.http.request(
            "POST",
            f"{self.auth_url}/register",
            json=register_request.model_dump()
        )

        # Return the response mapped to the RegisterResponse schema
        return RegisterResponse(**res)

    async def login(self, login_request: LoginRequest) -> LoginResponse:
        # Forwards the login request to the Authentication service.
        # Send POST request to the Authentication service's login endpoint
        res = await self.http.request(
            "POST",
            f"{self.auth_url}/login",
            json=login_request.model_dump()
        )

        # Return the response mapped to the LoginResponse schema
        return LoginResponse(**res)

    async def analyse(self, jwt: str, analyse_request: AnalyseRequest) -> AnalyseResponse:
        """
        Orchestrates the analysis workflow:
        1. Validates the JWT with the Auth service.
        2. Sends raw data to the Data Processing service.
        3. Sends processed data ID to the XAI service for analysis.
        """
        # Step 1: Validate the JWT token with the Authentication service
        jwt_valid_res = await self.http.request(
            "POST",
            f"{self.auth_url}/validate",
            json={"token": jwt}
        )

        # Extract doctor_id from validation response
        doctor_id = jwt_valid_res.get("doctor_id")
        if doctor_id is None:
            # Raise 401 if the token is invalid or doctor_id is missing
            raise HTTPException(status_code=401, detail="Invalid authorization header")

        # Step 2: Prepare payload for Data Processing service
        body = {
            "strategy": analyse_request.strategy,
            "raw_data": analyse_request.raw_data
        }

        # Send data to be processed
        process_res = await self.http.request(
            "POST",
            f"{self.data_url}/process",
            json=body
        )

        # Extract the ID of the processed data
        data_id = process_res.get("processed_data_id")
        if data_id is None:
            # Raise 500 if data processing failed to return an ID
            raise HTTPException(status_code=500, detail="Data processing failed")

        # Step 3: Prepare payload for XAI (Explainable AI) service
        body = {
            "doctor_id": doctor_id,
            "patient_hashed_cf": analyse_request.patient_hashed_cf,
            "strategy": analyse_request.strategy,
            "processed_data_id": data_id
        }

        # Request analysis from the XAI service
        xai_res = await self.http.request(
            "POST",
            f"{self.xai_url}/analyse",
            json=body
        )

        # Return the final analysis response
        return AnalyseResponse(**xai_res)

    async def get_reports(self, jwt: str, patient_hashed_cf: str | None = None) -> GetReportsResponse:
        # Retrieves reports from the XAI service for a specific doctor.
        # Optionally filters by patient hashed CF.
        # Step 1: Validate the JWT token with the Authentication service
        jwt_valid_res = await self.http.request(
            "POST",
            f"{self.auth_url}/validate",
            json={"token": jwt}
        )

        # Extract doctor_id
        doctor_id = jwt_valid_res.get("doctor_id")
        if doctor_id is None:
            raise HTTPException(status_code=401, detail="Invalid authorization header")

        # Construct the URL for fetching reports based on doctor_id
        url = f"{self.xai_url}/reports/{doctor_id}"

        # Append query parameter if patient_hashed_cf is provided
        if patient_hashed_cf is not None:
            url += f"?patient_hashed_cf={patient_hashed_cf}"

        # Step 2: Fetch reports from XAI service
        reports = await self.http.request("GET", url)

        # Return the reports mapped to the response schema
        return GetReportsResponse(**reports)