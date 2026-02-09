# 矩阵运算

**✅ 已完成** - C语言控制台版提供两种参数传递方式

## 项目概述

矩阵运算程序用于实现矩阵的各种数学运算，包括加减乘、转置、求逆、三角化等功能。本项目实现了题目要求的所有功能，并使用两种不同的参数传递方式。

## 功能需求

✅ 矩阵加法
✅ 矩阵减法
✅ 矩阵乘法
✅ 矩阵转置
✅ 矩阵求逆
✅ 矩阵三角化

## 版本规划

- C语言控制台版 ✅
- PyQt5桌面版 - 待定
- Streamlit网页版 - 待定

## 开发进度

- [x] 版本一：C语言控制台版
- [ ] 版本二：PyQt5桌面版
- [ ] 版本三：Streamlit网页版

## 目录结构

```
Matrix_Operations/
├── c_console/           # C语言控制台版
│   ├── main.c
│   ├── compile.bat
│   ├── compile.sh
│   └── README.md
├── pyqt5_gui/          # PyQt5桌面版
│   ├── main.py
│   ├── requirements.txt
│   ├── README.md
│   └── ui/
│       ├── __init__.py
│       └── main_window.py
├── streamlit_app/       # Streamlit网页版
│   ├── app.py
│   ├── requirements.txt
│   ├── README.md
│   └── run.bat
└── dataset/
    └── [数据文件（如需要）]
```

## 技术特点

### 实现方式1：参数为二维数组名、行数、列数

```c
void matrix_add_1(double matrix1[MAX_SIZE][MAX_SIZE],
                 double matrix2[MAX_SIZE][MAX_SIZE],
                 double result[MAX_SIZE][MAX_SIZE],
                 int rows, int cols);
```

### 实现方式2：参数为指针、行数、列数

```c
void matrix_add_2(double *matrix1, double *matrix2,
                 double *result, int rows, int cols);
```

## 完成时间

- **C语言控制台版**：2026年2月
