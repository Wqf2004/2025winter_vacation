# 扫雷游戏 - PyQt5桌面版

## 功能特点

- 图形化用户界面
- 用户登录和注册系统
- 三种难度选择
- 鼠标左键翻开，右键标记
- 实时计时和剩余雷数显示
- 排行榜功能
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
python main.py
```

## 操作说明

- 左键点击：翻开格子
- 右键点击：标记/取消标记地雷
- 新游戏：重新开始

## 文件结构

```
pyqt5_gui/
├── main.py              # 主程序入口
├── data_manager.py      # 数据管理模块
├── requirements.txt     # 依赖包
├── run.bat             # Windows启动脚本
├── run.sh              # Linux/Mac启动脚本
└── ui/
    ├── __init__.py
    ├── login_dialog.py # 登录/注册对话框
    └── main_window.py  # 主窗口
```

## 数据文件

程序会在 `../dataset/` 目录下创建以下文件：
- `user.txt`: 用户数据
- `rank.txt`: 排行榜数据
