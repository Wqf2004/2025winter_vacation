@echo off
chcp 936 > nul
echo ========================================
echo     出勤管理系统 - C控制台版编译脚本
echo ========================================
echo.

gcc main.c -o main.exe

if %ERRORLEVEL% EQU 0 (
    echo.
    echo 编译成功！
    echo.
    echo 运行程序请执行: main.exe
) else (
    echo.
    echo 编译失败！请检查代码。
)

pause
