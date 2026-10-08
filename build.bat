@echo off
chcp 936 >nul
setlocal
cd /d "%~dp0"
echo ============================================
echo   RDR2 Cheat Paster - Build EXE
echo ============================================
echo.
echo [1/2] installing dependencies...
python -m pip install --quiet pynput pyinstaller
if errorlevel 1 goto fail
echo [2/2] building exe...
python -m PyInstaller --noconfirm --clean --onefile --noconsole ^
  --name "RDR2作弊码速贴器" ^
  --hidden-import pynput.keyboard._win32 ^
  --hidden-import pynput.mouse._win32 ^
  rdr2_cheat_paster.py
if errorlevel 1 goto fail
echo.
echo [OK] build finished. output: dist\RDR2作弊码速贴器.exe
pause
exit /b 0
:fail
echo.
echo [NG] build failed. check the messages above.
pause
exit /b 1
