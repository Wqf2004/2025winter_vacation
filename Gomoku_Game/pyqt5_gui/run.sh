#!/bin/bash
echo "正在启动五子棋游戏 (PyQt5版本)..."
echo ""
python3 main.py
if [ $? -ne 0 ]; then
    echo ""
    echo "启动失败！请确保已安装依赖包。"
    echo "运行命令: pip install -r requirements.txt"
fi
