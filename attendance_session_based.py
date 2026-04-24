#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import ctypes
import datetime as dt
import http.cookiejar
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

# ===== 사용자 설정 =====
NAME = '본인 이름 입력'
PASSWORD = '본인 비밀번호 입력'
STR_CCODE = 'W260315002'
# ======================

BASE = 'https://microsoft.atosoft.net/worknet/'
SEARCH_URL = BASE + 'ajax_stu_search.asp'
LOGIN_PAGE_URL = BASE + 'slogin.asp'
LOGIN_URL = BASE + 'SLogin_ok.asp'
PRESENT_PAGE = BASE + 'present/presentD.asp'
PRESENT_IN_URL = BASE + 'present/PresentIn_ok.asp'
PRESENT_OUT_URL = BASE + 'present/PresentOut_ok.asp'
ROLLBOOK_URL = BASE + 'present/PresentRollBookChk.asp'
SUMMARY_URL = BASE + '_popup/student/_stuPresentList.asp'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'
SKIP_DATES_PATH = Path(__file__).with_name('skip_dates.txt')


def is_windows() -> bool:
    return sys.platform.startswith('win')


def show_popup(message: str, title: str = '출결 자동화') -> None:
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


def today_local() -> str:
    return dt.date.today().isoformat()


def to_js_unicode_percent(text: str) -> str:
    return ''.join(f'%u{ord(ch):04X}' for ch in text)


def encode_euckr_percent(text: str) -> str:
    return urllib.parse.quote_from_bytes(text.encode('euc-kr'))


def build_opener() -> urllib.request.OpenerDirector:
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    opener.addheaders = [('User-Agent', USER_AGENT)]
    return opener


def fetch_text(opener: urllib.request.OpenerDirector, url: str, *, data: bytes | None = None, headers: dict[str, str] | None = None) -> str:
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with opener.open(req, timeout=20) as resp:
        raw = resp.read()
        ctype = resp.headers.get_content_charset() or ''
        enc = ctype or 'euc-kr'
        return raw.decode(enc, errors='replace')


def find_str_code(opener: urllib.request.OpenerDirector, name: str) -> str:
    query = urllib.parse.urlencode({'term': to_js_unicode_percent(name)})
    text = fetch_text(opener, SEARCH_URL + '?' + query)
    data = json.loads(text)
    if not data:
        raise RuntimeError('이름 검색 결과가 없습니다.')
    value = str(data[0]['value'])
    try:
        _, str_code = value.split('<@>', 1)
    except ValueError as e:
        raise RuntimeError(f'strCode 파싱 실패: {value}') from e
    return str_code.strip()


def bootstrap_login_session(opener: urllib.request.OpenerDirector) -> str:
    return fetch_text(opener, LOGIN_PAGE_URL)


def login(opener: urllib.request.OpenerDirector, name: str, str_code: str, password: str) -> str:
    encoded_name = encode_euckr_percent(name)
    encoded_password = base64.b64encode(password.encode()).decode()
    form_text = (
        'strPrevUrl=&'
        f'strSName={encoded_name}&'
        f'strCode={str_code}&'
        'strLoginPwd=&'
        f'strLoginPwd1={encoded_password}'
    )
    form = form_text.encode('ascii')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': LOGIN_PAGE_URL,
        'Origin': 'https://microsoft.atosoft.net',
    }
    return fetch_text(opener, LOGIN_URL, data=form, headers=headers)


def open_present_page(opener: urllib.request.OpenerDirector, str_code: str, name: str) -> str:
    encoded_name = encode_euckr_percent(name)
    url = PRESENT_PAGE + '?' + f'strCode={str_code}&strCCode={STR_CCODE}&strName={encoded_name}'
    return fetch_text(opener, url, headers={'Referer': BASE + f'SMember/index.asp?strCode={str_code}'})


def get_rollbook(opener: urllib.request.OpenerDirector, str_code: str) -> tuple[str, str]:
    query = urllib.parse.urlencode({'strCode': str_code, 'strCCode': STR_CCODE})
    text = fetch_text(opener, ROLLBOOK_URL + '?' + query)
    parts = text.strip().split('|', 1)
    in_time = parts[0].strip() if parts and parts[0].strip() else ''
    out_time = parts[1].strip() if len(parts) > 1 and parts[1].strip() else ''
    return in_time, out_time


def run_action(opener: urllib.request.OpenerDirector, action: str, str_code: str) -> str:
    url = PRESENT_IN_URL if action == 'in' else PRESENT_OUT_URL
    query = urllib.parse.urlencode({'strCode': str_code, 'strCCode': STR_CCODE})
    return fetch_text(opener, url + '?' + query, headers={'Referer': PRESENT_PAGE + f'?strCode={str_code}&strCCode={STR_CCODE}'})


def fetch_attendance_summary(
    opener: urllib.request.OpenerDirector,
    str_code: str,
    name: str,
    start_day: str,
    end_day: str,
) -> tuple[str, str, str] | None:
    params = urllib.parse.urlencode(
        {
            'strCCode': STR_CCODE,
            'strCode': str_code,
            'Sday1': start_day,
            'Sday2': end_day,
        }
    )
    html = fetch_text(opener, SUMMARY_URL + '?' + params)
    import re

    pattern = re.compile(
        rf'<td[^>]*>\s*<center>{re.escape(name)}</center>\s*</td>\s*'
        r'<td[^>]*>\s*<center>(\d+)</center>\s*</td>\s*'
        r'<td[^>]*>\s*<center>(\d+)</center>\s*</td>\s*'
        r'<td[^>]*>\s*<center>\d+</center>\s*</td>\s*'
        r'<td[^>]*>\s*<center>\d+</center>\s*</td>\s*'
        r'<td[^>]*>\s*<center>\d+</center>\s*</td>\s*'
        r'<td[^>]*>\s*<center>\d+</center>\s*</td>\s*'
        r'<td[^>]*>\s*<center>([0-9.]+)</center>\s*</td>',
        re.S,
    )
    match = pattern.search(html)
    if not match:
        return None
    return match.group(1), match.group(2), match.group(3)


def build_friday_summary_message(
    opener: urllib.request.OpenerDirector,
    str_code: str,
    base_message: str,
) -> str:
    if dt.date.today().weekday() != 4:
        return base_message
    start_day = (dt.date.today() - dt.timedelta(days=4)).isoformat()
    end_day = dt.date.today().isoformat()
    summary = fetch_attendance_summary(opener, str_code, NAME, start_day, end_day)
    if not summary:
        return base_message
    training_days, attendance_days, attendance_rate = summary
    return (
        base_message
        + f'\n최근 5일 출결: 훈련일수 {training_days}일 / '
        + f'출석일수 {attendance_days}일 / 출석률 {attendance_rate}%'
    )


def finish(message: str, *, popup: bool) -> int:
    print(message)
    if popup:
        show_popup(message)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description='세션 기반 Atosoft 입퇴실')
    parser.add_argument('--action', choices=['in', 'out'], required=True)
    parser.add_argument('--no-popup', action='store_true')
    args = parser.parse_args()

    if NAME == '본인 이름 입력' or PASSWORD == '본인 비밀번호 입력':
        return finish('사용 전 attendance_session_based.py 상단의 NAME, PASSWORD를 수정하세요.', popup=not args.no_popup)

    today = today_local()
    if today in load_skip_dates():
        return finish(f'{today} 예외일이라 스킵', popup=not args.no_popup)

    opener = build_opener()
    str_code = find_str_code(opener, NAME)
    print(f'str_code={str_code}')

    bootstrap_login_session(opener)
    login_result = login(opener, NAME, str_code, PASSWORD)
    login_failed = '로그인 실패' in login_result or '아이디 또는 비밀번호' in login_result
    if login_failed:
        return finish('로그인 실패', popup=not args.no_popup)

    open_present_page(opener, str_code, NAME)
    before_in, before_out = get_rollbook(opener, str_code)

    if args.action == 'in' and before_in:
        return finish(f'{before_in} 입실 이미 처리됨', popup=not args.no_popup)
    if args.action == 'out' and before_out:
        message = build_friday_summary_message(opener, str_code, f'{before_out} 퇴실 이미 처리됨')
        return finish(message, popup=not args.no_popup)

    result = run_action(opener, args.action, str_code).strip()
    print(f'action_result={result or "-"}')

    after_in, after_out = get_rollbook(opener, str_code)
    final_time = after_in if args.action == 'in' else after_out
    action_label = '입실' if args.action == 'in' else '퇴실'

    if final_time:
        message = f'{final_time} {action_label} 완료'
        if args.action == 'out':
            message = build_friday_summary_message(opener, str_code, message)
        return finish(message, popup=not args.no_popup)
    return finish(f'{action_label} 처리 결과 확인 필요 (응답: {result or "-"})', popup=not args.no_popup)


if __name__ == '__main__':
    sys.exit(main())
