# 电话簿管理系统 - Streamlit网页版

## 功能说明

1. **联系人列表** - 表格展示所有联系人，支持排序和搜索
2. **添加联系人** - 输入联系人信息，自动验证格式
3. **查询联系人** - 按姓名或电话号码查询
4. **修改联系人** - 选择联系人进行编辑
5. **删除联系人** - 选择联系人删除
6. **保存数据** - 将数据保存到文件
7. **修改密码** - 修改系统登录密码
8. **数据验证** - 自动验证电话号码和E-mail格式

## 数据验证规则

### 电话号码验证
- 长度：7-15位
- 允许字符：数字、连字符(-)、空格
- 自动检查重复号码

### E-mail验证
- 必须包含 @ 符号
- @ 符号后必须包含点号
- 基本格式验证

## 安装运行

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行程序
```bash
streamlit run app.py
```

或双击 `run.bat`（Windows）

启动后浏览器自动打开 `http://localhost:8501`

## 局域网部署

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

其他设备可通过 `http://你的IP地址:8501` 访问

## 云端部署

支持以下平台免费部署：

- **Streamlit Cloud**：连接GitHub即可
- **Heroku**：使用Procfile配置
- **AWS/Azure/GCP**：使用云服务器

## 默认密码

- 默认密码：`admin123`

## 文件说明

- `app.py` - Streamlit主应用
- `data_manager.py` - 数据管理模块
- `requirements.txt` - 依赖文件
- `README.md` - 版本说明文档
- `run.bat` - Windows快捷启动脚本

## 界面特色

- 零安装使用，基于Web
- 响应式设计，适配各种设备
- 实时搜索和排序
- 现代化UI设计
- 侧边栏功能导航
- 实时统计信息显示
