@echo off
echo 正在启动五子棋游戏 (PyQt5版本)...
echo.
python main.py
if %errorlevel% neq 0 (
    echo.
    echo 启动失败！请确保已安装依赖包。
    echo 运行命令: pip install -r requirements.txt
)
pause
