@echo off
setlocal

echo ==============================
echo DataSchool scheduled tasks
echo ==============================
echo.

echo [Check-in]
schtasks /Query /TN "DataSchool Check-in" /V /FO LIST
if errorlevel 1 echo Task not found.
echo.

echo [Mid-Attendance]
schtasks /Query /TN "DataSchool Mid-Attendance" /V /FO LIST
if errorlevel 1 echo Task not found.
echo.

echo [Check-out]
schtasks /Query /TN "DataSchool Check-out" /V /FO LIST
if errorlevel 1 echo Task not found.
echo.
pause
