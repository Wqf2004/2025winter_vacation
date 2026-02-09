#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
学生信息管理系统 - Streamlit网页应用
Student Message Management System
"""

import streamlit as st
from data_manager import DataManager

# 设置页面配置
st.set_page_config(
    page_title='学生信息管理系统',
    page_icon='🎓',
    layout='wide',
    initial_sidebar_state='expanded'
)

# 自定义CSS样式
st.markdown('''
<style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #3498db;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    .stButton>button[kind="primary"] {
        background-color: #27ae60;
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #2ecc71;
    }
    div[data-testid="stMetricValue"] {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
    }
</style>
''', unsafe_allow_html=True)


# 初始化数据管理器
@st.cache_resource
def get_data_manager():
    """获取数据管理器实例"""
    return DataManager()


dm = get_data_manager()


def login_page():
    """登录页面"""
    st.title('🎓 学生信息管理系统')
    st.markdown('---')
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('### 系统登录')
        
        password = st.text_input('请输入密码', type='password', key='password')
        
        if st.button('登录', width='stretch'):
            correct_password = dm.read_password()
            
            if password == correct_password:
                st.session_state.logged_in = True
                st.success('登录成功！正在进入系统...')
                st.rerun()
            else:
                st.error('密码错误，请重试！')
                st.info(f'提示：默认密码为 `admin123`')


def grade_entry_page():
    """成绩录入页面"""
    st.title('📝 学生成绩录入')
    st.markdown('---')
    
    # 读取学生数据
    students_df = dm.read_students()
    
    if students_df.empty:
        st.warning('⚠️ 没有学生信息，请先在 `dataset/a.txt` 中添加学生数据')
        return
    
    # 显示学生列表
    st.markdown('#### 当前系统中的学生信息')
    st.dataframe(students_df, width='stretch', hide_index=True)
    
    st.markdown('---')
    st.markdown('#### 录入成绩')
    
    # 录入表单
    col1, col2 = st.columns(2)
    
    with col1:
        student_id = st.selectbox('选择学号', options=students_df['学号'].tolist(), key='student_id')
        
        course_id = st.text_input('课程编号', placeholder='请输入课程编号', key='course_id')
        
        course_name = st.text_input('课程名称', placeholder='请输入课程名称', key='course_name')
    
    with col2:
        credits = st.number_input('学分', min_value=0.1, max_value=10.0, step=0.1, key='credits')
        
        usual_score = st.number_input('平时成绩', min_value=0.0, max_value=100.0, step=0.1, key='usual_score')
        
        lab_score = st.number_input('实验成绩（无实验请输入-1）', min_value=-1.0, max_value=100.0, 
                                    value=-1.0, step=0.1, key='lab_score')
        
        exam_score = st.number_input('卷面成绩', min_value=0.0, max_value=100.0, step=0.1, key='exam_score')
    
    if st.button('提交成绩', type='primary', width='stretch', key='submit_grade'):
        # 验证输入
        if not course_id:
            st.error('请输入课程编号！')
            return
        
        if not course_name:
            st.error('请输入课程名称！')
            return
        
        if credits <= 0:
            st.error('学分必须大于0！')
            return
        
        if not (0 <= usual_score <= 100):
            st.error('平时成绩必须在0-100之间！')
            return
        
        if lab_score != -1 and not (0 <= lab_score <= 100):
            st.error('实验成绩必须是-1或0-100之间！')
            return
        
        if not (0 <= exam_score <= 100):
            st.error('卷面成绩必须在0-100之间！')
            return
        
        # 添加成绩
        grade_data = {
            '学号': student_id,
            '课程编号': course_id,
            '课程名称': course_name,
            '学分': credits,
            '平时成绩': usual_score,
            '实验成绩': lab_score,
            '卷面成绩': exam_score
        }
        
        success, message = dm.add_grade(grade_data)
        
        if success:
            st.success(message)
            st.balloons()
            # 清空输入
            st.session_state['course_id'] = ''
            st.session_state['course_name'] = ''
        else:
            st.error(message)


def sort_page():
    """成绩排序页面"""
    st.title('📊 学生成绩排序')
    st.markdown('---')
    
    # 读取成绩数据
    grades_df = dm.read_grades()
    
    if grades_df.empty:
        st.warning('⚠️ 没有成绩记录可排序！')
        return
    
    # 排序选项
    sort_option = st.selectbox(
        '选择排序方式',
        ['按综合成绩升序排列', '按综合成绩降序排列',
         '按实得学分升序排列', '按实得学分降序排列'],
        key='sort_option'
    )
    
    if st.button('开始排序', width='stretch', key='sort_btn'):
        # 排序
        if sort_option == '按综合成绩升序排列':
            grades_df = grades_df.sort_values('综合成绩', ascending=True)
        elif sort_option == '按综合成绩降序排列':
            grades_df = grades_df.sort_values('综合成绩', ascending=False)
        elif sort_option == '按实得学分升序排列':
            grades_df = grades_df.sort_values('学分', ascending=True)
        elif sort_option == '按实得学分降序排列':
            grades_df = grades_df.sort_values('学分', ascending=False)
        
        # 添加学生姓名
        grades_df['姓名'] = grades_df['学号'].apply(dm.get_student_name)
        
        # 调整列顺序
        grades_df = grades_df[['学号', '姓名', '课程编号', '课程名称', '学分', '综合成绩']]
        
        # 显示结果
        st.markdown('#### 排序结果')
        st.dataframe(grades_df, width='stretch', hide_index=True)
        
        # 统计信息
        st.markdown(f'共 {len(grades_df)} 条记录')


def student_query_page():
    """学生查询页面"""
    st.title('👤 学生基本信息查询')
    st.markdown('---')
    
    # 查询选项
    query_type = st.radio('查询方式', ['按学号查询', '按姓名查询', '按宿舍号查询'], horizontal=True)
    
    # 输入框
    if query_type == '按学号查询':
        placeholder = '请输入学号'
    elif query_type == '按姓名查询':
        placeholder = '请输入姓名'
    else:
        placeholder = '请输入宿舍号'
    
    keyword = st.text_input('', placeholder=placeholder, key='student_query_keyword')
    
    # 查询按钮
    if st.button('查询', width='stretch', key='student_query_btn'):
        if not keyword:
            st.warning('请输入查询内容！')
            return
        
        # 读取学生数据
        students_df = dm.read_students()
        
        # 根据查询方式筛选
        if query_type == '按学号查询':
            result_df = students_df[students_df['学号'] == keyword]
        elif query_type == '按姓名查询':
            result_df = students_df[students_df['姓名'] == keyword]
        else:
            result_df = students_df[students_df['宿舍号码'] == keyword]
        
        # 显示结果
        st.markdown('#### 查询结果')
        
        if result_df.empty:
            st.warning('未找到匹配的学生信息！')
        else:
            # 验证手机号码格式
            result_df['手机号格式'] = result_df['电话号码'].apply(
                lambda x: '✅ 有效' if dm.validate_phone_number(str(x)) else '❌ 无效'
            )
            
            st.dataframe(result_df, width='stretch', hide_index=True)
            st.success(f'共 {len(result_df)} 条记录')


def score_query_page():
    """成绩查询页面"""
    st.title('📈 学生成绩信息查询')
    st.markdown('---')
    
    # 输入学号
    student_id = st.text_input('请输入学号', placeholder='请输入要查询的学号', key='score_query_id')
    
    # 查询按钮
    if st.button('查询', width='stretch', key='score_query_btn'):
        if not student_id:
            st.warning('请输入学号！')
            return
        
        # 检查学号是否存在
        if not dm.check_student_id(student_id):
            st.error(f'未找到学号为 {student_id} 的学生！')
            return
        
        # 读取成绩数据
        grades_df = dm.read_grades()
        
        # 筛选该学生的成绩
        result_df = grades_df[grades_df['学号'] == student_id]
        
        # 显示结果
        st.markdown('#### 查询结果')
        
        if result_df.empty:
            st.info(f'学号为 {student_id} 的学生暂无成绩记录！')
        else:
            # 显示学生姓名
            student_name = dm.get_student_name(student_id)
            st.markdown(f'**学号：** {student_id}  **姓名：** {student_name}')
            st.markdown('---')
            
            # 显示成绩表格
            display_df = result_df[['课程编号', '课程名称', '学分', '平时成绩', '综合成绩']]
            st.dataframe(display_df, width='stretch', hide_index=True)
            
            # 统计信息
            total_credits = result_df['学分'].sum()
            st.success(f'共修：{len(result_df)} 科，实得总学分为：{total_credits:.2f}')


def delete_page():
    """信息删除页面"""
    st.title('🗑️ 学生信息删除')
    st.markdown('---')
    
    # 警告信息
    st.warning('⚠️ **警告：删除操作不可恢复，请谨慎操作！**')
    
    # 输入学号
    student_id = st.text_input('请输入要删除的学生学号', 
                              placeholder='请输入学号', key='delete_id')
    
    # 查询按钮
    if st.button('查询学生信息', width='stretch', key='search_student'):
        if not student_id:
            st.warning('请输入学号！')
            return
        
        # 检查学号是否存在
        if not dm.check_student_id(student_id):
            st.error(f'未找到学号为 {student_id} 的学生！')
            return
        
        # 读取学生数据
        students_df = dm.read_students()
        
        # 查找学生
        student_info = students_df[students_df['学号'] == student_id]
        
        # 显示学生信息
        st.markdown('#### 学生信息')
        st.dataframe(student_info, width='stretch', hide_index=True)
        
        # 验证手机号码
        phone = student_info['电话号码'].iloc[0]
        phone_valid = dm.validate_phone_number(str(phone))
        st.info(f'手机号码格式：{"✅ 有效" if phone_valid else "❌ 无效"}')
        
        # 删除按钮
        st.markdown('---')
        if st.button('🗑️ 删除该学生及其所有成绩', type='primary', 
                   width='stretch', key='confirm_delete'):
            success, message = dm.delete_student(student_id)
            
            if success:
                st.success(message)
                st.balloons()
            else:
                st.error(message)


def main():
    """主函数"""
    # 初始化会话状态
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # 如果未登录，显示登录页面
    if not st.session_state.logged_in:
        login_page()
        return
    
    # 侧边栏
    with st.sidebar:
        st.title('🎓 SMMS')
        st.markdown('---')
        
        page = st.radio(
            '导航菜单',
            ['📝 成绩录入', '📊 成绩排序', '👤 学生查询', '📈 成绩查询', '🗑️ 信息删除'],
            label_visibility='collapsed'
        )
        
        st.markdown('---')
        
        if st.button('退出登录', width='stretch'):
            st.session_state.logged_in = False
            st.rerun()
        
        # 统计信息
        st.markdown('---')
        st.markdown('#### 📊 数据统计')
        
        students_df = dm.read_students()
        grades_df = dm.read_grades()
        
        st.metric('学生总数', len(students_df))
        st.metric('成绩记录', len(grades_df))
        
        if not grades_df.empty:
            avg_score = grades_df['综合成绩'].mean()
            st.metric('平均综合成绩', f'{avg_score:.1f}')
    
    # 根据选择显示不同页面
    if page == '📝 成绩录入':
        grade_entry_page()
    elif page == '📊 成绩排序':
        sort_page()
    elif page == '👤 学生查询':
        student_query_page()
    elif page == '📈 成绩查询':
        score_query_page()
    elif page == '🗑️ 信息删除':
        delete_page()


if __name__ == '__main__':
    main()
