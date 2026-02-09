#!/bin/bash
echo "正在编译五子棋游戏 (C语言控制台版)..."
gcc main.c -o main
if [ $? -eq 0 ]; then
    echo "编译成功！"
    echo ""
    echo "运行命令: ./main"
else
    echo "编译失败！"
fi
