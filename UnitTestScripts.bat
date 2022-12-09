::
:: UnitTestScripts.bat
:: 
:: Author: Vincent Kocks (engineering@vingenuity.net)
:: v1.2.0
::
:: Runs unit test scripts for Python projects.
::
@echo off


:: Static Environment Variables
set PACKAGE_REQUIREMENTS_FILE=%~dp0requirements.txt
set PROJECT_NAME=VRROOMpy
set PROJECT_ROOT=.\python
set COVERAGE_REPORT_PATH=%PROJECT_ROOT%\htmlcov\index.html
set PYTHON=python

set OPEN_REPORT=True
set VERBOSE=True


:: Dynamic Environment Variables
if defined VERBOSE set VERBOSE_ARG=-v


:: Main Execution
echo Installing required Python packages for %PROJECT_NAME%...
%PYTHON% -m pip install -r %PACKAGE_REQUIREMENTS_FILE%
if ERRORLEVEL 1 goto :package_install_error
echo Installed Python packages successfully.

pushd %PROJECT_ROOT%
echo Linting %PROJECT_NAME% scripts...
%PYTHON -m black .

echo Testing %PROJECT_NAME% scripts...
%PYTHON% -m coverage run --branch -m unittest discover %VERBOSE_ARG%

echo Generating coverage reports...
%PYTHON% -m coverage report
%PYTHON% -m coverage html
popd

if not defined OPEN_REPORT (
    echo Environment variable %%OPEN_REPORT%% not set.
    echo Skipping opening of coverage report.
    goto :finish
)

if not exist %COVERAGE_REPORT_PATH% goto :report_open_error
echo Opening coverage report...
start "Coverage Report", "%COVERAGE_REPORT_PATH%"
goto :finish


:package_install_error
echo Python package installation failed!
goto :finish


:report_open_error
echo Unable to find coverage report to open!
goto :finish


:finish
if /I not "%1"=="-nopause" pause
