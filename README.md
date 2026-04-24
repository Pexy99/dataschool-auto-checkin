# DataSchool Auto Check-in

윈도우에서 사용할 수 있는 데이터스쿨 자동화 묶음입니다.

## 포함 파일
- `attendance_session_based.py`: 세션 기반 입실/퇴실 스크립트
- `mid_attendance.py`: 중간출결 스크립트
- `run_checkin.bat`: 입실 수동 실행
- `run_checkout.bat`: 퇴실 수동 실행
- `run_mid_attendance.bat`: 중간출결 수동 실행
- `register_tasks.bat`: 작업 스케줄러 자동 등록
- `remove_tasks.bat`: 등록된 작업 스케줄러 삭제
- `skip_dates.txt`: 예외일 목록

## 처음 사용할 때
1. `attendance_session_based.py` 상단에서 아래 값 수정
   - `NAME = '본인 이름 입력'`
   - `PASSWORD = '본인 비밀번호 입력'`
2. `mid_attendance.py` 상단에서도 아래 값 수정
   - `NAME = '본인 이름 입력'`
   - `PASSWORD = '본인 비밀번호 입력'`
3. Python 설치 확인
   - 권장: `py -3 --version` 이 실행되는지 확인
4. 필요하면 `skip_dates.txt`에 예외일 추가
   - 형식: `YYYY-MM-DD`
   - 예시: `2026-05-01`

## 수동 실행
- 입실: `run_checkin.bat`
- 퇴실: `run_checkout.bat`
- 중간출결: `run_mid_attendance.bat`

실행 결과는 콘솔에 출력되고, Windows 팝업으로도 표시됩니다.

## 작업 스케줄러 등록
`register_tasks.bat`를 실행하면 아래 3개 작업이 등록됩니다.
- `DataSchool Check-in` → 기본 `08:55`
- `DataSchool Mid-Attendance` → 기본 `15:30`
- `DataSchool Check-out` → 기본 `17:55`

`register_tasks.bat` 상단 변수 수정으로 변경 가능한 값:
- `CHECKIN_TIME`
- `CHECKOUT_TIME`
- `MID_ATTENDANCE_START`
- `MID_ATTENDANCE_END`
- `MID_ATTENDANCE_POLL`

중간출결은 등록된 시작 시각에 실행된 뒤,
기본적으로 `15:30 ~ 16:30` 동안 `30초` 간격으로 시도합니다.

또한 `register_tasks.bat`는 등록 전에 아래를 검사합니다.
- `attendance_session_based.py`의 이름/비밀번호 입력 여부
- `mid_attendance.py`의 이름/비밀번호 입력 여부

입력되지 않았으면 작업 등록을 막고 안내 메시지를 표시합니다.

## 작업 스케줄러 삭제
`remove_tasks.bat`를 실행하면 아래 3개 작업이 삭제됩니다.
- `DataSchool Check-in`
- `DataSchool Mid-Attendance`
- `DataSchool Check-out`

## 예외일 처리
`skip_dates.txt`에 날짜를 추가하면 해당 날짜는 자동 스킵됩니다.

예시:
```txt
2026-04-23
2026-05-01
```

## 입실/퇴실 동작 방식
- Atosoft 로그인 페이지(`slogin.asp`)에 먼저 접근해 세션 생성
- 이름 검색으로 `strCode` 조회
- 비밀번호 base64 인코딩 후 로그인
- 세션 쿠키 기반으로 입실/퇴실 요청
- 이미 처리된 경우 현재 기록된 시간을 팝업으로 표시

## 금요일 퇴실 추가 기능
금요일에 퇴실 처리(또는 이미 퇴실 처리된 상태 확인)를 하면,
최근 5일 출결현황도 같이 조회해서 팝업에 표시합니다.

표시 예시:
- `17:55 퇴실 완료`
- `최근 5일 출결: 훈련일수 4일 / 출석일수 4일 / 출석률 100.0%`

## 중간출결 동작 방식
- 별도 사이트 API 사용
- 출석 코드 조회 후 제출 반복
- 성공하면 팝업 표시
- 실패/시간 초과도 팝업 표시
