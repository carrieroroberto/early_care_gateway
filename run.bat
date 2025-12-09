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

echo Building and starting Docker containers...

docker-compose up --build
pause