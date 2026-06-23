@echo off

title Trade Trans Carrier Onboarding 2.0

REM Przejście do katalogu backend
cd /d "%~dp0backend"

REM Aktywacja środowiska Python
call venv\Scripts\activate.bat

REM Uruchomienie backendu
start "" cmd /k "uvicorn main:app"

REM Czekamy aż backend wystartuje
timeout /t 3 /nobreak > nul

REM Otwieramy aplikację
start "" "%~dp0frontend\index.html"

exit