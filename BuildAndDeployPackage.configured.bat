::
:: BuildAndDeployPackage.configured.bat
:: 
:: Author: Vincent Kocks (engineering@vingenuity.net)
:: v1.0.0
::
:: Pre-sets credentials for build systems before running the main batch script.
::
@echo off

set MAIN_SCRIPT_PATH=.\BuildAndDeployPackage.bat

set TWINE_PASSWORD=
set TWINE_USERNAME=

call %MAIN_SCRIPT_PATH% %*
