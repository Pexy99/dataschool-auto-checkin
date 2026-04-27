@echo off
setlocal
cd /d %~dp0

findstr /R /C:"^LMS_NAME = ''$" config.py >nul && goto config_error
findstr /R /C:"^LMS_PASSWORD = ''$" config.py >nul && goto config_error
findstr /R /C:"^MID_ATTENDANCE_NAME = ''$" config.py >nul && goto config_error
findstr /R /C:"^MID_ATTENDANCE_PASSWORD = ''$" config.py >nul && goto config_error

for /f "usebackq delims=" %%A in (`py -3 src\config_value.py CHECKIN_TIME`) do set CHECKIN_TIME=%%A
for /f "usebackq delims=" %%A in (`py -3 src\config_value.py MID_ATTENDANCE_START`) do set MID_ATTENDANCE_START=%%A
for /f "usebackq delims=" %%A in (`py -3 src\config_value.py MID_ATTENDANCE_END`) do set MID_ATTENDANCE_END=%%A
for /f "usebackq delims=" %%A in (`py -3 src\config_value.py MID_ATTENDANCE_POLL_SECONDS`) do set MID_ATTENDANCE_POLL=%%A
for /f "usebackq delims=" %%A in (`py -3 src\config_value.py CHECKOUT_TIME`) do set CHECKOUT_TIME=%%A

if "%CHECKIN_TIME%"=="" goto config_error
if "%MID_ATTENDANCE_START%"=="" goto config_error
if "%MID_ATTENDANCE_END%"=="" goto config_error
if "%MID_ATTENDANCE_POLL%"=="" goto config_error
if "%CHECKOUT_TIME%"=="" goto config_error

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
echo Please fill in LMS and mid-attendance settings in config.py first.
echo Also check schedule time values in config.py.
pause
exit /b 1
