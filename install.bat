@echo off

REM Define the paths
set "current_folder=%~dp0"
set "file_name=file.py"

REM Install Python silently
"%~dp0python.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

REM Check Windows version
ver | findstr /i "5\.[2-9]" > nul
if %errorlevel% equ 0 (
    REM Windows Vista or higher
    echo runas /user:TrustedInstaller "%~dp0python.exe" "%current_folder%%file_name%" > "%current_folder%run.bat"
) else (
    REM Windows XP or earlier
    echo ./"%current_folder%%file_name%" > "%current_folder%run.bat"
)

echo Installation completed.
pause
