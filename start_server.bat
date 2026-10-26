@echo off
title ArchiCheck Server
echo Starting ArchiCheck Server on http://0.0.0.0:5000 ...
cd /d "%~dp0"
python server.py
pause
