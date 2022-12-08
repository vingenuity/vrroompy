::
:: SwitchVrroomInputs.bat
:: 
:: Author: Vincent Kocks (engineering@vingenuity.net)
:: v1.0.0
::
:: Displays and allows changing of VRROOM inputs.
::
@echo off


:: --------------------------------------------------------------
:: FILE PARAMETERS
:: --------------------------------------------------------------
set PYTHON_SCRIPT=%~dp0python\switch_vrroom_inputs.py
set PYTHON=python


:: --------------------------------------------------------------
:: MAIN SCRIPT FLOW
:: --------------------------------------------------------------
set /P VRROOM_ADDRESS=Please enter the IP or web address of the VRROOM switch:
set /P VRROOM_PORT=Please enter the port number to connect on the VRROOM switch:

%PYTHON% %PYTHON_SCRIPT%  -a "%VRROOM_ADDRESS%" -p "%VRROOM_PORT%"

pause
