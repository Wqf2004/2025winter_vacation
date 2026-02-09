@echo off
chcp 65001 >nul
echo =========================================
echo   Josephus环问题 - Streamlit网页版
echo =========================================
echo.

echo 启动Streamlit应用...
streamlit run app.py

echo.
echo 应用已关闭
pause
