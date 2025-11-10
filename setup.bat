@echo off
echo ========================================
echo    EXPRESSIFY - Setup Environment
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan! Silakan install Python terlebih dahulu.
    echo Download di: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Membuat virtual environment...
python -m venv venv

echo [2/4] Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Mengupgrade pip...
python -m pip install --upgrade pip

echo [4/4] Menginstall dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo    Setup Berhasil! 🎉
echo ========================================
echo.
echo Untuk menjalankan game:
echo 1. Aktifkan environment: venv\Scripts\activate
echo 2. Jalankan game: python src/main.py
echo.
pause
