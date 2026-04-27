@echo off
cd /d %~dp0
py -3 src\attendance.py --action out
