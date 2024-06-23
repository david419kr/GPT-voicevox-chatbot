@echo off
set "VENV_DIR=%~dp0venv"
set "CLIENT_SCRIPT=client.py"

if exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Virtual environment already exists. Activating it...
    call "%VENV_DIR%\Scripts\activate.bat"

    echo Running streamlit application...
    streamlit run "%~dp0codes\%CLIENT_SCRIPT%"
) else (
    echo Virtual environment does not exist. Creating a new one...

    echo Creating virtual environment in %VENV_DIR%
    python -m venv "%VENV_DIR%
    call "%VENV_DIR%\Scripts\activate.bat"

    echo Installing required packages...
    pip install -r "%~dp0codes\requirements.txt"

    echo Running streamlit application...
    streamlit run "%~dp0codes\%CLIENT_SCRIPT%"
)

echo Done.
pause