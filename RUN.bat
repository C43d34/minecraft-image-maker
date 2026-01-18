@echo OFF
:: 1. Run virtual environment 
:: 2. Verify dependencies
:: 3. Run program


:: set current working directory => the directory this file exists in 
cd /d %~dp0 
:: Wrap string with quotes to prevent weird parser issues when passing variable 
SET venv_name="venv"
SET virtual_env_path="%CD%/%venv_name%/Scripts/activate"  

:: 1. 
:: Try to run virtual environment in this project 
echo Setting virtual environment at %virtual_env_path%
IF EXIST %virtual_env_path% (
    ::CALL runs the batch script to setup virtual environment  
    CALL %virtual_env_path% 
) ELSE (
    python -m venv %venv_name%
    CALL %virtual_env_path% 
)


:: 2
echo Installing required libraries...
python -m pip install -r gui_reqs.txt

:: 3. 
echo Starting GUI Program...
SET gui_run_path=python gui.py
%gui_run_path%