@echo off
setlocal
cd /d %~dp0

REM You can change the default times below.
set CHECKIN_TIME=08:55
set CHECKOUT_TIME=17:55

echo [1/2] Registering check-in task...
schtasks /Create /F /TN "DataSchool Check-in" /SC DAILY /ST %CHECKIN_TIME% /TR "cmd /c cd /d %~dp0 && py -3 attendance_session_based.py --action in"
if errorlevel 1 (
  echo Failed to register check-in task.
  pause
  exit /b 1
)

echo [2/2] Registering check-out task...
schtasks /Create /F /TN "DataSchool Check-out" /SC DAILY /ST %CHECKOUT_TIME% /TR "cmd /c cd /d %~dp0 && py -3 attendance_session_based.py --action out"
if errorlevel 1 (
  echo Failed to register check-out task.
  pause
  exit /b 1
)

echo.
echo Done.
echo Registered check-in time : %CHECKIN_TIME%
echo Registered check-out time: %CHECKOUT_TIME%
echo You can change the values at the top of this file before running it.
echo You can also change the times later in Task Scheduler.
pause
