@echo off
chcp 65001 >nul
title Flutter 文檔建構工具

echo 🚀 Flutter 文檔建構工具
echo ================================

:: 檢查 Python 是否安裝
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安裝，請先安裝 Python
    pause
    exit /b 1
)

:: 檢查並安裝必要套件
echo 📦 檢查必要套件...

python -c "import markdown" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 安裝 markdown 套件...
    pip install markdown
)

python -c "import yaml" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 安裝 PyYAML 套件...
    pip install PyYAML
)

:: 處理參數
if "%1"=="init" goto init
if "%1"=="build" goto build
if "%1"=="help" goto help
if "%1"=="-h" goto help
if "%1"=="--help" goto help
if "%1"=="" goto build

echo ❌ 未知參數: %1
echo 使用 'build.bat help' 查看使用方法
pause
exit /b 1

:init
echo 🎯 初始化專案結構...
python builder.py --init
goto end

:build
echo 🔨 建構文檔...
python builder.py
goto end

:help
echo 使用方法：
echo   build.bat init    - 初始化專案結構
echo   build.bat build   - 建構文檔（預設）
echo   build.bat help    - 顯示此說明
goto end

:end
echo.
echo ✅ 操作完成
pause