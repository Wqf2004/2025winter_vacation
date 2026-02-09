# 扫雷游戏 - C语言控制台版

## 功能特点

- 用户登录和注册系统
- 文件存储用户数据和游戏成绩
- 三种难度选择（简单、中等、困难）
- 雷区标记功能
- 实时计时
- 排行榜显示

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

- 格式：`行 列 操作`
  - 操作 `1`: 翻开格子
  - 操作 `0`: 标记/取消标记地雷
  - 输入 `q`: 退出游戏

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
- `user.txt`: 用户账号密码和最佳成绩
- `rank.txt`: 游戏成绩排行榜
