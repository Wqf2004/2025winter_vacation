#!/bin/bash
echo "编译电话簿管理系统..."
gcc main.c -o main
if [ $? -eq 0 ]; then
    echo "编译成功！"
    echo ""
    echo "运行程序..."
    ./main
else
    echo "编译失败！"
fi
