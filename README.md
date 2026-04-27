# DataSchool Auto Check-in

## 1. 수정할 파일
먼저 `config.py` 파일만 열어서 필요한 값을 입력하세요.

### LMS 입실/퇴실 사이트
```python
LMS_NAME = ''
LMS_PASSWORD = ''
```

### 중간출결 사이트
```python
MID_ATTENDANCE_NAME = ''
MID_ATTENDANCE_PASSWORD = ''
```

둘 다 같은 이름/비밀번호를 쓰면 같은 값을 입력하면 됩니다.

### 자동화 시간
```python
CHECKIN_TIME = '08:55'
MID_ATTENDANCE_START = '15:30'
MID_ATTENDANCE_END = '16:30'
MID_ATTENDANCE_POLL_SECONDS = 45
MID_ATTENDANCE_RANDOM_DELAY_SECONDS = 10
CHECKOUT_TIME = '17:55'
```

필요하면 `skip_dates.txt`에 쉬는 날짜를 추가하세요.

```txt
2026-05-01
2026-05-05
```

## 2. 자동화 등록
`register_tasks.bat`를 실행하면 작업 스케줄러에 월~금 자동 등록됩니다.

등록 시간은 `config.py`의 시간 설정을 사용합니다.
등록 상태 확인은 `check_tasks.bat`를 실행하면 됩니다.

## 3. 자동화 삭제
등록된 작업을 지우고 싶으면 `remove_tasks.bat`를 실행하면 됩니다.

## 4. 수동 실행
직접 테스트하고 싶으면 아래 파일을 실행하면 됩니다.

- `run_checkin.bat`
- `run_mid_attendance.bat`
- `run_checkout.bat`
- `check_tasks.bat`

## 5. 실행 결과
- 입실 성공 시: `08:55 입실 완료`
- 이미 입실된 경우: `08:55 입실 이미 처리됨`
- 중간출결 성공 시: `중간출결 완료 (코드)`
- 퇴실 성공 시: `17:55 퇴실 완료`
- 금요일 퇴실 시: 최근 5일 출결현황도 같이 팝업 표시

결과는 콘솔에 출력되고, Windows 팝업으로도 표시됩니다.

## 6. 윈도우 자동화 주의사항
- 컴퓨터가 켜져 있어야 자동 실행됩니다.
- 절전 모드, 최대 절전 모드 상태에서는 자동 실행되지 않을 수 있습니다.
- 화면이 꺼져 있어도 PC 자체가 깨어 있으면 실행될 수 있습니다.
- 노트북은 전원을 연결해두고 절전 설정을 확인하는 것을 권장합니다.
- 재부팅 후에도 윈도우에 다시 로그인되어 있고 작업 스케줄러가 살아 있으면 계속 동작할 수 있습니다.
- 시간 변경 후에는 `register_tasks.bat`를 다시 실행하거나 작업 스케줄러에서 직접 수정하면 됩니다.
