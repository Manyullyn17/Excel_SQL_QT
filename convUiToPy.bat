@echo off

rem Get the pyuic6 path
set "PROJECT_DIR=%cd%"
set "VENV_PATH=%PROJECT_DIR%\.venv\Scripts\pyuic6.exe"

:: Run pyuic6 with the provided arguments
%VENV_PATH% Excel_SQL_GUI.ui -o GUI.py
%VENV_PATH% settings.ui -o settings.py
