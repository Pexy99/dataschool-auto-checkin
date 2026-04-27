@echo off
setlocal
cd /d %~dp0

REM You can change the default times below.
set CHECKIN_TIME=08:55
set CHECKOUT_TIME=17:55
set MID_ATTENDANCE_START=15:30
set MID_ATTENDANCE_END=16:30
set MID_ATTENDANCE_POLL=30

findstr /R /C:"^NAME = ''$" config.py >nul && goto config_error
findstr /R /C:"^PASSWORD = ''$" config.py >nul && goto config_error

echo [1/3] Registering check-in task...
schtasks /Create /F /TN "DataSchool Check-in" /SC WEEKLY /D MON,TUE,WED,THU,FRI /ST %CHECKIN_TIME% /TR "cmd /c cd /d %~dp0 && py -3 src\attendance.py --action in"
if errorlevel 1 (
  echo Failed to register check-in task.
  pause
  exit /b 1
)

echo [2/3] Registering mid-attendance task...
schtasks /Create /F /TN "DataSchool Mid-Attendance" /SC WEEKLY /D MON,TUE,WED,THU,FRI /ST %MID_ATTENDANCE_START% /TR "cmd /c cd /d %~dp0 && py -3 src\mid_attendance.py --start-time %MID_ATTENDANCE_START% --end-time %MID_ATTENDANCE_END% --poll-seconds %MID_ATTENDANCE_POLL%"
if errorlevel 1 (
  echo Failed to register mid-attendance task.
  pause
  exit /b 1
)

echo [3/3] Registering check-out task...
schtasks /Create /F /TN "DataSchool Check-out" /SC WEEKLY /D MON,TUE,WED,THU,FRI /ST %CHECKOUT_TIME% /TR "cmd /c cd /d %~dp0 && py -3 src\attendance.py --action out"
if errorlevel 1 (
  echo Failed to register check-out task.
  pause
  exit /b 1
)

echo.
echo Done.
echo Registered check-in time      : %CHECKIN_TIME%
echo Registered mid-attendance time: %MID_ATTENDANCE_START%
echo Mid-attendance end time       : %MID_ATTENDANCE_END%
echo Mid-attendance poll seconds   : %MID_ATTENDANCE_POLL%
echo Registered check-out time     : %CHECKOUT_TIME%
pause
exit /b 0

:config_error
echo Please fill in NAME and PASSWORD in config.py first.
pause
exit /b 1
