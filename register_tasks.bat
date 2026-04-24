@echo off
setlocal
cd /d %~dp0

echo [1/2] Registering check-in task...
schtasks /Create /F /TN "DataSchool Check-in" /SC DAILY /ST 08:55 /TR "cmd /c cd /d %~dp0 && py -3 attendance_session_based.py --action in"
if errorlevel 1 (
  echo Failed to register check-in task.
  pause
  exit /b 1
)

echo [2/2] Registering check-out task...
schtasks /Create /F /TN "DataSchool Check-out" /SC DAILY /ST 17:55 /TR "cmd /c cd /d %~dp0 && py -3 attendance_session_based.py --action out"
if errorlevel 1 (
  echo Failed to register check-out task.
  pause
  exit /b 1
)

echo.
echo Done.
echo Default times: 08:55 for check-in, 17:55 for check-out.
echo You can change the times later in Task Scheduler.
pause
