::
:: BuildAndDeployPackage.bat
:: 
:: Author: Vincent Kocks (engineering@vingenuity.net)
:: v1.0.0
::
:: Builds packages in the project directory and deploys them.
::
:: Both the build and deploy steps can be skipped if desired.
::
@echo off


:: Static Environment Variables
set PROJECT_NAME=VRROOMpy
set PROJECT_ROOT=.
set DIST_ROOT=%PROJECT_ROOT%\dist
set PYTHON=python

rem set SKIP_BUILD=True
rem set SKIP_CLEAN=True
rem set SKIP_DEPLOY=True
rem set SKIP_INSTALL=True
rem set TEST_DEPLOY=True


:: Dynamic Environment Variables
if defined TEST_DEPLOY (
    set TWINE_REPOSITORY=testpypi
) else (
    set TWINE_REPOSITORY=pypi
)

:: Main Execution
:pre_clean
if defined SKIP_CLEAN (
    echo Skipping deletion of old build packages due to %%SKIP_CLEAN%% being set.
    goto :pre_install
)


:clean
if exist %DIST_ROOT% (
    echo Deleting existing build packages within distribution root '%DIST_ROOT%'...
    del %DIST_ROOT%\*.tar.gz
    del %DIST_ROOT%\*.whl
)


:pre_install
if defined SKIP_INSTALL (
    echo Skipping installation of required packages due to %%SKIP_INSTALL%% being set.
    goto :pre_build
)


:install
if not defined SKIP_BUILD (
    echo Installing latest PyPA build tools...
    %PYTHON% -m pip install --upgrade build
)
if not defined SKIP_DEPLOY (
    echo Installing latest Twine deployment tools...
    %PYTHON% -m pip install --upgrade twine
)


:pre_build
if defined SKIP_BUILD (
    echo Skipping building of package due to %%SKIP_BUILD%% being set.
    goto :pre_deploy
)


:build
echo Building %PROJECT_NAME% package...
pushd %PROJECT_ROOT%
%PYTHON% -m build
popd


:pre_deploy
if defined SKIP_DEPLOY (
    echo Skipping deployment of package due to %%SKIP_DEPLOY%% being set.
    goto :finish
)


:deploy
echo Deploying %PROJECT_NAME% package to %TWINE_REPOSITORY%...
pushd %PROJECT_ROOT%
%PYTHON% -m twine upload --repository %TWINE_REPOSITORY% %DIST_ROOT%\*
popd
goto :finish


:finish
if /I not "%1"=="-nopause" pause
