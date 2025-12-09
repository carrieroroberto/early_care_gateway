import os
from fastapi import Header, HTTPException
from app.schemas.auth_schema import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from app.schemas.xai_schema import AnalyseRequest, AnalyseResponse, GetReportsResponse

class Gateway:
    def __init__(self, http_client):
        self.auth_url = os.getenv("AUTHENTICATION_URL")
        self.xai_url = os.getenv("EXPLAINABLE_AI_URL")
        self.data_url = os.getenv("DATA_PROCESSING_URL")
        self.http = http_client

    async def register(self, register_request: RegisterRequest) -> RegisterResponse:
        res = await self.http.request(
            "POST",
            f"{self.auth_url}/register",
            json=register_request.model_dump()
        )
        
        return RegisterResponse(**res)

    async def login(self, login_request: LoginRequest) -> LoginResponse:
        res = await self.http.request(
            "POST",
            f"{self.auth_url}/login",
            json=login_request.model_dump()
        )

        return LoginResponse(**res)

    async def analyse(self, jwt: str, analyse_request: AnalyseRequest) -> AnalyseResponse:
        jwt_valid_res = await self.http.request(
            "POST",
            f"{self.auth_url}/validate",
            json={"token": jwt}
        )

        doctor_id = jwt_valid_res.get("doctor_id")
        if doctor_id is None:
            raise HTTPException(status_code=401, detail="Invalid authorization header")

        body = {
            "strategy": analyse_request.strategy,
            "raw_data": analyse_request.raw_data
        }

        process_res = await self.http.request(
            "POST",
            f"{self.data_url}/process",
            json=body
        )

        data_id = process_res.get("processed_data_id")
        if data_id is None:
            raise HTTPException(status_code=500, detail="Data processing failed")

        body = {
            "doctor_id": doctor_id,
            "patient_hashed_cf": analyse_request.patient_hashed_cf,
            "strategy": analyse_request.strategy,
            "processed_data_id": data_id
        }

        xai_res = await self.http.request(
            "POST",
            f"{self.xai_url}/analyse",
            json=body
        )

        return AnalyseResponse(**xai_res)

    async def get_reports(self, jwt: str, patient_hashed_cf: str | None = None) -> GetReportsResponse:
        jwt_valid_res = await self.http.request(
            "POST",
            f"{self.auth_url}/validate",
            json={"token": jwt}
        )

        doctor_id = jwt_valid_res.get("doctor_id")
        if doctor_id is None:
            raise HTTPException(status_code=401, detail="Invalid authorization header")

        url = f"{self.xai_url}/reports/{doctor_id}"

        if patient_hashed_cf is not None:
            url += f"?patient_hashed_cf={patient_hashed_cf}"

        reports = await self.http.request("GET", url)

        return GetReportsResponse(**reports)