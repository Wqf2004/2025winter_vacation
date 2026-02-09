# 出勤管理系统 - PyQt5桌面版

## 功能特性

- 图形化用户界面
- 职工打卡记录处理
- 出勤情况查询（按编号、全勤、请假、旷工）
- 请假管理功能
- 统计分析功能
- 排序功能
- 登录验证

## 环境要求

- Python 3.7+
- PyQt5

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行方法

### Windows
```bash
# 双击运行
run.bat

# 或命令行运行
python main.py
```

### Linux/macOS
```bash
python main.py
```

## 文件说明

- `main.py` - 主程序入口
- `data_manager.py` - 数据管理模块
- `ui/` - UI模块目录
  - `main_window.py` - 主窗口
  - `login_dialog.py` - 登录对话框
- `requirements.txt` - Python依赖列表
- `run.bat` - Windows启动脚本

## 默认密码

admin123

## 使用说明

1. 运行程序后输入密码登录
2. 使用左侧菜单选择功能
3. 在查询页面选择不同的查询方式
4. 在请假页面录入请假信息
5. 在统计页面查看统计数据
6. 在排序页面查看排序结果

## 技术栈

- PyQt5 - GUI框架
- Python 3.7+ - 开发语言
