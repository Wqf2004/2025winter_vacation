# 扫雷游戏 - Streamlit网页版

## 功能特点

- 网页化界面
- 用户登录和注册系统
- 三种难度选择
- 在线排行榜
- 响应式设计
- 数据持久化存储

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

- 输入行和列号选择格子
- 选择操作类型（翻开或标记）
- 点击执行按钮进行操作

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
- `user.txt`: 用户数据
- `rank.txt`: 排行榜数据
