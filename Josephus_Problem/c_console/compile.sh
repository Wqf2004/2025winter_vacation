#!/bin/bash

echo "编译C语言程序..."
gcc main.c -o main -Wall

if [ $? -eq 0 ]; then
    echo "编译成功！"
    echo "运行程序..."
    ./main
else
    echo "编译失败！"
fi
