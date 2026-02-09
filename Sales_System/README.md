# 销售系统

**✅ 开发完成**

## 项目概述

销售系统用于管理商品销售业务，支持管理员、店长、销售员三种角色的不同权限管理。

## 功能特性

### 管理员功能
- ✅ 自身密码修改
- ✅ 用户信息管理：添加、修改、查询、删除
- ✅ 商品信息管理：添加、修改、查询、删除
- ✅ 销售报表显示：日报表、月报表、商品销售量报表、销售员业绩报表
- ✅ 退出登陆系统

### 店长功能
- ✅ 自身密码修改
- ✅ 商品信息管理：添加、修改、查询、删除
- ✅ 销售报表显示：日报表、月报表、商品销售量报表、销售员业绩报表
- ✅ 退出登陆系统

### 销售员功能
- ✅ 商品查询浏览、商品销售
- ✅ 自己销售报表显示：日报表、月报表
- ✅ 退出登陆系统

## 项目结构

```
Sales_System/
├── c_console/           # C语言控制台版 ✅
│   ├── main.c
│   ├── compile.bat
│   ├── compile.sh
│   └── README.md
├── pyqt5_gui/          # PyQt5桌面版 ✅
│   ├── data_manager.py
│   ├── requirements.txt
│   ├── run.bat
│   └── README.md
├── streamlit_app/       # Streamlit网页版 ✅
│   ├── app.py
│   ├── data_manager.py
│   ├── requirements.txt
│   ├── run.bat
│   └── README.md
├── dataset/
│   ├── password.txt    # 管理员密码
│   ├── users.txt       # 用户数据
│   ├── products.txt    # 商品数据
│   └── sales.txt      # 销售记录
└── requirements.md     # 需求文档
```

## 默认账户

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| manager | manager123 | 店长 |
| sales1 | sales123 | 销售员 |
| sales2 | sales456 | 销售员 |

管理员密码文件：`dataset/password.txt`（默认：admin123）

## 快速开始

### C语言控制台版

#### Windows
```bash
cd c_console
compile.bat
main.exe
```

#### Linux/Mac
```bash
cd c_console
chmod +x compile.sh
./compile.sh
./main
```

### Streamlit网页版

```bash
cd streamlit_app
pip install -r requirements.txt
run.bat
# 或手动运行: streamlit run app.py
```

### PyQt5桌面版

```bash
cd pyqt5_gui
pip install -r requirements.txt
run.bat
# 或手动运行: python main.py
```

## 数据文件说明

### users.txt
```
用户ID|用户名|密码|角色
```
角色：1-管理员，2-店长，3-销售员

### products.txt
```
商品编号|商品名称|单价|库存量
```

### sales.txt
```
销售ID|商品编号|商品名称|销售数量|单价|总金额|销售日期|销售员ID
```

## 开发状态

- [x] 需求分析
- [x] 数据结构设计
- [x] C语言控制台版开发
- [x] Streamlit网页版开发
- [x] PyQt5桌面版开发（基础框架）
- [ ] 完整PyQt5版GUI开发

## 功能清单

| 功能模块 | C控制台 | PyQt5 | Streamlit |
|---------|---------|-------|-----------|
| 登录验证 | ✅ | ⚠️ | ✅ |
| 密码修改 | ✅ | - | - |
| 用户管理 | ✅ | - | - |
| 商品管理 | ✅ | - | - |
| 商品浏览 | ✅ | - | ✅ |
| 商品销售 | ✅ | - | ✅ |
| 日报表 | ✅ | - | ✅ |
| 月报表 | ✅ | - | ✅ |
| 商品销售量报表 | ✅ | - | ✅ |
| 销售员业绩报表 | ✅ | - | ✅ |

## 注意事项

1. C语言控制台版本菜单选择超过9时使用字符（A、B、C...）
2. 数据文件使用UTF-8编码
3. 程序启动时会自动检查并加载 `dataset/` 目录下的数据文件
4. 销售员只能查看自己的销售记录
5. 商品销售时会自动更新库存

## 技术栈

- **C语言控制台版**：C语言、文件操作
- **PyQt5桌面版**：Python、PyQt5
- **Streamlit网页版**：Python、Streamlit

## 完成时间

2025年2月
