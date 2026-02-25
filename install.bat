@echo off
chcp 65001 >nul
title Fuck Win11 — Kurulum

echo.
echo ╔══════════════════════════════════════╗
echo ║   Fuck Win11 — Kurulum Kontrolü      ║
echo ╚══════════════════════════════════════╝
echo.

:: Python kontrolü
echo [1/2] Python kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo  HATA: Python bulunamadi!
    echo  https://www.python.org/downloads/ adresinden Python 3.8+ indirin.
    echo  Kurulumda "Add Python to PATH" kutusunu isaretleyin!
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo  OK: Python %PYVER% bulundu.
echo.

:: tkinter kontrolü
echo [2/2] tkinter kontrol ediliyor...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo  HATA: tkinter bulunamadi!
    echo  Python'u resmi siteden yeniden kurun (tkinter varsayilan olarak gelir).
    echo.
    pause
    exit /b 1
)
echo  OK: tkinter mevcut.
echo.

echo ══════════════════════════════════════
echo  Tum gereksinimler karsilandi!
echo  Bu program icin pip install gerekmez.
echo  Tum kutuphaneler Python ile birlikte gelir.
echo.
echo  Baslatmak icin:
echo    python win11_system_repair.py
echo  (Sag tik - Yonetici olarak calistir)
echo ══════════════════════════════════════
echo.
pause
