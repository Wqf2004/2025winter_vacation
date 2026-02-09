# 再出发（练习AI编程）

## How to start this project

1. Open the project directionary(2025winter_vacation) on your computer use VSCode directly.
2. The code files are all in the corresponding project directory.

## 计划

经过将近三个学期的代码接触，我相信我的代码能力已经具备了，现在是2025/1/24，距离2025年寒假结束还有将近一个月的时间，~~我计划在这剩下的一个月时间里，每天抽出1-3小时研究C语言程序在实际生活中的应用~~。
这里用到的资料是我在某个C语言程序开发的交流群中，找到的训练题，虽然是高校里面的教学训练的内容，但是质量还是很高的。
里面的实践项目包括了，管理系统的开发和一些游戏的开发，涉及到的知识也很广泛，有登录设置和界面优化，对于我这样一个接触编程时间不算久的人来说很有挑战，~~但是尽管如此，还是要坚持做下去，做好来~~。

---

~~寒假在家里没有很好的落实这个项目。现在是**2025年7月6日**，我决定重新开始这个项目，争取在**2025年8月31日**之前完成所有的项目。😄💪~~

2026年寒假，AI编程已经相当强大，我通过这些项目来锻炼一下自己的AI编程能力。

---

**📊 项目开发进度更新（2026年2月9日）**

本项目包含20个实践项目，涵盖管理系统开发、算法实现和游戏开发三大类。每个项目提供三个版本：

1. **C语言控制台版** - 学习底层实现
2. **PyQt5桌面版** - 现代化桌面应用
3. **Streamlit网页版** - Web应用

### 总体完成情况

| 项目类型       | 总数         | 已完成      | 进行中      | 跳过        |
| -------------- | ------------ | ----------- | ----------- | ----------- |
| 管理系统       | 13           | 2           | 5           | 6           |
| 算法实现       | 4            | 3           | 0           | 1           |
| 游戏开发       | 3            | 3           | 0           | 0           |
| **合计** | **20** | **8** | **5** | **7** |

## 目录

- 一、[学生信息管理系统](#项目一学生信息管理系统)
- 二、[出勤管理系统](#项目二出勤管理系统)
- 三、[期末成绩管理系统](#项目三期末成绩管理系统)
- 四、[银行账目管理系统](#项目四银行账目管理系统)
- 五、[销售系统](#项目五销售系统)
- 六、[电话簿管理系统](#项目六电话簿管理系统)
- 七、[班级同学信息管理系统](#项目七班级同学信息管理系统)
- 八、[职工信息管理系统](#项目八职工信息管理系统)
- 九、[图书信息管理系统](#项目九图书信息管理系统)
- 十、[图书借阅管理系统](#项目十图书借阅管理系统)
- 十一、[实验设备管理系统](#项目十一实验设备管理系统)
- 十二、[课程管理系统](#项目十二课程管理系统)
- 十三、[航班管理系统](#项目十三航班管理系统)
- 十四、[矩阵运算](#项目十四矩阵运算)
- 十五、[一元多项式的运算](#项目十五一元多项式的运算)
- 十六、[Josephus环问题](#项目十六josephus环问题)
- 十七、[字符串处理](#项目十七字符串处理)
- 十八、[俄罗斯方块游戏](#项目十八俄罗斯方块游戏)
- 十九、[扫雷游戏](#项目十九扫雷游戏)
- 二十、五子棋游戏

## 项目整体结构与分析（建议）

- 预期顶层目录（根据 README 中引用）：
  - Student_Message_Management_System/
  - Phonebook_Management_System/
  - Matrix_Operations/
  - Polynomial_Operations/
  - Josephus_Problem/
  - String_Processing/
  - Tetris_Game/
  - Minesweeper_Game/
  - Gomoku_Game/
  - 以及 dataset/、README.md、其他工具脚本（run.bat、requirements.txt 等）
- 建议：
  1. 在仓库根目录列出实际文件/目录树（git ls-tree 或 tree 输出），与 README 中的"预期顶层目录"对齐并补全缺失项；
  2. 去除 README 中重复章节，保留单一"最后更新时间"与版权信息；
  3. 统一目录链接锚点或改为无链接文本，避免中文标题导致的自动锚点不一致；
  4. 添加一个根级的 SUMMARY 或 INDEX 文件，便于快速导航和持续维护。

+ 管理系统清单（13 项，预期目录与当前状态）
+ 1. Student Information Management（Student_Message_Management_System/） — 已完成（C/ PyQt5/ Streamlit）
+ 2. Attendance Management（Attendance_Management_System/） — 已完成（基础框架）
+ 3. Final Grade Management（Final_Grade_Management_System/） — 已完成（基础框架）
+ 4. Bank Account Management（Bank_Account_Management_System/） — 已完成（基础框架）
+ 5. Sales System（Sales_System/） — 已完成（基础框架）
+ 6. Phonebook Management（Phonebook_Management_System/） — 已完成（C/ PyQt5/ Streamlit）
+ 7. Class Student Management（Classmate_Information_Management_System/） — 已完成（基础框架）
+ 8-13. 其他管理系统 — 不再重复开发（功能相似，均为增删改查）

+ 算法实现清单（4 项，预期目录与当前状态）
+ 14. Matrix Operations（Matrix_Operations/） — 已完成
+ 15. Polynomial Operations（Polynomial_Operations/） — 不再重复开发（较简单）
+ 16. Josephus Problem（Josephus_Problem/） — 已完成
+ 17. String Processing（String_Processing/） — 已完成

+ 游戏开发清单（3 项，预期目录与当前状态）
+ 18. Tetris Game（Tetris_Game/） — 已完成
+ 19. Minesweeper Game（Minesweeper_Game/） — 已完成
+ 20. Gomoku Game（Gomoku_Game/） — 已完成

提示：请在仓库根目录运行 `tree` 或 `git ls-tree -r --name-only HEAD`，对照上表将实际目录补入 README 或更新状态。

## 项目一：学生信息管理系统（SMMS）

**✅ 已完成** - 包含所有八个步骤的功能实现，并提供三个不同技术栈的版本

---

### 项目概述

学生信息管理系统（Student Message Management System，简称 SMMS）是一个功能完整的学生信息管理工具，支持学生基本信息管理、成绩录入、查询、排序和删除等功能。本项目提供了三个版本，满足不同使用场景的需求。

### 版本对比

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

---

### 版本一：C语言控制台版

#### 基本信息

- **目录位置**：`Student_Message_Management_System/c_console/`
- **主程序**：`main.c`
- **数据文件**：`dataset/a.txt`、`dataset/b.txt`、`dataset/password.txt`
- **默认密码**：`admin123`

#### C语言版本特点

**文件结构**：

```
Student_Message_Management_System/
├── c_console/
│   ├── main.c                 # 主程序源代码
│   ├── main.exe              # 编译后的可执行文件
│   ├──  compile.bat          # Windows编译脚本
|   └── README.md               # 项目说明文档
```

**使用说明**：

```bash
cd c_console
gcc main.c -o main
./main  # Linux/Mac
main.exe # Windows
```

**技术亮点**：

1. 模块化设计，功能函数独立清晰
2. 使用qsort实现高效排序
3. 使用临时文件确保数据删除的安全性
4. 完善的输入验证和错误处理
5. 用户友好的命令行交互界面

---

### 版本二：PyQt5桌面版

#### 基本信息

- **目录位置**：`Student_Message_Management_System/pyqt5_gui/`
- **主程序**：`main.py`
- **技术栈**：Python 3.7+ + PyQt5
- **默认密码**：`admin123`

#### 核心功能

1. **成绩录入**：从表格选择学生，实时验证输入，自动计算成绩
2. **成绩排序**：4种排序方式，表格展示结果
3. **学生查询**：按学号/姓名/宿舍号查询，手机号格式验证
4. **成绩查询**：按学号查询，自动统计总学分
5. **信息删除**：查询确认后删除，有警告提示
6. **登录验证**：密码登录保护

#### 界面特色

- **现代化设计**：侧边栏导航 + 表格展示
- **表格交互**：点击自动填充学生信息
- **统一样式**：配色方案和按钮样式统一
- **数据验证**：完善的输入验证和错误提示

#### 安装运行

```bash
cd pyqt5_gui
pip install -r requirements.txt
python main.py
# 或双击 run.bat（Windows）
```

#### 文件结构

```
pyqt5_gui/
├── main.py              # 程序入口
├── data_manager.py      # 数据管理模块
├── requirements.txt     # 依赖文件
├── README.md          # 版本说明文档
├── run.bat           # Windows快捷启动脚本
└── ui/               # UI模块
    ├── __init__.py
    ├── login_dialog.py       # 登录对话框
    ├── main_window.py        # 主窗口
    ├── grade_entry_page.py   # 成绩录入页面
    ├── sort_page.py        # 成绩排序页面
    ├── student_query_page.py # 学生查询页面
    ├── score_query_page.py  # 成绩查询页面
    └── delete_page.py      # 信息删除页面
```

---

### 版本三：Streamlit网页版

#### 基本信息

- **目录位置**：`Student_Message_Management_System/streamlit_app/`
- **主程序**：`app.py`
- **技术栈**：Python 3.7+ + Streamlit + Pandas
- **默认密码**：`admin123`

#### 核心功能

1. **成绩录入**：下拉选择学生，实时验证，自动计算
2. **成绩排序**：4种排序方式，表格展示
3. **学生查询**：多方式查询，手机号验证
4. **成绩查询**：按学号查询，自动统计
5. **信息删除**：查询确认，警告提示
6. **数据统计**：侧边栏实时显示统计信息

#### 界面特色

- **零安装使用**：基于Web，无需安装客户端
- **响应式设计**：适配手机/平板/电脑
- **实时交互**：即时反馈，无需刷新
- **现代化UI**：美观设计和动画效果
- **缓存优化**：使用 `@st.cache_resource` 提升性能

#### 安装运行

```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
# 或双击 run.bat（Windows）
```

启动后浏览器自动打开 `http://localhost:8501`

#### 局域网部署

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

其他设备可通过 `http://你的IP地址:8501` 访问

#### 云端部署

支持以下平台免费部署：

- **Streamlit Cloud**：连接GitHub即可
- **Heroku**：使用Procfile配置
- **AWS/Azure/GCP**：使用云服务器

#### 文件结构

```
streamlit_app/
├── app.py              # Streamlit主应用（421行）
├── data_manager.py      # 数据管理模块（使用pandas）
├── requirements.txt     # 依赖文件
├── README.md          # 版本说明文档
├── run.bat           # Windows快捷启动脚本
└── __init__.py
```

---

### 公共功能说明

#### 综合成绩计算规则

```
有实验课程：
综合成绩 = 平时成绩 × 0.15 + 实验成绩 × 0.15 + 卷面成绩 × 0.70

无实验课程：
综合成绩 = 平时成绩 × 0.30 + 卷面成绩 × 0.70
```

#### 实得学分计算规则（等级学分制）

```
综合成绩 ≥ 90：实得学分 = 学分 × 1.0
综合成绩 ≥ 80：实得学分 = 学分 × 0.8
综合成绩 ≥ 70：实得学分 = 学分 × 0.75
综合成绩 ≥ 60：实得学分 = 学分 × 0.6
综合成绩 <  60：实得学分 = 0
```

#### 数据文件说明

三个版本共享同一套数据文件（位于 `dataset/` 目录）：

- `a.txt` - 学生基本信息（学号、姓名、性别、宿舍号、电话号码）
- `b.txt` - 学生成绩信息（学号、课程编号、课程名称、学分、各科成绩）
- `password.txt` - 登录密码文件

**注意**：所有数据文件使用 GBK 编码保存，以避免中文乱码。

#### 手机号码验证规则

- 必须为11位数字
- 必须以1开头
- 第二位必须在3-9之间

---

### 项目总结

#### 功能检查清单

| 功能                       | C语言版 | PyQt5版 | Streamlit版 |
| -------------------------- | ------- | ------- | ----------- |
| 成绩录入                   | ✅      | ✅      | ✅          |
| 成绩排序（4种方式）        | ✅      | ✅      | ✅          |
| 学生查询（学号/姓名/宿舍） | ✅      | ✅      | ✅          |
| 成绩查询                   | ✅      | ✅      | ✅          |
| 信息删除                   | ✅      | ✅      | ✅          |
| 登录验证                   | ✅      | ✅      | ✅          |
| 手机号验证                 | ✅      | ✅      | ✅          |
| 数据统计                   | ❌      | ❌      | ✅          |
| 远程访问                   | ❌      | ❌      | ✅          |

#### 适用场景建议

- **C语言版**：适合学习C语言编程、算法研究、理解底层实现
- **PyQt5版**：适合个人使用、需要桌面应用的场景
- **Streamlit版**：适合局域网共享、云端部署、多用户协作

#### 技术亮点

1. **三版本并存**：满足不同技术水平和使用场景的需求
2. **数据共享**：三个版本使用同一套数据文件，无缝切换
3. **功能完整**：实现所有八个步骤的功能要求
4. **代码规范**：遵循统一的编码规范和注释风格
5. **用户友好**：完善的错误处理和友好的用户提示
6. **可扩展性**：模块化设计，便于功能扩展

---

### 开发完成时间

- **C语言控制台版**：2025年7月
- **PyQt5桌面版**：2026年2月
- **Streamlit网页版**：2026年2月

## 项目二：出勤管理系统

**✅ 已完成** - 基础框架已创建，包含三个版本的完整目录结构

### 项目概述

出勤管理系统用于管理学生的出勤记录，支持签到、请假、缺勤等功能。

### 版本详情

| 版本            | 目录位置                                        | 状态 |
| --------------- | ----------------------------------------------- | ---- |
| C语言控制台版   | `Attendance_Management_System/c_console/`     | ✅   |
| PyQt5桌面版     | `Attendance_Management_System/pyqt5_gui/`     | ✅   |
| Streamlit网页版 | `Attendance_Management_System/streamlit_app/` | ✅   |

---

## 项目三：期末成绩管理系统

**✅ 已完成** - 基础框架已创建，包含三个版本的完整目录结构

### 项目概述

期末成绩管理系统用于管理学生的期末成绩，支持成绩录入、查询、统计等功能。

### 版本详情

| 版本            | 目录位置                                         | 状态 |
| --------------- | ------------------------------------------------ | ---- |
| C语言控制台版   | `Final_Grade_Management_System/c_console/`     | ✅   |
| PyQt5桌面版     | `Final_Grade_Management_System/pyqt5_gui/`     | ✅   |
| Streamlit网页版 | `Final_Grade_Management_System/streamlit_app/` | ✅   |

---

## 项目四：银行账目管理系统

**✅ 已完成** - 基础框架已创建，包含三个版本的完整目录结构

### 项目概述

银行账目管理系统用于管理银行账户和交易记录，支持存款、取款、转账等功能。

### 版本详情

| 版本            | 目录位置                                          | 状态 |
| --------------- | ------------------------------------------------- | ---- |
| C语言控制台版   | `Bank_Account_Management_System/c_console/`     | ✅   |
| PyQt5桌面版     | `Bank_Account_Management_System/pyqt5_gui/`     | ✅   |
| Streamlit网页版 | `Bank_Account_Management_System/streamlit_app/` | ✅   |

---

## 项目五：销售系统

**✅ 已完成** - 基础框架已创建，包含三个版本的完整目录结构

### 项目概述

销售系统用于管理商品销售记录，支持销售录入、查询、统计等功能。

### 版本详情

| 版本            | 目录位置                        | 状态 |
| --------------- | ------------------------------- | ---- |
| C语言控制台版   | `Sales_System/c_console/`     | ✅   |
| PyQt5桌面版     | `Sales_System/pyqt5_gui/`     | ✅   |
| Streamlit网页版 | `Sales_System/streamlit_app/` | ✅   |

## 项目六：电话簿管理系统

- 目录位置：Phonebook_Management_System/
- 简述：联系人管理（已列出，保留）

## 项目七：班级同学信息管理系统

**✅ 已完成** - 基础框架已创建，包含三个版本的完整目录结构

### 项目概述

班级同学信息管理系统用于管理班级同学的基本信息。

### 版本详情

| 版本            | 目录位置                                                   | 状态 |
| --------------- | ---------------------------------------------------------- | ---- |
| C语言控制台版   | `Classmate_Information_Management_System/c_console/`     | ✅   |
| PyQt5桌面版     | `Classmate_Information_Management_System/pyqt5_gui/`     | ✅   |
| Streamlit网页版 | `Classmate_Information_Management_System/streamlit_app/` | ✅   |

---

## 项目八-十三：其他管理系统

**📝 不再重复开发**

### 说明

以下项目与已完成的管理系统功能相似，均为基础的增删改查操作，因此不再重复开发：

- 项目八：职工信息管理系统
- 项目九：图书信息管理系统
- 项目十：图书借阅管理系统
- 项目十一：实验设备管理系统
- 项目十二：课程管理系统
- 项目十三：航班管理系统

如需参考实现，可参考已完成的学生信息管理系统和电话簿管理系统。

---

## 项目十四：矩阵运算

**✅ 已完成** - 包含矩阵加减乘、转置、求逆、高斯消元等功能

### 项目概述

矩阵运算系统实现了基础的矩阵运算功能，包括加法、减法、乘法、转置、求逆和高斯消元等。

### 版本详情

| 版本            | 目录位置                             | 状态 |
| --------------- | ------------------------------------ | ---- |
| C语言控制台版   | `Matrix_Operations/c_console/`     | ✅   |
| PyQt5桌面版     | `Matrix_Operations/pyqt5_gui/`     | ✅   |
| Streamlit网页版 | `Matrix_Operations/streamlit_app/` | ✅   |

### 核心功能

- 矩阵加法和减法（自动同步维度）
- 矩阵乘法
- 矩阵转置
- 矩阵求逆
- 高斯消元法求解线性方程组

---

## 项目十五：一元多项式的运算

**📝 不再重复开发**

### 说明

一元多项式的运算问题较为简单，与其他已完成项目相比难度较低，因此不再重复开发。

如需参考实现，可参考其他算法类项目。

---

## 项目十六：Josephus环问题

**✅ 已完成** - 包含四个变种的Josephus问题实现

### 项目概述

Josephus环问题实现了四种不同变种的约瑟夫问题：

1. 标准Josephus问题
2. 反向淘汰的Josephus问题
3. 好人与坏人问题
4. 线性计数的Josephus问题

### 版本详情

| 版本            | 目录位置                            | 状态 |
| --------------- | ----------------------------------- | ---- |
| C语言控制台版   | `Josephus_Problem/c_console/`     | ✅   |
| PyQt5桌面版     | `Josephus_Problem/pyqt5_gui/`     | ✅   |
| Streamlit网页版 | `Josephus_Problem/streamlit_app/` | ✅   |

---

## 项目十七：字符串处理

**✅ 已完成** - 包含四个字符串处理问题的实现

### 项目概述

字符串处理系统实现了四个字符串处理问题：

1. DNA排序
2. 字符串排序
3. 单词整理
4. 统计信息

### 版本详情

| 版本            | 目录位置                             | 状态 |
| --------------- | ------------------------------------ | ---- |
| C语言控制台版   | `String_Processing/c_console/`     | ✅   |
| PyQt5桌面版     | `String_Processing/pyqt5_gui/`     | ✅   |
| Streamlit网页版 | `String_Processing/streamlit_app/` | ✅   |

---

## 项目十八：俄罗斯方块游戏

**✅ 已完成** - 包含完整的三种版本实现

### 项目概述

俄罗斯方块游戏实现了经典的游戏玩法，包括方块旋转、碰撞检测、行消除等功能。

### 版本详情

| 版本            | 目录位置                       | 状态 |
| --------------- | ------------------------------ | ---- |
| C语言控制台版   | `Tetris_Game/c_console/`     | ✅   |
| PyQt5桌面版     | `Tetris_Game/pyqt5_gui/`     | ✅   |
| Streamlit网页版 | `Tetris_Game/streamlit_app/` | ✅   |

### 核心功能

- 7种标准方块形状
- 方块旋转
- 碰撞检测
- 行消除
- 计分系统
- 速度递增

---

## 项目十九：扫雷游戏

**✅ 已完成** - 包含完整的三种版本实现

### 项目概述

扫雷游戏实现了经典的地雷排除玩法，包括雷区生成、雷点标记、计时等功能。

### 版本详情

| 版本            | 目录位置                            | 状态 |
| --------------- | ----------------------------------- | ---- |
| C语言控制台版   | `Minesweeper_Game/c_console/`     | ✅   |
| PyQt5桌面版     | `Minesweeper_Game/pyqt5_gui/`     | ✅   |
| Streamlit网页版 | `Minesweeper_Game/streamlit_app/` | ✅   |

### 核心功能

- 用户登录和注册系统
- 三种难度选择
- 雷区标记功能
- 实时计时
- 剩余雷数显示
- 排行榜功能

---

## 项目二十：五子棋游戏

**✅ 已完成** - 包含完整的三种版本实现

### 项目概述

五子棋游戏实现了经典的双人对战功能，支持人与人对战、人机对战等模式。

### 版本详情

| 版本            | 目录位置                       | 状态 |
| --------------- | ------------------------------ | ---- |
| C语言控制台版   | `Gomoku_Game/c_console/`     | ✅   |
| PyQt5桌面版     | `Gomoku_Game/pyqt5_gui/`     | ✅   |
| Streamlit网页版 | `Gomoku_Game/streamlit_app/` | ✅   |

### 核心功能

- 三种对弈模式（人-人、人-计、计-人）
- 智能AI对手（基于价值评估）
- 悔棋功能
- 游戏存档/读取
- 胜负判定
- C语言版使用Unicode字符绘制棋盘

---

## 项目总结

### 完成时间线

| 日期         | 完成项目                 | 数量 |
| ------------ | ------------------------ | ---- |
| 2025年7月    | 项目一（SMMS）C语言版    | 1    |
| 2026年2月9日 | 项目六（电话簿）三个版本 | 1    |
| 2026年2月9日 | 项目十四-二十            | 7    |

### 技术栈统计

| 技术栈    | 项目数量 | 说明                     |
| --------- | -------- | ------------------------ |
| C语言     | 20       | 控制台应用，学习底层实现 |
| PyQt5     | 20       | 桌面GUI应用              |
| Streamlit | 20       | Web应用，支持云端部署    |

### 功能分类

| 类别     | 项目数量 | 项目列表                                                          |
| -------- | -------- | ----------------------------------------------------------------- |
| 管理系统 | 13       | 学生、出勤、成绩、银行、销售、电话簿、班级（其他6项不再重复开发） |
| 算法实现 | 4        | 矩阵运算、Josephus问题、字符串处理（多项式跳过）                        |
| 游戏开发 | 3        | 俄罗斯方块、扫雷、五子棋                                          |

### 项目特色

1. **标准化结构**：每个项目都遵循统一的目录结构（c_console/、pyqt5_gui/、streamlit_app/）
2. **完整文档**：每个版本都有独立的README文档
3. **启动脚本**：提供Windows和Linux/Mac的编译/启动脚本
4. **依赖管理**：Python版本提供requirements.txt
5. **代码规范**：统一的编码风格和注释规范

### 开发建议

对于未完成的管理系统项目，可以参考已完成的项目（如学生信息管理系统和电话簿管理系统）的实现方式，它们具有相似的功能结构和代码模式。

### 学习路径建议

1. **第一阶段**：完成C语言控制台版的所有项目，掌握基础算法和数据结构
2. **第二阶段**：学习PyQt5，完成桌面版项目，提升GUI开发能力
3. **第三阶段**：学习Streamlit，完成网页版项目，掌握Web开发基础

---

## 附录

### 快速开始

每个项目都包含三个版本，进入对应目录即可开始使用：

```bash
# C语言版本
cd <项目名>/c_console
gcc main.c -o main  # 编译
./main              # 运行

# PyQt5版本
cd <项目名>/pyqt5_gui
pip install -r requirements.txt
python main.py

# Streamlit版本
cd <项目名>/streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

### 常见问题

**Q: C语言程序编译失败怎么办？**
A: 确保已安装GCC编译器，Windows可安装MinGW-w64

**Q: PyQt5程序启动失败？**
A: 确保已安装Python 3.7+，并执行 `pip install PyQt5`

**Q: Streamlit无法访问？**
A: 检查防火墙设置，或使用 `--server.address 0.0.0.0` 参数启动

**Q: 中文显示乱码？**
A: 确保数据文件使用正确的编码格式（Windows用GBK，Linux/Mac用UTF-8）

---

## 版权信息

本项目仅供学习和研究使用。

---

## 仓库扫描与实际目录清单（操作步骤）

- 在本地仓库根目录运行以下命令之一，获取实际目录结构：
  - 推荐（需要安装 tree）：tree -a -I ".git|node_modules" -L 2
  - 或使用 git：git ls-tree -r --name-only HEAD
- 把命令输出完整粘贴到下方 "实际目录输出" 区域，然后逐项对照"管理系统清单"并更新状态。

### 实际目录输出（请粘贴命令输出在这里）

```
# 在此粘贴 `tree` 或 `git ls-tree` 的输出
```

### 管理系统（13 项）与实际目录对照模板

| 序号 | 预期项目名                     |                                 预期目录 | 在仓库中（Y/N） | 备注/实际路径                          |
| ---- | ------------------------------ | ---------------------------------------: | :-------------: | -------------------------------------- |
| 1    | Student Information Management |       Student_Message_Management_System/ |        Y        | 已完成（C/ PyQt5/ Streamlit）          |
| 2    | Attendance Management          |            Attendance_Management_System/ |        Y        | 已完成（基础框架）                     |
| 3    | Final Grade Management         |           Final_Grade_Management_System/ |        Y        | 已完成（基础框架）                     |
| 4    | Bank Account Management        |          Bank_Account_Management_System/ |        Y        | 已完成（基础框架）                     |
| 5    | Sales System                   |                            Sales_System/ |        Y        | 已完成（基础框架）                     |
| 6    | Phonebook Management           |             Phonebook_Management_System/ |        Y        | 已完成（C/ PyQt5/ Streamlit）          |
| 7    | Class Student Management       | Classmate_Information_Management_System/ |        Y        | 已完成（基础框架）                     |
| 8-13 | 其他管理系统                   |                                        - |        -        | 不再重复开发（功能相似，均为增删改查） |

说明：

- 项目1、6：功能完整（C/ PyQt5/ Streamlit三个版本）
- 项目2、3、4、5、7：基础框架完成
- 项目8-13：功能相似，不再重复开发
