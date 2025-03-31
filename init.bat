:: ================================================== ::

:: ~~ Script para iniciar servers.
@echo off
chcp 65001 >nul

:: ~~ Inicia o servidor Django.
start wt -w 0 nt -d . --title "Main Server                              " cmd /k "python manage.py runserver"

:: ~~ Tempo de espera.
timeout /t 5 /nobreak >nul

:: ~~ Inicia o servidor WebDriver.
wt -w 0 nt -d . --title "App Instance                               " cmd /k "python -m uvicorn scripts.instance:app --host 127.0.0.1 --port 5001"

:: ================================================== ::