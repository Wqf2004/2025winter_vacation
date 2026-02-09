# 银行账目管理系统

## 项目概述

银行账目管理系统用于管理个人或企业的银行账户，支持开户、借款、还款、存款、查询、排序、统计等功能。

## 功能特性

### 核心功能
- ✅ 开户：创建新账户，自动生成账号
- ✅ 借款：从账户借入资金（余额变负）
- ✅ 还款：偿还借款
- ✅ 存款：存入资金（余额变正）
- ✅ 清户：删除账户（逻辑删除）
- ✅ 文件紧缩：清除已删除账户

### 查询统计
- ✅ 按账号查询账户信息
- ✅ 查询最大借款账户
- ✅ 查询最大存款账户
- ✅ 统计账户数量、借款总额、存款总额等

### 排序功能
- ✅ 按借款余额排序（从大到小）
- ✅ 按存款余额排序（从大到小）
- ✅ 按开户日期排序（从小到大）

### 安全功能
- ✅ 登录验证（默认密码：admin123）
- ✅ 允许三次输入机会
- ✅ 借款超额预警（超过5万元）

### 数据校验
- ✅ 身份证号格式验证
- ✅ 日期格式验证

## 版本规划

### ✅ 版本一：C语言控制台版
- 路径：`c_console/`
- 编译运行：
  ```bash
  # Windows
  compile.bat
  main.exe

  # Linux/Mac
  bash compile.sh
  ./main
  ```

### ✅ 版本二：Streamlit网页版
- 路径：`streamlit_app/`
- 安装依赖：
  ```bash
  pip install -r requirements.txt
  ```
- 运行：
  ```bash
  streamlit run app.py
  # 或
  run.bat
  ```

### ⏳ 版本三：PyQt5桌面版
- 路径：`pyqt5_gui/`
- 安装依赖：
  ```bash
  pip install -r requirements.txt
  ```
- 运行：
  ```bash
  python main.py
  # 或
  run.bat
  ```
- 注意：PyQt5版本的主窗口可以参考 `Final_Grade_Management_System/pyqt5_gui/ui/main_window.py` 的结构进行开发，将成绩管理相关的功能替换为银行账户管理功能。

## 数据文件

所有数据文件存储在 `dataset/` 目录下：

- `AccountBasic.txt` - 账户基本信息（gb2312编码）
- `AccountBalance.txt` - 账户余额（utf-8编码）
- `password.txt` - 登录密码（utf-8编码，默认：admin123）

### 数据格式

**AccountBasic.txt**
```
账号|姓名|身份证号|开户日期
10001|张三|110101199001011234|2024-01-15
```

**AccountBalance.txt**
```
账号|余额
10001|-60000.00
```

**password.txt**
```
admin123
```

## 业务规则

### 余额表示
- **正数**：表示存款额
- **负数**：表示借款额
- **零**：无存款无借款

### 账号规则
- 自动生成，从 10001 开始递增
- 已删除账户账号置为 -1（逻辑删除）

### 删除规则
- 清户时账号置为 -1
- 不立即删除文件记录
- 需要手动执行"文件紧缩"功能

## 开发规范

### 编码规范
- 使用 4 空格缩进
- 每行最大长度 100 字符
- 使用单引号（Python）
- 语句末尾添加分号（C语言）
- 添加中文注释

### 文件编码
- 含中文的文件使用 **gb2312/gbk** 编码
- 其他文件使用 **utf-8** 编码

## 测试数据

系统已预置测试数据：

| 账号 | 姓名 | 身份证号 | 开户日期 | 余额 |
|------|------|----------|----------|------|
| 10001 | 张三 | 110101199001011234 | 2024-01-15 | -60000.00 |
| 10002 | 李四 | 110101199002025678 | 2024-02-20 | 50000.00 |
| 10003 | 王五 | 110101199003034590 | 2024-03-10 | -30000.00 |
| 10004 | 赵六 | 110101199004041234 | 2024-04-05 | 100000.00 |
| 10005 | 钱七 | 110101199005056789 | 2024-05-12 | -40000.00 |

## 开发状态

- [x] 需求文档
- [x] 测试数据
- [x] C语言控制台版
- [x] Streamlit网页版
- [x] 数据管理模块（PyQt5）
- [x] 登录对话框（PyQt5）
- [ ] PyQt5主窗口（可参考Final Grade系统结构开发）

## 目录结构

```
Bank_Account_Management_System/
├── requirements.md          # 需求文档
├── README.md               # 项目说明（本文件）
├── c_console/              # C语言控制台版
│   ├── main.c
│   ├── compile.bat
│   ├── compile.sh
│   └── README.md
├── pyqt5_gui/              # PyQt5桌面版
│   ├── main.py
│   ├── data_manager.py
│   ├── requirements.txt
│   ├── run.bat
│   ├── README.md
│   └── ui/
│       ├── __init__.py
│       ├── login_dialog.py
│       └── main_window.py  # 待完善
├── streamlit_app/          # Streamlit网页版
│   ├── app.py
│   ├── data_manager.py
│   ├── requirements.txt
│   ├── run.bat
│   └── README.md
└── dataset/                # 数据文件
    ├── AccountBasic.txt
    ├── AccountBalance.txt
    └── password.txt
```

## 完成时间

2025年冬季
