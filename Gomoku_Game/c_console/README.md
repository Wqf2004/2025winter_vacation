# 五子棋游戏 - C语言控制台版

## 功能特点

- 三种对弈模式：计-人、人-计、人-人
- 使用Unicode字符绘制棋盘
- 智能AI对手（基于价值评估）
- 悔棋功能
- 游戏存档功能
- 胜负判定

## 编译和运行

### Windows
```bash
# 编译
compile.bat

# 运行
main.exe
```

### Linux/Mac
```bash
# 编译
chmod +x compile.sh
./compile.sh

# 运行
./main
```

## 操作说明

- 格式：`x y` - 在坐标(x,y)落子
- 输入 `u` - 悔棋
- 输入 `q` - 退出游戏

## 游戏规则

- 黑方先手
- 五子连珠获胜
- 支持悔棋和存档

## AI策略

AI基于位置价值评估，考虑：
- 连珠数量（活二、活三、活四等）
- 阻挡对手
- 位置优势（靠近中心）

## 文件结构

```
c_console/
├── main.c          # 主程序
├── compile.bat     # Windows编译脚本
├── compile.sh      # Linux/Mac编译脚本
└── README.md       # 说明文档
```

## 数据文件

程序会在 `../dataset/` 目录下创建以下文件：
- `save.txt`: 游戏存档
