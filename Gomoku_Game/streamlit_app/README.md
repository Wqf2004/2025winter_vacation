# 五子棋游戏 - Streamlit网页版

## 功能特点

- 网页化界面
- 三种对弈模式：人-人、人-计、计-人
- 在线对战
- 智能AI对手
- 悔棋功能
- 游戏存档/读取
- 响应式设计

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行

### Windows
```bash
run.bat
```

### Linux/Mac
```bash
chmod +x run.sh
./run.sh
```

或者直接运行：
```bash
streamlit run app.py
```

## 操作说明

- 输入行列号选择位置
- 点击"落子"按钮进行落子
- 悔棋：撤销最近两步
- 保存/读取：存档管理

## 文件结构

```
streamlit_app/
├── app.py              # 主程序
├── data_manager.py     # 数据管理模块
├── requirements.txt    # 依赖包
├── run.bat            # Windows启动脚本
├── run.sh             # Linux/Mac启动脚本
└── README.md          # 说明文档
```

## 数据文件

程序会在 `../dataset/` 目录下创建以下文件：
- `save.txt`: 游戏存档
