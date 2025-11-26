@echo off
REM ===================================================
REM Expressify - Build Both Versions (Portable & Install)
REM ===================================================

echo ========================================
echo Building Expressify - All Versions
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install PyInstaller if not already installed
echo Installing/Checking PyInstaller...
pip install pyinstaller
echo.

REM Clean all previous builds
echo Cleaning previous builds...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "*.spec" del /q *.spec
echo.

REM ==========================================
REM BUILD 1: One-File (Portable)
REM ==========================================
echo ========================================
echo [1/2] Building Portable Version...
echo ========================================
pyinstaller ^
    --name="Expressify" ^
    --onefile ^
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
echo Portable build complete!
echo Renaming...
move dist\Expressify.exe dist\Expressify.exe
echo.

REM Clean for next build
rmdir /s /q build

REM ==========================================
REM BUILD 2: One-Directory (Install)
REM ==========================================
echo ========================================
echo [2/2] Building Install Version...
echo ========================================
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
echo Install build complete!
echo.

REM ==========================================
REM CREATE ZIP FOR INSTALL VERSION
REM ==========================================
echo Creating zip for Install version...
cd dist
powershell -Command "Compress-Archive -Path 'Expressify' -DestinationPath 'Expressify.zip' -Force"
cd ..
echo.

REM ==========================================
REM SUMMARY
REM ==========================================
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Portable Version:
echo   - dist\Expressify.exe
echo   - Size: ~150-200 MB
echo   - Ready to distribute!
echo.
echo Install Version:
echo   - dist\Expressify.zip
echo   - Size: ~180 MB (zipped)
echo   - User must extract before use
echo.
echo ========================================
echo Next Steps:
echo 1. Test both versions
echo 2. Upload to GitHub Releases
echo ========================================
pause
