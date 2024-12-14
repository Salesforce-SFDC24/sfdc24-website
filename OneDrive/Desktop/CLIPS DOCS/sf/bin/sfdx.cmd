@echo off
setlocal enableextensions

set SF_BINPATH=%~dp0\sf.cmd
if exist "%LOCALAPPDATA%\sf\client\bin\sf.cmd" (
  "%LOCALAPPDATA%\sf\client\bin\sf.cmd" %*
) else (
  "%~dp0\..\client\bin\node.exe" "%~dp0\..\client\bin\run" %*
)
