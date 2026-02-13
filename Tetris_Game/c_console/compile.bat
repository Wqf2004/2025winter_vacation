@echo off
echo ========================================
echo Compiling Tetris Game...
echo ========================================
echo.

echo [1/3] Compiling tetris_ai.c...
gcc -c tetris_ai.c -o tetris_ai.o
if %errorlevel% neq 0 (
    echo FAILED to compile tetris_ai.c!
    pause
    exit /b 1
)
echo       Done

echo.
echo [2/3] Compiling imitation_learning.c...
gcc -c imitation_learning.c -o imitation_learning.o
if %errorlevel% neq 0 (
    echo FAILED to compile imitation_learning.c!
    pause
    exit /b 1
)
echo       Done

echo.
echo [3/3] Compiling main.c...
gcc -o main.exe main.c tetris_ai.o imitation_learning.o -lwinmm -lm
if %errorlevel% neq 0 (
    echo FAILED to compile main.c!
    pause
    exit /b 1
)
echo       Done

echo.
echo [3/3] Compiling train_ai.c...
gcc -o train_ai.exe train_ai.c tetris_ai.o -lm
if %errorlevel% neq 0 (
    echo FAILED to compile train_ai.c!
    pause
    exit /b 1
)
echo       Done

echo.
echo ========================================
echo Compilation SUCCESS!
echo ========================================
echo.
echo Executables:
echo   - main.exe        (Main game)
echo   - train_ai.exe    (AI training)
echo.
echo Run game: .\main.exe
echo Run training: .\train_ai.exe
echo.
pause
