# DataSchool Auto Check-in

## 포함 파일
- `attendance_session_based.py`: 세션 기반 입퇴실 스크립트
- `run_checkin.bat`: 입실 수동 실행
- `run_checkout.bat`: 퇴실 수동 실행
- `register_tasks.bat`: 작업 스케줄러 자동 등록
- `remove_tasks.bat`: 등록된 작업 스케줄러 삭제
- `skip_dates.txt`: 예외일 목록

## 사용 전 설정
1. `attendance_session_based.py` 상단에서 아래 값 수정
   - `NAME = '본인 이름 입력'`
   - `PASSWORD = '본인 비밀번호 입력'`
2. Python 설치 확인
3. 필요하면 `skip_dates.txt`에 `YYYY-MM-DD` 형식으로 예외일 추가

## 작업 스케줄러 등록
- `register_tasks.bat`를 실행하면 아래 2개 작업이 등록됩니다.
  - `DataSchool Check-in` → 기본 08:55
  - `DataSchool Check-out` → 기본 17:55
- 시간은 작업 스케줄러에서 자유롭게 수정 가능합니다.

## 작업 스케줄러 삭제
- `remove_tasks.bat`를 실행하면 아래 2개 작업이 삭제됩니다.
  - `DataSchool Check-in`
  - `DataSchool Check-out`

## 동작 방식
- 실행 후 로그인 세션을 만든 뒤 입실/퇴실 요청
- 이미 처리된 경우 현재 기록된 시간을 표시
- 성공/스킵/실패 결과를 콘솔 출력 + Windows 팝업으로 표시

## 예외일 처리
- `skip_dates.txt`에 날짜를 추가하면 해당 날짜는 자동 스킵됩니다.
- 형식 예시:
  - `2026-04-23`
  - `2026-05-01`
