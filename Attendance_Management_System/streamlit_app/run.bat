@echo off
chcp 65001 >nul
echo ========================================
echo     出勤管理系统 - Streamlit网页版
echo ========================================
echo.

REM 检查是否安装了依赖
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo 未检测到Streamlit，正在安装依赖...
    pip install -r requirements.txt
    echo.
)

echo 启动系统...
streamlit run app.py

pause
