:: ================================================== ::

:: ~~ Script para instalar todas as dependências do projeto.
@echo off
chcp 65001 >nul
echo Instalando...
winget install 9PNRBTZXMB4Z
pip install --upgrade pip
pip install selenium
pip install --upgrade selenium
pip install xlwings
pip install --upgrade xlwings
pip install openpyxl
pip install --upgrade openpyxl
pip install pywin32
pip install --upgrade pywin32
pip install pandas
pip install --upgrade pandas
pip install keyboard
pip install --upgrade keyboard
pip install requests
pip install --upgrade requests
pip install dotenv
pip install --upgrade dotenv
pip install rich
pip install --upgrade rich
pip install setuptools
pip install --upgrade setuptools
pip install tabulate
pip install --upgrade tabulate
pip install django
pip install --upgrade django
pip install fastapi
pip install --upgrade fastapi
pip install uvicorn
pip install --upgrade uvicorn
echo Instalação finalizada.

:: ================================================== ::