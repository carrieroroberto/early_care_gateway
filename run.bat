@echo off
color 03
cls

:::   ___          _         ___                 ___      _                        
:::  | __|__ _ _ _| |_  _   / __|__ _ _ _ ___   / __|__ _| |_ _____ __ ____ _ _  _ 
:::  | _|/ _` | '_| | || | | (__/ _` | '_/ -_) | (_ / _` |  _/ -_) V  V / _` | || |
:::  |___\__,_|_| |_|\_, |  \___\__,_|_| \___|  \___\__,_|\__\___|\_/\_/\__,_|\_, |
:::                  |__/                                                     |__/ 
:::
:: The ASCII art above is extracted and printed automatically by the loop below.

for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A
:: This loop searches the current script for lines starting with ":::"
:: and prints them, effectively displaying the ASCII banner.

echo Starting containers...
docker-compose up --build -d
:: Builds and starts all Docker containers in detached mode.

echo.
echo Waiting for services to be ready...

:: Waits for each microservice until its /docs endpoint returns HTTP 200
call :wait_http http://localhost:8001/docs AUDIT
call :wait_http http://localhost:8000/docs AUTH
call :wait_http http://localhost:8004/docs DATA
call :wait_http http://localhost:8003/docs XAI
call :wait_http http://localhost:8002/docs GATEWAY

echo.
echo All services are ready.

cd tests
:: Moves to the test directory.

echo Installing Python test dependencies...
python -m venv test
:: Creates a virtual environment named "test".

call test\Scripts\activate.bat
:: Activates the virtual environment.

python -m pip install --upgrade pip
pip install -r requirements.txt
:: Installs and updates required Python test packages.

echo Running tests...
python -m pytest
:: Executes test suite using pytest.

pause
exit /b
:: Pauses so the window stays open, then exits.

:wait_http
:: Function to poll an HTTP endpoint until it returns status code 200.

set URL=%1
set NAME=%2

echo Waiting for %NAME%_SERVICE...

:check_http
powershell -NoProfile -Command ^
"try { $r = Invoke-WebRequest -Uri '%URL%' -UseBasicParsing; if($r.StatusCode -eq 200){ exit 0 } else { exit 1 } } catch { exit 1 }"
:: Uses PowerShell to send an HTTP request.
:: If the endpoint is reachable and returns 200, success. Otherwise retry.

if %ERRORLEVEL% neq 0 (
    timeout /t 1 >nul
    goto check_http
)
:: If the service is not ready, waits 1 second and checks again.

exit /b
