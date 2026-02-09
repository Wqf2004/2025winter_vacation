@echo off
echo 正在编译扫雷游戏 (C语言控制台版)...
gcc main.c -o main.exe
if %errorlevel% == 0 (
    echo 编译成功！
    echo.
    echo 运行命令: main.exe
) else (
    echo 编译失败！
)
pause
