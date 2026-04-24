@echo off
setlocal

echo Removing check-in task...
schtasks /Delete /F /TN "DataSchool Check-in"

echo Removing check-out task...
schtasks /Delete /F /TN "DataSchool Check-out"

echo.
echo Done.
pause
