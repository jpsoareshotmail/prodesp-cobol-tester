@echo off
echo ========================================
echo Sistema de Testes COBOL - Interface Web
echo ========================================
echo.

REM Verificar se Python está instalado
python3 --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python 3 não encontrado!
    echo Instale Python 3 de: https://www.python.org/
    pause
    exit /b 1
)

REM Verificar/criar ambiente virtual
if not exist "venv" (
    echo [*] Criando ambiente virtual...
    python3 -m venv venv
)

REM Ativar ambiente virtual
echo [*] Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências
echo [*] Instalando dependências...
pip install -q -r requirements.txt

echo.
echo ✓ Ambiente pronto!
echo.
echo ========================================
echo Ww Abrindo interface web...
echo ========================================
echo.
echo URL: http://localhost:5000
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

REM Abrir navegador
start http://localhost:5000

REM Iniciar servidor Flask
python3 web_app.py
