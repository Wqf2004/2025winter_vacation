# PyQt5 桌面版 - 银行账目管理系统

## 安装依赖

```bash
pip install PyQt5
```

或

```bash
pip install -r requirements.txt
```

## 运行

```bash
python main.py
```

或

```bash
run.bat
```

## 功能说明

### 侧边栏导航
- 开户
- 借款
- 还款
- 存款
- 查询账户
- 最大借款账户
- 最大存款账户
- 按借款余额排序
- 按存款余额排序
- 按开户日期排序
- 清户
- 文件紧缩
- 统计信息

### 登录验证
- 默认密码：admin123
- 允许三次输入机会
- 登录成功后显示主界面

### 预警功能
- 程序启动时自动检查借款额超过5万元的账户

## 开发说明

### 已完成模块
- ✅ data_manager.py - 数据管理模块
- ✅ ui/login_dialog.py - 登录对话框
- ✅ main.py - 程序入口
- ⏳ ui/main_window.py - 主窗口（参考 Final Grade 系统开发）

### 主窗口开发参考

主窗口文件 `ui/main_window.py` 可以参考 `Final_Grade_Management_System/pyqt5_gui/ui/main_window.py` 的结构进行开发，主要修改：

1. 将标题从"期末成绩管理系统"改为"银行账目管理系统"
2. 将侧边栏按钮替换为银行系统功能
3. 将各个功能页面的表单和表格替换为银行相关内容
4. 修改数据加载和保存逻辑

## 数据文件

- `../dataset/password.txt` - 密码文件
- `../dataset/AccountBasic.txt` - 账户基本信息
- `../dataset/AccountBalance.txt` - 账户余额
