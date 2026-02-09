"""
银行账目管理系统 - Streamlit 网页版
"""
import os
import streamlit as st
from data_manager import DataManager

# 页面配置
st.set_page_config(
    page_title='银行账目管理系统',
    page_icon='🏦',
    layout='wide'
)

# 获取项目根目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_manager = DataManager(base_dir)

# 会话状态
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'accounts' not in st.session_state:
    st.session_state.accounts = []


def login():
    """登录页面"""
    st.title('🏦 银行账目管理系统')

    with st.form('login_form'):
        password = st.text_input('请输入密码', type='password')
        submit = st.form_submit_button('登录')

        if submit:
            if data_manager.verify_password(password):
                st.session_state.logged_in = True
                st.session_state.accounts = data_manager.read_accounts()
                st.success('登录成功！')
                st.rerun()
            else:
                st.error('密码错误！')


def open_account():
    """开户"""
    st.subheader('开户')

    with st.form('open_account'):
        name = st.text_input('姓名')
        id_card = st.text_input('身份证号')
        date = st.text_input('开户日期 (YYYY-MM-DD)')
        amount = st.number_input('开户金额', value=0.0, min_value=0.0)

        if st.form_submit_button('提交'):
            if not name or not id_card or not date:
                st.warning('请填写完整信息！')
                return

            # 简单验证
            if len(id_card) != 18:
                st.warning('身份证号格式不正确！')
                return

            account_no = data_manager.get_next_account_no(st.session_state.accounts)
            st.session_state.accounts.append({
                'account_no': account_no,
                'name': name,
                'id_card': id_card,
                'create_date': date,
                'balance': amount
            })

            data_manager.save_accounts(st.session_state.accounts)
            st.success(f'开户成功！账号: {account_no}, 余额: {amount:.2f}元')


def borrow_repay_deposit(operation):
    """借款/还款/存款"""
    titles = {1: '借款', 2: '还款', 3: '存款'}
    st.subheader(titles[operation])

    account_no = st.number_input('账号', min_value=10000, value=10001, step=1)
    amount = st.number_input('金额', value=0.0, min_value=0.0)

    if st.button('提交'):
        account = None
        for acc in st.session_state.accounts:
            if acc['account_no'] == account_no:
                account = acc
                break

        if not account:
            st.warning('未找到该账户！')
            return

        old_balance = account['balance']

        if operation == 1:  # 借款
            account['balance'] -= amount
            st.success(f'借款成功！')
        elif operation == 2:  # 还款
            if account['balance'] + amount > 0:
                st.warning('还款金额超过借款额！')
                return
            account['balance'] += amount
            st.success(f'还款成功！')
        else:  # 存款
            account['balance'] += amount
            st.success(f'存款成功！')

        # 表格形式显示账户变更信息
        st.markdown("### 账户余额变更")
        df_data = {
            '字段': ['账号', '姓名', '操作前余额', '变更金额', '操作后余额'],
            '值': [
                str(account['account_no']),
                account['name'],
                f"{old_balance:.2f}元",
                f"{amount:.2f}元",
                f"{account['balance']:.2f}元"
            ]
        }
        st.dataframe(df_data, hide_index=True, width='stretch')

        data_manager.save_accounts(st.session_state.accounts)


def query_account():
    """查询账户"""
    st.subheader('查询账户')

    account_no = st.number_input('账号', min_value=10000, value=10001, step=1)

    if st.button('查询'):
        for acc in st.session_state.accounts:
            if acc['account_no'] == account_no:
                # 表格形式显示
                st.markdown("### 账户信息")
                df_data = {
                    '字段': ['账号', '姓名', '身份证号', '开户日期', '余额'],
                    '值': [
                        str(acc['account_no']),
                        acc['name'],
                        acc['id_card'],
                        acc['create_date'],
                        f"{acc['balance']:.2f}元"
                    ]
                }
                st.dataframe(df_data, hide_index=True, width='stretch')
                return
        st.warning('未找到该账户！')


def show_max_borrower_depositor(mode):
    """显示最大借款/存款账户"""
    titles = {1: '最大借款账户', 2: '最大存款账户'}
    st.subheader(titles[mode])

    target_account = None
    target_value = 0

    for acc in st.session_state.accounts:
        if acc['account_no'] == -1:
            continue

        if mode == 1:  # 借款
            if acc['balance'] < 0:
                if acc['balance'] < target_value:
                    target_value = acc['balance']
                    target_account = acc
        else:  # 存款
            if acc['balance'] > 0:
                if acc['balance'] > target_value:
                    target_value = acc['balance']
                    target_account = acc

    if target_account:
        # 表格形式显示
        df_data = {
            '字段': ['账号', '姓名', '身份证号', '开户日期', '余额'],
            '值': [
                str(target_account['account_no']),
                target_account['name'],
                target_account['id_card'],
                target_account['create_date'],
                f"{target_account['balance']:.2f}元"
            ]
        }
        st.dataframe(df_data, hide_index=True, width='stretch')
    else:
        st.warning('未找到相关账户！')


def sort_accounts(mode):
    """排序显示账户"""
    titles = {1: '按借款余额排序', 2: '按存款余额排序', 3: '按开户日期排序'}
    st.subheader(titles[mode])

    filtered_accounts = []

    for acc in st.session_state.accounts:
        if acc['account_no'] == -1:
            continue

        if mode == 1:  # 借款
            if acc['balance'] < 0:
                filtered_accounts.append(acc)
        elif mode == 2:  # 存款
            if acc['balance'] > 0:
                filtered_accounts.append(acc)
        else:  # 开户日期
            filtered_accounts.append(acc)

    if mode == 1 or mode == 2:
        filtered_accounts.sort(key=lambda x: x['balance'], reverse=True)
    else:
        filtered_accounts.sort(key=lambda x: x['create_date'])

    if filtered_accounts:
        # 格式化余额显示
        df_data = {
            '账号': [acc['account_no'] for acc in filtered_accounts],
            '姓名': [acc['name'] for acc in filtered_accounts],
            '身份证号': [acc['id_card'] for acc in filtered_accounts],
            '开户日期': [acc['create_date'] for acc in filtered_accounts],
            '余额': [f"{acc['balance']:.2f}元" for acc in filtered_accounts]
        }
        st.dataframe(df_data, hide_index=True, width='stretch')
    else:
        st.warning('未找到相关账户！')


def delete_account():
    """清户"""
    st.subheader('清户')

    account_no = st.number_input('要删除的账号', min_value=10000, value=10001, step=1)

    if st.button('删除'):
        for acc in st.session_state.accounts:
            if acc['account_no'] == account_no:
                st.warning(f'确认删除账号 {account_no}？此操作不可恢复！')
                if st.button('确认删除'):
                    acc['account_no'] = -1
                    data_manager.save_accounts(st.session_state.accounts)
                    st.success('账户已删除！')
                return
        st.warning('未找到该账户！')


def compact_files():
    """文件紧缩"""
    st.subheader('文件紧缩')

    if st.button('执行文件紧缩'):
        original_count = len(st.session_state.accounts)
        st.session_state.accounts = [acc for acc in st.session_state.accounts if acc['account_no'] != -1]
        new_count = len(st.session_state.accounts)
        data_manager.save_accounts(st.session_state.accounts)
        st.success(f'文件紧缩完成！删除了 {original_count - new_count} 个账户。')


def show_statistics():
    """统计信息"""
    st.subheader('统计信息')

    total_count = len([acc for acc in st.session_state.accounts if acc['account_no'] != -1])
    borrow_count = len([acc for acc in st.session_state.accounts if acc['account_no'] != -1 and acc['balance'] < 0])
    deposit_count = len([acc for acc in st.session_state.accounts if acc['account_no'] != -1 and acc['balance'] > 0])
    total_borrow = sum([-acc['balance'] for acc in st.session_state.accounts if acc['account_no'] != -1 and acc['balance'] < 0])
    total_deposit = sum([acc['balance'] for acc in st.session_state.accounts if acc['account_no'] != -1 and acc['balance'] > 0])

    st.metric('当前账户个数', total_count)
    st.metric('借款账户数', borrow_count)
    st.metric('存款账户数', deposit_count)
    st.metric('当前借款总额', f'{total_borrow:.2f}元')
    st.metric('当前存款总额', f'{total_deposit:.2f}元')
    st.metric('差额', f'{total_deposit - total_borrow:.2f}元')


def check_warnings():
    """检查预警账户"""
    warnings = [acc for acc in st.session_state.accounts if acc['account_no'] != -1 and acc['balance'] < -50000]

    if warnings:
        st.warning('以下账户借款超过5万元：')
        # 表格形式显示预警账户
        df_data = {
            '账号': [acc['account_no'] for acc in warnings],
            '姓名': [acc['name'] for acc in warnings],
            '借款额': [f"{-acc['balance']:.2f}元" for acc in warnings]
        }
        st.dataframe(df_data, hide_index=True, width='stretch')


# 主程序
if not st.session_state.logged_in:
    login()
else:
    # 侧边栏导航
    page = st.sidebar.selectbox(
        '选择功能',
        ['开户', '借款', '还款', '存款', '查询账户', '最大借款账户', '最大存款账户',
         '按借款余额排序', '按存款余额排序', '按开户日期排序', '清户', '文件紧缩', '统计信息']
    )

    # 刷新数据
    st.session_state.accounts = data_manager.read_accounts()

    # 显示预警
    check_warnings()

    # 根据选择显示不同页面
    if page == '开户':
        open_account()
    elif page == '借款':
        borrow_repay_deposit(1)
    elif page == '还款':
        borrow_repay_deposit(2)
    elif page == '存款':
        borrow_repay_deposit(3)
    elif page == '查询账户':
        query_account()
    elif page == '最大借款账户':
        show_max_borrower_depositor(1)
    elif page == '最大存款账户':
        show_max_borrower_depositor(2)
    elif page == '按借款余额排序':
        sort_accounts(1)
    elif page == '按存款余额排序':
        sort_accounts(2)
    elif page == '按开户日期排序':
        sort_accounts(3)
    elif page == '清户':
        delete_account()
    elif page == '文件紧缩':
        compact_files()
    elif page == '统计信息':
        show_statistics()
