#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
批量创建项目目录结构和模板文件
"""

import os

# 项目列表
projects = [
    {
        'id': 'Attendance_Management_System',
        'name': '出勤管理系统',
        'overview': '出勤管理系统用于管理学生的出勤记录，支持学生基本信息管理、出勤记录录入、查询、统计等功能。',
        'features': ['学生信息管理', '出勤记录录入', '出勤情况查询', '出勤率统计', '迟到/早退/请假记录', '数据导出功能']
    },
    {
        'id': 'Final_Grade_Management_System',
        'name': '期末成绩管理系统',
        'overview': '期末成绩管理系统用于管理学生的期末考试成绩，支持成绩录入、查询、排序、统计等功能。',
        'features': ['学生成绩录入', '成绩查询', '成绩排序', '平均分计算', '及格率统计', '成绩分析']
    },
    {
        'id': 'Bank_Account_Management_System',
        'name': '银行账目管理系统',
        'overview': '银行账目管理系统用于管理个人或企业的银行账户，支持存取款记录、转账、查询等功能。',
        'features': ['账户管理', '存取款记录', '转账功能', '余额查询', '交易明细', '利息计算']
    },
    {
        'id': 'Sales_System',
        'name': '销售系统',
        'overview': '销售系统用于管理商品销售业务，支持商品管理、销售记录、库存管理等功能。',
        'features': ['商品管理', '销售记录', '库存管理', '客户管理', '销售统计', '报表生成']
    },
    {
        'id': 'Phonebook_Management_System',
        'name': '电话簿管理系统',
        'overview': '电话簿管理系统用于管理联系人信息，支持联系人添加、查询、修改、删除等功能。',
        'features': ['联系人添加', '联系人查询', '联系人修改', '联系人删除', '分组管理', '导入导出']
    },
    {
        'id': 'Classmate_Information_Management_System',
        'name': '班级同学信息管理系统',
        'overview': '班级同学信息管理系统用于管理班级同学的基本信息，支持信息录入、查询、统计等功能。',
        'features': ['同学信息录入', '信息查询', '信息统计', '分组管理', '生日提醒', '通讯录导出']
    },
    {
        'id': 'Employee_Information_Management_System',
        'name': '职工信息管理系统',
        'overview': '职工信息管理系统用于管理企业职工信息，支持职工档案管理、考勤管理、薪资管理等功能。',
        'features': ['职工档案管理', '考勤管理', '薪资管理', '部门管理', '职务管理', '离职管理']
    },
    {
        'id': 'Book_Information_Management_System',
        'name': '图书信息管理系统',
        'overview': '图书信息管理系统用于管理图书馆图书信息，支持图书入库、借阅、归还、查询等功能。',
        'features': ['图书入库', '图书借阅', '图书归还', '图书查询', '图书统计', '超期提醒']
    },
    {
        'id': 'Book_Borrowing_Management_System',
        'name': '图书借阅管理系统',
        'overview': '图书借阅管理系统用于管理图书借阅业务，支持借阅登记、归还管理、逾期处理等功能。',
        'features': ['借阅登记', '归还管理', '逾期处理', '读者管理', '借阅统计', '催还通知']
    },
    {
        'id': 'Laboratory_Equipment_Management_System',
        'name': '实验设备管理系统',
        'overview': '实验设备管理系统用于管理实验室设备，支持设备借用、归还、维修、报废等功能。',
        'features': ['设备借用', '设备归还', '设备维修', '设备报废', '设备统计', '使用记录']
    },
    {
        'id': 'Course_Management_System',
        'name': '课程管理系统',
        'overview': '课程管理系统用于管理学校课程信息，支持课程安排、选课管理、课程查询等功能。',
        'features': ['课程安排', '选课管理', '课程查询', '排课管理', '教室管理', '教师管理']
    },
    {
        'id': 'Flight_Management_System',
        'name': '航班管理系统',
        'overview': '航班管理系统用于管理航班信息，支持航班查询、订票、改签、退票等功能。',
        'features': ['航班查询', '订票管理', '改签处理', '退票处理', '航班统计', '座位管理']
    },
    {
        'id': 'Matrix_Operations',
        'name': '矩阵运算',
        'overview': '矩阵运算程序用于实现矩阵的各种数学运算，包括加减乘、转置、求逆等功能。',
        'features': ['矩阵加法', '矩阵减法', '矩阵乘法', '矩阵转置', '矩阵求逆', '行列式计算']
    },
    {
        'id': 'Polynomial_Operations',
        'name': '一元多项式运算',
        'overview': '一元多项式运算程序用于实现一元多项式的各种运算，包括加减乘、求值、求导等功能。',
        'features': ['多项式加法', '多项式减法', '多项式乘法', '多项式求值', '多项式求导', '积分运算']
    },
    {
        'id': 'Josephus_Problem',
        'name': 'Josephus环问题',
        'overview': 'Josephus问题是一个经典的数学问题，本程序用于模拟和解决约瑟夫环问题。',
        'features': ['模拟过程', '求解幸存者', '参数设置', '结果显示', '历史记录', '性能分析']
    },
    {
        'id': 'String_Processing',
        'name': '字符串处理',
        'overview': '字符串处理程序用于实现各种字符串操作，包括查找、替换、分割、格式化等功能。',
        'features': ['字符串查找', '字符串替换', '字符串分割', '字符串格式化', '正则表达式', '编码转换']
    },
    {
        'id': 'Tetris_Game',
        'name': '俄罗斯方块游戏',
        'overview': '俄罗斯方块是一款经典的益智游戏，本程序实现完整的游戏逻辑和界面。',
        'features': ['方块下落', '方块旋转', '消行计分', '等级系统', '暂停/继续', '最高分记录']
    },
    {
        'id': 'Minesweeper_Game',
        'name': '扫雷游戏',
        'overview': '扫雷是一款经典的逻辑推理游戏，本程序实现完整的游戏逻辑和界面。',
        'features': ['雷区生成', '雷点标记', '计时功能', '剩余雷数', '游戏难度选择', '排行榜']
    },
    {
        'id': 'Gomoku_Game',
        'name': '五子棋游戏',
        'overview': '五子棋是一款经典的策略游戏，本程序实现完整的双人对战功能。',
        'features': ['棋盘绘制', '落子判断', '胜负判定', '悔棋功能', '重新开始', '对局记录']
    }
]


def create_readme(project):
    """创建项目的README文件"""
    content = f"""# {project['name']}

**⏳ 待开发**

## 项目概述

{project['overview']}

## 功能需求

{chr(10).join([f"- {feature}" for feature in project['features']])}

## 版本规划

- C语言控制台版
- PyQt5桌面版
- Streamlit网页版

## 开发进度

- [ ] 版本一：C语言控制台版
- [ ] 版本二：PyQt5桌面版
- [ ] 版本三：Streamlit网页版

## 目录结构

```
{project['id']}/
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
│       ├── main_window.py
│       └── [功能页面]
├── streamlit_app/       # Streamlit网页版
│   ├── app.py
│   ├── data_manager.py
│   ├── requirements.txt
│   ├── README.md
│   └── run.bat
└── dataset/
    ├── [数据文件1]
    ├── [数据文件2]
    └── password.txt    # 密码文件
```

## 开发说明

参考 SMMS（项目一）的开发流程和文件结构，实现以下功能：

{chr(10).join([f"{i+1}. {feature}" for i, feature in enumerate(project['features'])])}

## 完成时间

待定
"""
    return content


def create_init(project):
    """创建项目的__init__.py文件"""
    content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
{project['name']} - 项目模板
"""

__version__ = '1.0.0'
__author__ = 'Project Team'
'''
    return content


def create_project_structure(project):
    """创建项目的目录结构"""
    base_path = f"./{project['id']}"
    
    # 创建主目录
    os.makedirs(base_path, exist_ok=True)
    
    # 创建子目录
    subdirs = [
        f"{base_path}/c_console",
        f"{base_path}/pyqt5_gui/ui",
        f"{base_path}/streamlit_app",
        f"{base_path}/dataset"
    ]
    
    for subdir in subdirs:
        os.makedirs(subdir, exist_ok=True)
    
    # 创建README.md
    with open(f"{base_path}/README.md", 'w', encoding='utf-8') as f:
        f.write(create_readme(project))
    
    # 创建__init__.py
    with open(f"{base_path}/__init__.py", 'w', encoding='utf-8') as f:
        f.write(create_init(project))
    
    # 创建C语言版本的基础文件
    c_readme = f"""# C语言控制台版

**⏳ 待开发**

## 功能说明

{chr(10).join([f"- {feature}" for feature in project['features']])}

## 编译说明

```bash
cd c_console
gcc main.c -o main
./main  # Linux/Mac
main.exe # Windows
```

## 文件说明

- `main.c` - 主程序源代码
- `compile.bat` - Windows编译脚本
- `compile.sh` - Linux编译脚本
- `README.md` - 版本说明文档
"""
    
    with open(f"{base_path}/c_console/README.md", 'w', encoding='utf-8') as f:
        f.write(c_readme)
    
    # 创建PyQt5版本的基础文件
    pyqt5_requirements = """PyQt5>=5.15.0
"""
    
    pyqt5_readme = f"""# PyQt5桌面版

**⏳ 待开发**

## 功能说明

{chr(10).join([f"- {feature}" for feature in project['features']])}

## 安装运行

```bash
cd pyqt5_gui
pip install -r requirements.txt
python main.py
```

## 文件说明

- `main.py` - 程序入口
- `data_manager.py` - 数据管理模块
- `requirements.txt` - 依赖文件
- `README.md` - 版本说明文档
- `run.bat` - Windows快捷启动脚本
- `ui/` - UI模块
"""
    
    with open(f"{base_path}/pyqt5_gui/requirements.txt", 'w', encoding='utf-8') as f:
        f.write(pyqt5_requirements)
    
    with open(f"{base_path}/pyqt5_gui/README.md", 'w', encoding='utf-8') as f:
        f.write(pyqt5_readme)
    
    with open(f"{base_path}/pyqt5_gui/ui/__init__.py", 'w', encoding='utf-8') as f:
        f.write('')
    
    # 创建Streamlit版本的基础文件
    streamlit_requirements = """streamlit>=1.28.0
pandas>=2.0.0
"""
    
    streamlit_readme = f"""# Streamlit网页版

**⏳ 待开发**

## 功能说明

{chr(10).join([f"- {feature}" for feature in project['features']])}

## 安装运行

```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

## 文件说明

- `app.py` - Streamlit主应用
- `data_manager.py` - 数据管理模块（使用pandas）
- `requirements.txt` - 依赖文件
- `README.md` - 版本说明文档
- `run.bat` - Windows快捷启动脚本
"""
    
    with open(f"{base_path}/streamlit_app/requirements.txt", 'w', encoding='utf-8') as f:
        f.write(streamlit_requirements)
    
    with open(f"{base_path}/streamlit_app/README.md", 'w', encoding='utf-8') as f:
        f.write(streamlit_readme)
    
    with open(f"{base_path}/streamlit_app/__init__.py", 'w', encoding='utf-8') as f:
        f.write('')
    
    print(f"[OK] 已创建项目：{project['name']}")


def main():
    """主函数"""
    print("=" * 60)
    print("开始批量创建项目目录结构和模板文件...")
    print("=" * 60)
    print()
    
    for project in projects:
        create_project_structure(project)
    
    print()
    print("=" * 60)
    print(f"成功创建 {len(projects)} 个项目的目录结构！")
    print("=" * 60)


if __name__ == '__main__':
    main()
