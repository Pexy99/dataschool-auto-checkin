@echo off
setlocal EnableDelayedExpansion

call :show "DataSchool Check-in" "Check-in"
call :show "DataSchool Mid-Attendance" "Mid-Attendance"
call :show "DataSchool Check-out" "Check-out"
pause
exit /b 0

:show
set "TASK_NAME=%~1"
set "LABEL=%~2"
set "FOUND=0"

for /f "usebackq tokens=1-3 delims=," %%A in (`schtasks /Query /TN "%TASK_NAME%" /FO CSV /NH 2^>nul`) do (
  set "FOUND=1"
  set "TASK=%%~A"
  set "NEXT=%%~B"
  set "STATUS=%%~C"
)

if "%FOUND%"=="0" (
  echo %LABEL%: NOT FOUND
  goto :eof
)

echo %LABEL%: Next=!NEXT! Status=!STATUS!
goto :eof
