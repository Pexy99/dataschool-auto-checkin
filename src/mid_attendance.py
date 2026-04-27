#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ctypes
import datetime as dt
import json
import random
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config

CODE_URL = 'https://msdataschool4.azurewebsites.net/api/code'
ATTENDANCE_URL = 'https://msdataschool4.azurewebsites.net/api/attendance'
SKIP_DATES_PATH = ROOT / 'skip_dates.txt'
POLL_SECONDS = 45
RANDOM_DELAY_SECONDS = 10
DEFAULT_START_TIME = '15:30'
DEFAULT_END_TIME = '16:30'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'


def is_windows() -> bool:
    return sys.platform.startswith('win')


def show_popup(message: str, title: str = '중간출결 자동화') -> None:
    if is_windows():
        ctypes.windll.user32.MessageBoxW(0, message, title, 0)


def load_skip_dates() -> set[str]:
    if not SKIP_DATES_PATH.exists():
        return set()
    return {
        line.strip()
        for line in SKIP_DATES_PATH.read_text(encoding='utf-8').splitlines()
        if line.strip() and not line.strip().startswith('#')
    }


def fetch_json(url: str, *, data: bytes | None = None) -> dict:
    req = urllib.request.Request(url, data=data, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read().decode('utf-8', errors='replace')
    return json.loads(raw)


def fetch_code() -> str:
    data = fetch_json(CODE_URL)
    return str(data.get('code', '')).strip()


def submit_attendance(name: str, password: str, code: str) -> dict:
    body = json.dumps({'name': name, 'password': password, 'code': code}).encode('utf-8')
    req = urllib.request.Request(
        ATTENDANCE_URL,
        data=body,
        headers={
            'User-Agent': USER_AGENT,
            'Content-Type': 'application/json',
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read().decode('utf-8', errors='replace')
    return json.loads(raw)


def parse_hhmm(value: str) -> tuple[int, int]:
    hour, minute = value.split(':', 1)
    return int(hour), int(minute)


def today_local() -> dt.date:
    return dt.date.today()


def finish(message: str, *, popup: bool) -> int:
    print(message)
    if popup:
        show_popup(message)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description='MS Data School 중간출결 자동화')
    parser.add_argument('--start-time', default=DEFAULT_START_TIME)
    parser.add_argument('--end-time', default=DEFAULT_END_TIME)
    parser.add_argument('--poll-seconds', type=int, default=POLL_SECONDS)
    parser.add_argument('--random-delay-seconds', type=int, default=RANDOM_DELAY_SECONDS)
    parser.add_argument('--no-popup', action='store_true')
    args = parser.parse_args()

    if not config.MID_ATTENDANCE_NAME or not config.MID_ATTENDANCE_PASSWORD:
        return finish('config.py의 MID_ATTENDANCE_NAME, MID_ATTENDANCE_PASSWORD를 먼저 입력하세요.', popup=not args.no_popup)

    today = today_local()
    if today.isoformat() in load_skip_dates():
        return finish(f'{today.isoformat()} 예외일이라 중간출결 스킵', popup=not args.no_popup)

    start_h, start_m = parse_hhmm(args.start_time)
    end_h, end_m = parse_hhmm(args.end_time)
    start_dt = dt.datetime.combine(today, dt.time(start_h, start_m))
    end_dt = dt.datetime.combine(today, dt.time(end_h, end_m))
    now = dt.datetime.now()

    if now < start_dt:
        wait_seconds = int((start_dt - now).total_seconds())
        print(f'start_wait_seconds={wait_seconds}')
        time.sleep(max(wait_seconds, 0))

    if args.random_delay_seconds > 0:
        delay = random.randint(0, args.random_delay_seconds)
        print(f'random_delay_seconds={delay}')
        time.sleep(delay)

    last_message = ''
    while dt.datetime.now() <= end_dt:
        try:
            code = fetch_code()
            print(f'code={code or "-"}')
            if not code:
                last_message = '출석 코드를 가져오지 못했습니다.'
            else:
                result = submit_attendance(config.MID_ATTENDANCE_NAME, config.MID_ATTENDANCE_PASSWORD, code)
                message = str(result.get('message', '')).strip() or str(result)
                print(f'server_message={message}')
                if '출석이 확인되었습니다' in message:
                    return finish(f'중간출결 완료 ({code})', popup=not args.no_popup)
                last_message = message
        except Exception as e:
            last_message = f'오류: {e}'
            print(last_message)
        time.sleep(max(args.poll_seconds, 1))

    return finish(f'중간출결 실패 또는 시간 초과: {last_message or "응답 없음"}', popup=not args.no_popup)


if __name__ == '__main__':
    sys.exit(main())
