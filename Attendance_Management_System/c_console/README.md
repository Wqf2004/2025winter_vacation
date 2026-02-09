# 出勤管理系统 - C控制台版

## 功能特性

- 职工打卡记录处理
- 出勤情况查询（按编号、全勤、请假、旷工）
- 请假管理功能
- 统计分析功能
- 排序功能
- 登录验证

## 编译运行

### Windows
```bash
# 编译
compile.bat

# 运行
main.exe
```

### Linux
```bash
# 编译
gcc -o main main.c

# 运行
./main
```

## 文件说明

- `main.c` - 主程序源代码
- `compile.bat` - Windows编译脚本
- `dataset/` - 数据文件目录

## 数据文件

- `EmpBasic.txt` - 职工基本信息
- `Attendance.txt` - 月出勤情况
- `punchIn.txt` - 当日出勤记录
- `MonthPunchIn.txt` - 月逐日出勤情况
- `password.txt` - 密码文件（默认：admin123）

## 使用说明

1. 运行程序后输入密码登录（默认：admin123）
2. 选择功能菜单进行操作
3. 所有操作完成后自动保存数据

## 主要算法

- 迟到次数计算：每迟到10分钟记1次
- 旷工判断：未打卡或迟到超过1小时
- 请假优惠：女职工3天、55岁以上男职工2天、生日月份1天
