@echo off
chcp 65001 >nul
echo ========================================
echo   矩阵运算系统 - PyQt5桌面版
echo ========================================
echo.

REM 检查是否安装了依赖
python -c "import PyQt5" 2>nul
if errorlevel 1 (
    echo [提示] 未检测到PyQt5，正在安装依赖...
    echo.
    pip install -r requirements.txt
    echo.
)

REM 运行程序
echo [启动] 正在启动程序...
python main.py

pause
