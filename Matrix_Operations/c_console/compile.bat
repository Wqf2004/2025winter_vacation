@echo off
echo 编译矩阵运算系统...
gcc main.c -o main.exe
if %errorlevel% equ 0 (
    echo 编译成功！
    echo.
    echo 运行程序...
    main.exe
) else (
    echo 编译失败！
)
pause
