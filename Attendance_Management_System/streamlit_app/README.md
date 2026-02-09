# 出勤管理系统 - Streamlit网页版

## 功能特性

- Web界面，支持浏览器访问
- 职工打卡记录处理
- 出勤情况查询（按编号、全勤、请假、旷工）
- 请假管理功能
- 统计分析功能
- 排序功能
- 登录验证
- 数据可视化展示

## 环境要求

- Python 3.7+
- Streamlit
- Pandas

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行方法

### Windows
```bash
# 双击运行
run.bat

# 或命令行运行
streamlit run app.py
```

### Linux/macOS
```bash
streamlit run app.py
```

访问地址：http://localhost:8501

## 文件说明

- `app.py` - 主程序
- `data_manager.py` - 数据管理模块
- `requirements.txt` - Python依赖列表
- `run.bat` - Windows启动脚本

## 默认密码

admin123

## 使用说明

1. 运行程序后在浏览器访问 http://localhost:8501
2. 输入密码登录
3. 使用左侧菜单选择功能
4. 在各个页面进行相应操作

## 技术栈

- Streamlit - Web框架
- Pandas - 数据处理
- Python 3.7+ - 开发语言

## 功能模块

- **打卡记录处理**：读取当日打卡记录，自动计算迟到和旷工
- **查询功能**：
  - 按职工编号查询
  - 全勤职工清单
  - 请假天数超过5天的职工
  - 有旷工行为的职工
- **请假管理**：录入请假信息，更新出勤记录
- **统计功能**：计算各项统计指标
- **排序功能**：
  - 最早到厂的职工
  - 按出生日期升序输出全体职工
  - 按出生日期降序列出全体女职工
