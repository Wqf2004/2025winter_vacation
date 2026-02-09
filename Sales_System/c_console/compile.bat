@echo off
echo Compiling Sales System C Console Version...
gcc main.c -o main.exe
if errorlevel 1 (
    echo Compilation failed!
    pause
    exit /b 1
)
echo Compilation successful!
pause
