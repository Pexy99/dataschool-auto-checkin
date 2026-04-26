@echo off
setlocal EnableDelayedExpansion

echo ================================================
echo Name             Start      Next Run               Status
echo ================================================
call :show "DataSchool Check-in" "Check-in"
call :show "DataSchool Mid-Attendance" "Mid-Attendance"
call :show "DataSchool Check-out" "Check-out"
echo ================================================
pause
exit /b 0

:show
set TASK_NAME=%~1
set LABEL=%~2
set START_TIME=
set NEXT_RUN=
set STATUS=

for /f "tokens=1,* delims=:" %%A in ('schtasks /Query /TN "%TASK_NAME%" /V /FO LIST 2^>nul') do (
    set KEY=%%A
    set VALUE=%%B
    if /I "!KEY!"=="Start Time" set START_TIME=!VALUE:~1!
    if /I "!KEY!"=="Next Run Time" set NEXT_RUN=!VALUE:~1!
    if /I "!KEY!"=="Status" set STATUS=!VALUE:~1!
)

if not defined STATUS (
    echo %-16s
    echo %LABEL%    NOT FOUND
    goto :eof
)

echo %LABEL%                !START_TIME!   !NEXT_RUN!   !STATUS!
goto :eof
