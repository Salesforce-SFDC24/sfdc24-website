@echo off
setlocal enableextensions

if not "%SF_REDIRECTED%"=="1" if exist "%LOCALAPPDATA%\sf\client\bin\sf.cmd" (
  set SF_REDIRECTED=1
  "%LOCALAPPDATA%\sf\client\bin\sf.cmd" %*
  goto:EOF
)

if not defined SF_BINPATH set SF_BINPATH="%~dp0sf.cmd"

if exist "%~dp0..\bin\node.exe" (
  "%~dp0..\bin\node.exe"  "%~dp0..\bin\run" %*
) else if exist "%LOCALAPPDATA%\oclif\node\node-22.10.0.exe" (
  "%LOCALAPPDATA%\oclif\node\node-22.10.0.exe"  "%~dp0..\bin\run" %*
) else (
  node  "%~dp0..\bin\run" %*
)
