#!/bin/bash

echo "========================================"
echo "学生信息管理系统编译脚本"
echo "========================================"
echo ""

echo "正在编译main.c..."
gcc main.c -o main -std=c99

if [ $? -eq 0 ]; then
    echo ""
    echo "编译成功！"
    echo ""
    echo "运行程序请输入: ./main"
    echo ""
    echo "首次使用密码: admin123"
    echo ""
    echo "注意：Linux系统可能需要安装ncurses库"
    echo "安装命令: sudo apt-get install libncurses5-dev"
    echo ""
else
    echo ""
    echo "编译失败！请检查是否安装了gcc编译器"
    echo ""
    echo "Ubuntu/Debian安装命令:"
    echo "sudo apt-get install gcc"
    echo ""
    echo "CentOS/RHEL安装命令:"
    echo "sudo yum install gcc"
    echo ""
fi
