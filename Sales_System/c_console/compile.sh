#!/bin/bash
echo "Compiling Sales System C Console Version..."
gcc main.c -o main
if [ $? -ne 0 ]; then
    echo "Compilation failed!"
    exit 1
fi
echo "Compilation successful!"
chmod +x main
