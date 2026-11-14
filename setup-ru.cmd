@echo off
chcp 65001 >nul
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" python -m venv .venv
if errorlevel 1 goto error
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto error
".venv\Scripts\python.exe" setup_demo.py
if errorlevel 1 goto error
echo Установка завершена. Запустите start-ru.cmd
pause
exit /b 0
:error
echo Не удалось завершить установку. Проверьте сообщение выше.
pause
exit /b 1
