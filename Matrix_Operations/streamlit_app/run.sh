#!/bin/bash

echo "========================================"
echo "  矩阵运算系统 - Streamlit网页版"
echo "========================================"
echo ""

# 检查是否安装了依赖
python3 -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[提示] 未检测到Streamlit，正在安装依赖..."
    echo ""
    pip3 install -r requirements.txt
    echo ""
fi

# 运行程序
echo "[启动] 正在启动Streamlit应用..."
echo "[注意] 浏览器将自动打开，如未打开请访问: http://localhost:8501"
echo ""
streamlit run app.py
