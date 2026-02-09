@echo off
echo 编译C语言程序...
gcc main.c -o main.exe -Wall

if %errorlevel% equ 0 (
    echo 编译成功！
    echo 运行程序...
    main.exe
) else (
    echo 编译失败！
)

pause
