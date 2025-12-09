@echo off
color 03
cls

:::   ___          _         ___                 ___      _                        
:::  | __|__ _ _ _| |_  _   / __|__ _ _ _ ___   / __|__ _| |_ _____ __ ____ _ _  _ 
:::  | _|/ _` | '_| | || | | (__/ _` | '_/ -_) | (_ / _` |  _/ -_) V  V / _` | || |
:::  |___\__,_|_| |_|\_, |  \___\__,_|_| \___|  \___\__,_|\__\___|\_/\_/\__,_|\_, |
:::                  |__/                                                     |__/ 
:::

for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A

echo Starting containers...
docker-compose up --build -d

echo.
echo Waiting for services to be ready...

call :wait_http http://localhost:8001/docs AUDIT
call :wait_http http://localhost:8000/docs AUTH
call :wait_http http://localhost:8004/docs DATA
call :wait_http http://localhost:8003/docs XAI
call :wait_http http://localhost:8002/docs GATEWAY

echo.
echo All services are ready.

cd tests

echo Installing Python test dependencies...
python -m venv test
call test\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Running tests...
python -m pytest
pause
exit /b

:wait_http
set URL=%1
set NAME=%2

echo Waiting for %NAME%_SERVICE...

:check_http
powershell -NoProfile -Command ^
"try { $r = Invoke-WebRequest -Uri '%URL%' -UseBasicParsing; if($r.StatusCode -eq 200){ exit 0 } else { exit 1 } } catch { exit 1 }"

if %ERRORLEVEL% neq 0 (
    timeout /t 1 >nul
    goto check_http
)

exit /b