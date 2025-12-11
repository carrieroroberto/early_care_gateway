# Import schemas for request and response models related to authentication and XAI analysis
from ..schemas.auth_schema import RegisterResponse, RegisterRequest, LoginResponse, LoginRequest
from ..schemas.xai_schema import AnalyseResponse, AnalyseRequest, GetReportsResponse

# Import utility functions for dependency injection (service retrieval and JWT handling)
from ..utils.dependencies import get_gateway_service, get_jwt

# Import the Gateway service class
from ..services.gateway_service import Gateway

# Initialize the API router with a prefix and tags for documentation organization
router = APIRouter(prefix="/gateway", tags=["Endpoints"])

@router.post("/register", response_model=RegisterResponse)
async def register(register_body: RegisterRequest, gateway_service: Gateway = Depends(get_gateway_service)) -> RegisterResponse:
    # Endpoint to register a new user.
    # It delegates the registration logic to the gateway service.
    try:
        # Call the register method of the gateway service with the provided request body
        return await gateway_service.register(register_body)
    except Exception as e:
        # Raise an HTTP 400 exception if an error occurs during registration
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=LoginResponse)
async def login(login_body: LoginRequest, gateway_service: Gateway = Depends(get_gateway_service)) -> LoginResponse:
    # Endpoint to authenticate a user.
    # It delegates the login logic to the gateway service.
    try:
        # Call the login method of the gateway service with the provided credentials
        return await gateway_service.login(login_body)
    except Exception as e:
        # Raise an HTTP 400 exception if an error occurs during login
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/analyse", response_model=AnalyseResponse)
async def analyse(
    analyse_body: AnalyseRequest, jwt: str = Depends(get_jwt), gateway_service: Gateway = Depends(get_gateway_service)) -> AnalyseResponse:
    # Endpoint to perform data analysis.
    # Requires a valid JWT token for authorization.
    try:
        # Call the analyse method of the gateway service, passing the JWT and the analysis request data
        return await gateway_service.analyse(jwt=jwt, analyse_request=analyse_body)
    except Exception as e:
        # Raise an HTTP 400 exception if an error occurs during the analysis process
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reports", response_model=GetReportsResponse)
async def get_reports(jwt: str = Depends(get_jwt), patient_hashed_cf: str | None = Query(None), gateway_service: Gateway = Depends(get_gateway_service)) -> GetReportsResponse:
    # Endpoint to retrieve reports.
    # Requires a valid JWT token. Optionally filters by patient's hashed tax code (CF).
    try:
        # Call the get_reports method of the gateway service with the JWT and optional patient identifier
        return await gateway_service.get_reports(jwt=jwt, patient_hashed_cf=patient_hashed_cf)
    except Exception as e:
        # Raise an HTTP 400 exception if an error occurs while retrieving reports
        raise HTTPException(status_code=400, detail=str(e))