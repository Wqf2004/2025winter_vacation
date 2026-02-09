"""
期末成绩管理系统 - Streamlit网页版
"""
import os
import streamlit as st
import pandas as pd

from data_manager import DataManager

# 获取项目根目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_manager = DataManager(base_dir)

# 页面配置
st.set_page_config(
    page_title='期末成绩管理系统',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)

# 登录状态
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 登录页面
if not st.session_state.logged_in:
    st.title('📊 期末成绩管理系统')
    st.subheader('系统登录')

    password = st.text_input('请输入密码', type='password')

    if st.button('登录'):
        if data_manager.verify_password(password):
            st.session_state.logged_in = True
            st.success('登录成功！')
            st.rerun()
        else:
            st.error('密码错误！')

    st.stop()

# 主界面
st.title('📊 期末成绩管理系统')

# 侧边栏导航
page = st.sidebar.radio(
    '功能导航',
    ['录入成绩', '查询基本情况', '查询成绩', '成绩一览表', '受奖情况',
     '成绩排序', '统计功能']
)

# 加载数据
@st.cache_data
def load_data():
    basic_df = data_manager.read_student_basics_df()
    grade_df = data_manager.read_student_grades_df()
    return basic_df, grade_df

basic_df, grade_df = load_data()

# 录入成绩页面
if page == '录入成绩':
    st.header('录入学生成绩')

    col1, col2 = st.columns(2)
    with col1:
        student_id = st.text_input('学号')
        computer_score = st.number_input('计算机成绩', min_value=0.0, max_value=100.0, value=0.0, step=0.5)
        math_score = st.number_input('高等数学成绩', min_value=0.0, max_value=100.0, value=0.0, step=0.5)

    with col2:
        english_score = st.number_input('外语成绩', min_value=0.0, max_value=100.0, value=0.0, step=0.5)
        pe_score = st.number_input('体育成绩', min_value=0.0, max_value=100.0, value=0.0, step=0.5)

    if st.button('提交'):
        if not student_id:
            st.warning('请输入学号！')
        elif student_id not in basic_df['学号'].values:
            st.warning('该学生不存在！')
        else:
            average_score = (computer_score + math_score + english_score + pe_score) / 4

            if student_id in grade_df['学号'].values:
                grade_df.loc[grade_df['学号'] == student_id, ['计算机', '高等数学', '外语', '体育', '平均分']] = [
                    computer_score, math_score, english_score, pe_score, average_score
                ]
                st.success('成绩已更新！')
            else:
                new_row = pd.DataFrame({
                    '学号': [student_id],
                    '计算机': [computer_score],
                    '高等数学': [math_score],
                    '外语': [english_score],
                    '体育': [pe_score],
                    '平均分': [average_score]
                })
                grade_df = pd.concat([grade_df, new_row], ignore_index=True)
                st.success('成绩已录入！')

            data_manager.save_student_grade_df(grade_df)

# 查询基本情况页面
elif page == '查询基本情况':
    st.header('查询学生基本情况')

    student_id = st.text_input('请输入学号')

    if st.button('查询'):
        result = basic_df[basic_df['学号'] == student_id]
        if not result.empty:
            st.dataframe(result, width='stretch')
        else:
            st.warning('未找到该学生！')

    st.write('所有学生基本情况：')
    st.dataframe(basic_df, width='stretch')

# 查询成绩页面
elif page == '查询成绩':
    st.header('查询学生成绩')

    student_id = st.text_input('请输入学号')

    if st.button('查询'):
        result = grade_df[grade_df['学号'] == student_id]
        if not result.empty:
            merged = pd.merge(result, basic_df[['学号', '姓名']], on='学号', how='left')
            st.dataframe(merged, width='stretch')
        else:
            st.warning('未找到该学生！')

# 成绩一览表页面
elif page == '成绩一览表':
    st.header('期末成绩一览表')

    merged_df = pd.merge(grade_df, basic_df[['学号', '姓名']], on='学号', how='left')
    st.dataframe(merged_df, width='stretch')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('学生总数', len(grade_df))
    with col2:
        st.metric('计算机平均分', f'{grade_df["计算机"].mean():.2f}')
    with col3:
        st.metric('高等数学平均分', f'{grade_df["高等数学"].mean():.2f}')
    with col4:
        st.metric('平均成绩最高', f'{grade_df["平均分"].max():.2f}')

# 受奖情况页面
elif page == '受奖情况':
    st.header('受奖情况')

    merged_df = pd.merge(grade_df, basic_df[['学号', '姓名']], on='学号', how='left')
    merged_df['奖励金额'] = merged_df['平均分'].apply(data_manager.calculate_award)

    award_df = merged_df[merged_df['奖励金额'] > 0]
    st.dataframe(award_df, width='stretch')

    if not award_df.empty:
        st.success(f'共有 {len(award_df)} 名学生获得奖励')
    else:
        st.info('暂无受奖学生')

# 成绩排序页面
elif page == '成绩排序':
    st.header('按平均成绩从高到低排序')

    merged_df = pd.merge(grade_df, basic_df[['学号', '姓名']], on='学号', how='left')
    sorted_df = merged_df.sort_values('平均分', ascending=False)

    st.dataframe(sorted_df, width='stretch')

# 统计功能页面
elif page == '统计功能':
    st.header('统计功能')

    stat_type = st.selectbox(
        '选择统计类型',
        ['各科平均分', '各科最高最低分', '各科各级别人数', '留级退学统计', '补考留级判断']
    )

    if stat_type == '各科平均分':
        st.subheader('各科平均分')

        avg_data = {
            '科目': ['计算机', '高等数学', '外语', '体育'],
            '平均分': [
                grade_df['计算机'].mean(),
                grade_df['高等数学'].mean(),
                grade_df['外语'].mean(),
                grade_df['体育'].mean()
            ]
        }
        st.dataframe(pd.DataFrame(avg_data), width='stretch')

    elif stat_type == '各科最高最低分':
        st.subheader('各科最高分和最低分')

        max_min_data = {
            '科目': ['计算机', '高等数学', '外语', '体育'],
            '最高分': [
                grade_df['计算机'].max(),
                grade_df['高等数学'].max(),
                grade_df['外语'].max(),
                grade_df['体育'].max()
            ],
            '最低分': [
                grade_df['计算机'].min(),
                grade_df['高等数学'].min(),
                grade_df['外语'].min(),
                grade_df['体育'].min()
            ]
        }
        st.dataframe(pd.DataFrame(max_min_data), width='stretch')

    elif stat_type == '各科各级别人数':
        st.subheader('各科各级别人数')

        subjects = ['计算机', '高等数学', '外语', '体育']
        levels = ['优(90+)', '良(80-89)', '中(70-79)', '及格(60-69)', '不及格(<60)']

        level_data = {'等级': levels}
        for subject in subjects:
            counts = [0] * 5
            for score in grade_df[subject]:
                if score >= 90:
                    counts[0] += 1
                elif score >= 80:
                    counts[1] += 1
                elif score >= 70:
                    counts[2] += 1
                elif score >= 60:
                    counts[3] += 1
                else:
                    counts[4] += 1
            level_data[subject] = counts

        st.dataframe(pd.DataFrame(level_data), width='stretch')

    elif stat_type == '留级退学统计':
        st.subheader('留级退学统计')

        retain_count = sum(1 for _, row in basic_df.iterrows() if row['留级次数'] > 0)
        makeup_count = sum(1 for _, row in basic_df.iterrows() if row['补考次数'] > 0)
        drop_count = sum(1 for _, row in basic_df.iterrows()
                        if row['留级次数'] >= 2 or row['补考次数'] >= 8)

        stat_data = pd.DataFrame({
            '项目': ['留级人数', '补考人数', '退学人数'],
            '人数': [retain_count, makeup_count, drop_count]
        })
        st.dataframe(stat_data, width='stretch')

    elif stat_type == '补考留级判断':
        st.subheader('补考与留级判断')

        result_data = []
        for _, grade_row in grade_df.iterrows():
            basic_row = basic_df[basic_df['学号'] == grade_row['学号']]
            if not basic_row.empty:
                basic_info = basic_row.iloc[0]

                fail_computer = grade_row['计算机'] < 60
                fail_math = grade_row['高等数学'] < 60
                fail_english = grade_row['外语'] < 60
                fail_pe = grade_row['体育'] < 60

                fail_subjects = []
                if fail_computer:
                    fail_subjects.append('计算机')
                if fail_math:
                    fail_subjects.append('高等数学')
                if fail_english:
                    fail_subjects.append('外语')
                if fail_pe:
                    fail_subjects.append('体育')

                if fail_subjects:
                    status = f'需补考：{", ".join(fail_subjects)}'
                    if fail_computer and fail_math and fail_english:
                        status += '，需留级'
                else:
                    status = '全科及格'

                if basic_info['留级次数'] >= 2:
                    status += '，需退学（留级）'
                elif basic_info['补考次数'] >= 8:
                    status += '，需退学（补考）'

                result_data.append({
                    '学号': grade_row['学号'],
                    '姓名': basic_info['姓名'],
                    '状态': status
                })

        st.dataframe(pd.DataFrame(result_data), width='stretch')

# 侧边栏底部
st.sidebar.markdown('---')
st.sidebar.write('🎓 期末成绩管理系统 v1.0')
st.sidebar.write('📊 数据科学期末项目')

if st.sidebar.button('退出登录'):
    st.session_state.logged_in = False
    st.rerun()
