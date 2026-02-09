#!/bin/bash

echo "========================================"
echo "  矩阵运算系统 - PyQt5桌面版"
echo "========================================"
echo ""

# 检查是否安装了依赖
python3 -c "import PyQt5" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[提示] 未检测到PyQt5，正在安装依赖..."
    echo ""
    pip3 install -r requirements.txt
    echo ""
fi

# 运行程序
echo "[启动] 正在启动程序..."
python3 main.py
