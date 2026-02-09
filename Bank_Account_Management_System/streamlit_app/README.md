# Streamlit 网页版 - 银行账目管理系统

## 安装依赖

```bash
pip install streamlit
```

或

```bash
pip install -r requirements.txt
```

## 运行

```bash
streamlit run app.py
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
- 登录成功后显示主界面

### 预警功能
- 程序启动时自动检查借款额超过5万元的账户

## 数据文件

- `../dataset/password.txt` - 密码文件
- `../dataset/AccountBasic.txt` - 账户基本信息
- `../dataset/AccountBalance.txt` - 账户余额
