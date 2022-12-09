::
:: SwitchVrroomInputs.bat
:: 
:: Author: Vincent Kocks (engineering@vingenuity.net)
:: v1.1.0
::
:: Displays and allows changing of VRROOM inputs.
::
@echo off


:: --------------------------------------------------------------
:: FILE PARAMETERS
:: --------------------------------------------------------------
set PROJECT_ROOT=..
set PYTHON_SCRIPT=%~dp0switch_vrroom_inputs.py
set PYTHON=python
rem set SKIP_INSTALL=True


:: --------------------------------------------------------------
:: MAIN SCRIPT FLOW
:: --------------------------------------------------------------
if defined SKIP_INSTALL (
    echo Skipping installation of required packages due to %%SKIP_INSTALL%% being set.
    goto :main
)
echo Installing required packages...
%PYTHON% -m pip install -e %PROJECT_ROOT%
if ERRORLEVEL 1 goto :package_install_error
echo Installed required packages successfully.

:main
set /P VRROOM_ADDRESS=Please enter the IP or web address of the VRROOM switch:
set /P VRROOM_PORT=Please enter the port number to connect on the VRROOM switch:

%PYTHON% %PYTHON_SCRIPT%  -a "%VRROOM_ADDRESS%" -p "%VRROOM_PORT%"
goto :finish


:package_install_error
echo Python package installation failed!
goto :finish


:finish
pause
