@echo off
REM FitTrack AI - Environment Setup Script (Windows)
REM Run this script to set up your environment with the Groq API key

echo.
echo ========================================
echo   FitTrack AI - Environment Setup
echo ========================================
echo.

REM Load API key from config file if it exists
if exist "api_key.txt" (
    set /p GROQ_API_KEY=<api_key.txt
    echo [OK] Loaded API key from api_key.txt
) else (
    REM Fallback: Set placeholder (REPLACE WITH YOUR OWN FOR PRODUCTION)
    set GROQ_API_KEY=your_groq_api_key_here
    echo [WARNING] Using placeholder API key
    echo.
    echo To use your own key:
    echo   - Create api_key.txt with your Groq API key
    echo   - Or set: set GROQ_API_KEY=your_key_here
    echo.
)

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
) else (
    echo [ERROR] Virtual environment not found
    echo Please run: python -m venv venv
    exit /b 1
)

REM Verify API key is set
if "%GROQ_API_KEY%"=="" (
    echo [ERROR] GROQ_API_KEY not set
    exit /b 1
) else (
    echo [OK] GROQ_API_KEY configured
)

echo.
echo ====================================
echo   Setup complete!
echo ====================================
echo.
echo Now run: python app.py
echo.
echo Or run everything in one command:
echo   setup_env.bat ^&^& python app.py
echo.

REM Stay in the environment
cmd /k

