# 班级同学信息管理系统

**✅ 已完成** - 提供三个不同技术栈的版本

## 项目概述

班级同学信息管理系统用于管理班级同学的基本信息，支持信息录入、查询、修改、删除等功能。本项目提供了三个版本，满足不同使用场景的需求。

## 版本对比

| 特性                 | C语言控制台版 | PyQt5桌面版    | Streamlit网页版        |
| -------------------- | ------------- | -------------- | ---------------------- |
| **界面类型**   | 命令行界面    | 桌面GUI应用    | Web网页应用            |
| **技术栈**     | C语言         | Python + PyQt5 | Python + Streamlit     |
| **安装复杂度** | 需编译        | 需安装PyQt5    | 需安装Streamlit        |
| **使用方式**   | 本地终端运行  | 本地桌面运行   | 浏览器访问（支持远程） |
| **界面美观度** | 基础文本界面  | 现代化桌面界面 | 现代化网页界面         |
| **跨平台**     | 需重新编译    | 完全支持       | 完全支持               |
| **远程访问**   | 不支持        | 需远程桌面     | 原生支持               |
| **适用场景**   | 学习研究      | 个人使用       | 局域网/云端部署        |

## 功能需求

✅ 同学信息录入
✅ 信息查询
✅ 信息修改
✅ 信息删除
✅ 数据统计
✅ 通讯录导出（保存到文件）

## 版本规划

- C语言控制台版 ✅
- PyQt5桌面版 ✅
- Streamlit网页版 ✅

## 开发进度

- [x] 版本一：C语言控制台版
- [x] 版本二：PyQt5桌面版
- [x] 版本三：Streamlit网页版

## 目录结构

```
Classmate_Information_Management_System/
├── c_console/           # C语言控制台版
│   ├── main.c
│   ├── compile.bat
│   ├── compile.sh
│   └── README.md
├── pyqt5_gui/          # PyQt5桌面版
│   ├── main.py
│   ├── data_manager.py
│   ├── requirements.txt
│   ├── README.md
│   ├── run.bat
│   └── ui/
│       ├── __init__.py
│       ├── login_dialog.py
│       └── main_window.py
├── streamlit_app/       # Streamlit网页版
│   ├── app.py
│   ├── data_manager.py
│   ├── requirements.txt
│   ├── README.md
│   └── run.bat
└── dataset/
    ├── students.txt       # 学生数据文件
    └── password.txt     # 密码文件
```

## 完成时间

- **C语言控制台版**：2026年2月
- **PyQt5桌面版**：2026年2月
- **Streamlit网页版**：2026年2月
