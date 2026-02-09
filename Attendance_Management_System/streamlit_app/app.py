"""
出勤管理系统 - Streamlit网页版
"""
import os
import sys
import streamlit as st
import pandas as pd

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_manager import DataManager


# 初始化Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


def login_page(data_manager):
    """登录页面"""
    st.title('🔐 出勤管理系统')
    st.markdown('---')

    password = st.text_input('请输入密码', type='password', key='login_password')

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button('登录', width='stretch'):
            if data_manager.verify_password(password):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error('密码错误！')


def main_page():
    """主页面"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_manager = DataManager(base_dir)

    # 加载数据
    emp_df = data_manager.read_employees_df()
    att_df = data_manager.read_attendance_df()
    punch_df = data_manager.read_punch_records_df()

    st.title('🏢 出勤管理系统')
    st.markdown('---')

    # 侧边栏
    with st.sidebar:
        st.header('功能菜单')
        page = st.radio(
            '选择功能',
            ['打卡记录处理', '查询功能', '请假管理', '统计功能', '排序功能'],
            label_visibility='collapsed'
        )

    # 页面内容
    if page == '打卡记录处理':
        process_punch_page(data_manager, emp_df, att_df, punch_df)
    elif page == '查询功能':
        query_page(data_manager, emp_df, att_df, punch_df)
    elif page == '请假管理':
        leave_page(data_manager, emp_df, att_df)
    elif page == '统计功能':
        statistics_page(data_manager, emp_df, att_df, punch_df)
    elif page == '排序功能':
        sort_page(data_manager, emp_df, punch_df)


def process_punch_page(data_manager, emp_df, att_df, punch_df):
    """打卡记录处理页面"""
    st.subheader('📅 打卡记录处理')

    st.info('读取当日打卡记录，自动计算迟到次数和旷工天数，并更新月出勤情况文件。')

    if st.button('处理打卡记录', type='primary', width='stretch'):
        with st.spinner('正在处理...'):
            att_df = data_manager.process_punch_records_df(emp_df, att_df, punch_df)
            data_manager.save_attendance_df(att_df)
            data_manager.append_month_records_df(punch_df)

        st.success('✅ 打卡记录处理完成！已更新月出勤情况文件。')

    st.markdown('---')
    st.subheader('当日打卡记录')
    if not punch_df.empty:
        punch_display = punch_df.copy()
        punch_display['到厂时间'] = punch_display['时'].astype(str).str.zfill(2) + ':' + \
                                  punch_display['分'].astype(str).str.zfill(2) + ':' + \
                                  punch_display['秒'].astype(str).str.zfill(2)
        st.dataframe(punch_display[['编号', '到厂时间']], width='stretch')
    else:
        st.warning('暂无打卡记录')


def query_page(data_manager, emp_df, att_df, punch_df):
    """查询功能页面"""
    st.subheader('🔍 查询功能')

    query_type = st.radio('选择查询方式', [
        '按职工编号查询',
        '全勤职工清单',
        '请假天数超过5天的职工',
        '有旷工行为的职工'
    ])

    st.markdown('---')

    if query_type == '按职工编号查询':
        emp_id = st.text_input('请输入职工编号', key='query_emp_id')

        if st.button('查询', width='stretch'):
            emp, att, punch_info = data_manager.query_by_id(emp_df, att_df, punch_df, emp_id)

            if emp is not None:
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown('#### 👤 职工基本信息')
                    st.dataframe(emp, width='stretch')

                with col2:
                    st.markdown('#### 📊 当月出勤情况')
                    st.dataframe(att, width='stretch')

                st.markdown('#### 🕐 当日到厂时间')
                if punch_info:
                    st.success(f'到厂时间：{punch_info}')
                else:
                    st.warning('当日未打卡')
            else:
                st.error('未找到该职工！')

    elif query_type == '全勤职工清单':
        perfect_df = data_manager.get_perfect_attendance(emp_df, att_df)

        if not perfect_df.empty:
            st.success(f'共有 {len(perfect_df)} 名全勤职工')
            st.dataframe(perfect_df, width='stretch')
        else:
            st.warning('暂无全勤职工')

    elif query_type == '请假天数超过5天的职工':
        excessive_df = data_manager.get_excessive_leave(emp_df, att_df)

        if not excessive_df.empty:
            st.success(f'共有 {len(excessive_df)} 名职工请假天数超过5天')
            st.dataframe(excessive_df, width='stretch')
        else:
            st.warning('暂无请假天数超过5天的职工')

    elif query_type == '有旷工行为的职工':
        absent_df = data_manager.get_absent_employees(emp_df, att_df)

        if not absent_df.empty:
            st.success(f'共有 {len(absent_df)} 名职工有旷工行为')
            st.dataframe(absent_df, width='stretch')
        else:
            st.warning('暂无旷工记录')


def leave_page(data_manager, emp_df, att_df):
    """请假管理页面"""
    st.subheader('📝 请假管理')

    emp_id = st.text_input('请输入请假职工的编号', key='leave_emp_id')

    if st.button('提交请假', type='primary', width='stretch'):
        if emp_id:
            emp = emp_df[emp_df['编号'] == emp_id]

            if not emp.empty:
                att_idx = att_df[att_df['编号'] == emp_id].index

                if len(att_idx) > 0:
                    idx_val = att_idx[0]
                    att_df.at[idx_val, '请假天数'] += 1
                    if att_df.at[idx_val, '旷工天数'] > 0:
                        att_df.at[idx_val, '旷工天数'] -= 1

                    data_manager.save_attendance_df(att_df)

                    emp_name = emp.iloc[0]['姓名']
                    leave_days = att_df.at[idx_val, '请假天数']
                    absent_days = att_df.at[idx_val, '旷工天数']

                    st.success(f'✅ 请假信息已更新！\n\n'
                              f'职工：{emp_name}\n'
                              f'请假天数：{leave_days}\n'
                              f'旷工天数：{absent_days}')
                else:
                    st.error('未找到该职工的出勤记录！')
            else:
                st.error('未找到该职工！')
        else:
            st.warning('请输入职工编号！')

    st.markdown('---')
    st.subheader('📋 当前出勤情况')
    st.dataframe(att_df, width='stretch')


def statistics_page(data_manager, emp_df, att_df, punch_df):
    """统计功能页面"""
    st.subheader('📊 统计功能')

    if st.button('显示统计信息', type='primary', width='stretch'):
        stats = data_manager.calculate_statistics(emp_df, att_df, punch_df)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric('职工总数', stats['total_emp'])
            st.metric('全勤职工数', stats['perfect_count'])

        with col2:
            st.metric('全勤率', f'{stats["perfect_rate"]:.2f}%')
            st.metric('当日最长迟到时间', f'{stats["max_late_minutes"] // 60}分钟')

        with col3:
            st.metric('当日迟到职工数', stats['late_today_count'])
            st.metric('当日迟到率', f'{stats["late_today_rate"]:.2f}%')

        st.markdown('---')

        col4, col5, col6 = st.columns(3)

        with col4:
            st.metric('最大请假天数', f'{stats["max_leave_days"]}天')
            st.metric('最大迟到次数', f'{stats["max_late_count"]}次')

        with col5:
            st.metric('最大旷工天数', f'{stats["max_absent_days"]}天')


def sort_page(data_manager, emp_df, punch_df):
    """排序功能页面"""
    st.subheader('📈 排序功能')

    sort_type = st.radio('选择排序方式', [
        '最早到厂的职工',
        '按出生日期升序输出全体职工',
        '按出生日期降序列出全体女职工'
    ])

    st.markdown('---')

    if sort_type == '最早到厂的职工':
        earliest = data_manager.get_earliest_arrival(emp_df, punch_df)

        if earliest:
            st.success(f'🏆 最早到厂职工')
            result_df = pd.DataFrame([earliest])
            st.dataframe(result_df, width='stretch')
        else:
            st.warning('今日无打卡记录')

    elif sort_type == '按出生日期升序输出全体职工':
        sorted_df = data_manager.sort_by_birth_date(emp_df, ascending=True)

        if not sorted_df.empty:
            st.success(f'📊 共 {len(sorted_df)} 名职工')
            st.dataframe(sorted_df, width='stretch')
        else:
            st.warning('暂无职工数据')

    elif sort_type == '按出生日期降序列出全体女职工':
        sorted_df = data_manager.sort_by_birth_date(emp_df, ascending=False, female_only=True)

        if not sorted_df.empty:
            st.success(f'👩 共 {len(sorted_df)} 名女职工')
            st.dataframe(sorted_df, width='stretch')
        else:
            st.warning('暂无女职工数据')


def main():
    """主函数"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_manager = DataManager(base_dir)

    # 页面配置
    st.set_page_config(
        page_title='出勤管理系统',
        page_icon='🏢',
        layout='wide',
        initial_sidebar_state='expanded'
    )

    # 路由
    if not st.session_state.logged_in:
        login_page(data_manager)
    else:
        main_page()


if __name__ == '__main__':
    main()
