@echo off
echo Activating Python Virtual Environment...
echo.

REM Activate the virtual environment
set DEBUG=true
set ENVIRONMENT=development
call venv\Scripts\activate.bat

REM Show current Python and pip info
echo.
echo Virtual environment activated!
echo Python: %VIRTUAL_ENV%\Scripts\python.exe
echo.
echo To run the application:
echo   python run.py
echo.
echo To deactivate:
echo   deactivate
echo.

REM Keep the command prompt open
cmd /k
