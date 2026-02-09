# 五子棋游戏 - PyQt5桌面版

## 功能特点

- 图形化界面
- 三种对弈模式：人-人、人-计、计-人
- 鼠标点击落子
- 智能AI对手
- 悔棋功能
- 游戏存档/读取
- 鼠标预览落子位置
- 最后一步高亮显示

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

- 点击棋盘落子
- 悔棋：撤销最近两步
- 保存：保存对局记录
- 读取：读取存档继续游戏

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
    └── main_window.py  # 主窗口
```

## 数据文件

程序会在 `../dataset/` 目录下创建以下文件：
- `save.txt`: 游戏存档
