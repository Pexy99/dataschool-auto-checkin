#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config

ALLOWED_KEYS = {
    'CHECKIN_TIME',
    'MID_ATTENDANCE_START',
    'MID_ATTENDANCE_END',
    'MID_ATTENDANCE_POLL_SECONDS',
    'CHECKOUT_TIME',
}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in ALLOWED_KEYS:
        print('')
        return 1
    print(getattr(config, sys.argv[1]))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
