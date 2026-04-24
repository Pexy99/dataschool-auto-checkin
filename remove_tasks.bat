@echo off
setlocal

echo Removing check-in task...
schtasks /Delete /F /TN "DataSchool Check-in"

echo Removing mid-attendance task...
schtasks /Delete /F /TN "DataSchool Mid-Attendance"

echo Removing check-out task...
schtasks /Delete /F /TN "DataSchool Check-out"

echo.
echo Done.
pause
