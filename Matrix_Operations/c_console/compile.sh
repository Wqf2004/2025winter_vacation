#!/bin/bash
echo "编译矩阵运算系统..."
gcc main.c -o main
if [ $? -eq 0 ]; then
    echo "编译成功！"
    echo ""
    echo "运行程序..."
    ./main
else
    echo "编译失败！"
fi
