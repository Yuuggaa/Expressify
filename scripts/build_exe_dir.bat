@echo off
REM ===================================================
REM Expressify - Build Executable (Directory Mode)
REM Faster startup, larger size
REM ===================================================

echo ========================================
echo Building Expressify Executable (Dir Mode)
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install PyInstaller if not already installed
echo Installing PyInstaller...
pip install pyinstaller
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "*.spec" del /q *.spec
echo.

REM Build executable (directory mode for faster startup)
echo Building executable...
pyinstaller ^
    --name="Expressify" ^
    --onedir ^
    --windowed ^
    --icon="assets/images/icon.ico" ^
    --add-data="assets;assets" ^
    --add-data="src/ui;src/ui" ^
    --hidden-import="mediapipe" ^
    --hidden-import="cv2" ^
    --hidden-import="pygame" ^
    --hidden-import="numpy" ^
    --hidden-import="PIL" ^
    --hidden-import="matplotlib" ^
    --hidden-import="matplotlib.pyplot" ^
    --collect-data="mediapipe" ^
    --noconsole ^
    src/main.py

echo.
echo ========================================
echo Build Complete!
echo Executable location: dist\Expressify\Expressify.exe
echo ========================================
echo.
echo Note: Distribute the entire 'dist\Expressify' folder
pause
