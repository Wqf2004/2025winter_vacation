@echo off
chcp 65001 >nul
echo ========================================
echo     出勤管理系统 - PyQt5桌面版
echo ========================================
echo.

REM 检查是否安装了依赖
python -c "import PyQt5" 2>nul
if errorlevel 1 (
    echo 未检测到PyQt5，正在安装依赖...
    pip install -r requirements.txt
    echo.
)

echo 启动系统...
python main.py

pause
