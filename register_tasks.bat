@echo off
setlocal
cd /d %~dp0

echo [1/2] 입실 작업 등록 중...
schtasks /Create /F /TN "DataSchool Check-in" /SC DAILY /ST 08:55 /TR "cmd /c cd /d %~dp0 && py -3 attendance_session_based.py --action in"
if errorlevel 1 (
  echo 입실 작업 등록 실패
  pause
  exit /b 1
)

echo [2/2] 퇴실 작업 등록 중...
schtasks /Create /F /TN "DataSchool Check-out" /SC DAILY /ST 17:55 /TR "cmd /c cd /d %~dp0 && py -3 attendance_session_based.py --action out"
if errorlevel 1 (
  echo 퇴실 작업 등록 실패
  pause
  exit /b 1
)

echo.
echo 등록 완료!
echo 기본 시간은 입실 08:55, 퇴실 17:55 입니다.
echo 시간이 다르면 작업 스케줄러에서 각 작업 시간을 수정하면 됩니다.
pause
