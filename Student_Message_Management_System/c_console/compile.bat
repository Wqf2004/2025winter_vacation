@echo off
chcp 936 > nul
echo ========================================
echo 学生信息管理系统编译脚本
echo ========================================
echo.

echo 正在编译main.c...
gcc main.c -o main.exe

if %errorlevel% == 0 (
    echo.
    echo 编译成功！
    echo.
    echo 运行程序请输入: main.exe
    echo 或直接双击main.exe文件
    echo.
    echo 首次使用密码: admin123
    echo.
) else (
    echo.
    echo 编译失败！请检查是否安装了gcc编译器
    echo.
    echo 下载MinGW-w64: https://www.mingw-w64.org/
    echo 或使用Visual Studio编译
    echo.
)

pause
