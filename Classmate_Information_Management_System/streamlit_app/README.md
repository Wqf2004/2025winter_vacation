# 班级同学信息管理系统 - Streamlit网页版

## 功能说明

1. **同学列表** - 表格展示所有同学信息，支持搜索
2. **添加同学** - 输入同学信息
3. **查询同学** - 按姓名、学号、宿舍、QQ或电话查询
4. **修改同学** - 选择同学进行编辑
5. **删除同学** - 选择同学删除
6. **保存数据** - 将数据保存到文件
7. **修改密码** - 修改系统登录密码

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
- 实时搜索功能
- 现代化UI设计
- 侧边栏功能导航
- 实时统计信息显示
- 缓存优化（@st.cache_resource）
