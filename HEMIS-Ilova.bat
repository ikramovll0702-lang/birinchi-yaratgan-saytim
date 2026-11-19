@echo off
title HEMIS - Oliy Ta'lim Boshqaruv Tizimi
cd /d "%~dp0"

echo ========================================================
echo    HEMIS - Oliy Ta'lim Muassasasi Talabalar Tizimi
echo    Dastur ishga tushirilmoqda, iltimos kuting...
echo ========================================================
echo.

python desktop_app.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [XATOLIK] Dasturni ishga tushirishda xatolik yuz berdi.
    echo Iltimos, Python va kerakli kutubxonalar ornatilganligini tekshiring:
    echo pip install -r requirements.txt
    pause
)
