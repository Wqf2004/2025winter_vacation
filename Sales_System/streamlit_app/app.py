"""
销售系统 - Streamlit 网页版
"""
import os
import streamlit as st
from data_manager import DataManager
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title='销售系统',
    page_icon='🛒',
    layout='wide'
)

# 获取项目根目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_manager = DataManager(base_dir)

# 会话状态
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None


def login():
    """登录页面"""
    st.title('🛒 销售系统')

    with st.form('login_form'):
        username = st.text_input('用户名')
        password = st.text_input('密码', type='password')
        submit = st.form_submit_button('登录')

        if submit:
            user = data_manager.verify_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.current_user = user
                st.success('登录成功！')
                st.rerun()
            else:
                st.error('用户名或密码错误！')


def show_products():
    """显示所有商品"""
    st.subheader('商品浏览')
    products = data_manager.read_products()

    if products:
        df_data = {
            '商品ID': [p['id'] for p in products],
            '商品名称': [p['name'] for p in products],
            '单价': [f"{p['price']:.2f}元" for p in products],
            '库存': [p['stock'] for p in products]
        }
        st.dataframe(df_data, hide_index=True, width='stretch')
    else:
        st.warning('暂无商品数据！')


def sell_product():
    """销售商品"""
    st.subheader('销售商品')
    products = data_manager.read_products()

    if not products:
        st.warning('暂无商品数据！')
        return

    # 选择商品
    product_options = {f"{p['id']} - {p['name']}": p for p in products}
    selected = st.selectbox('选择商品', list(product_options.keys()))
    product = product_options[selected]

    # 输入数量
    quantity = st.number_input('销售数量', min_value=1, max_value=product['stock'], value=1)

    if st.button('确认销售'):
        # 更新库存
        product['stock'] -= quantity
        data_manager.save_products(products)

        # 添加销售记录
        sales = data_manager.read_sales()
        new_id = len(sales) + 1
        today = datetime.now().strftime('%Y-%m-%d')

        sales.append({
            'id': new_id,
            'product_id': product['id'],
            'product_name': product['name'],
            'quantity': quantity,
            'unit_price': product['price'],
            'total_amount': quantity * product['price'],
            'date': today,
            'seller_id': st.session_state.current_user['id']
        })
        data_manager.save_sales(sales)

        st.success(f'销售成功！总金额: {quantity * product["price"]:.2f}元')


def show_daily_report():
    """日报表"""
    st.subheader('销售日报表')

    sales = data_manager.read_sales()
    users = data_manager.read_users()

    # 获取当前日期
    today = datetime.now().strftime('%Y-%m-%d')

    # 根据角色过滤
    filtered_sales = []
    for sale in sales:
        if sale['date'] == today:
            if st.session_state.current_user['role'] == 3:  # 销售员只能看自己的
                if sale['seller_id'] == st.session_state.current_user['id']:
                    filtered_sales.append(sale)
            else:  # 管理员和店长看所有
                filtered_sales.append(sale)

    if filtered_sales:
        df_data = {
            '销售ID': [s['id'] for s in filtered_sales],
            '商品名称': [s['product_name'] for s in filtered_sales],
            '销售数量': [s['quantity'] for s in filtered_sales],
            '单价': [f"{s['unit_price']:.2f}元" for s in filtered_sales],
            '总金额': [f"{s['total_amount']:.2f}元" for s in filtered_sales],
            '销售员': [
                next((u['username'] for u in users if u['id'] == s['seller_id']), '未知')
                for s in filtered_sales
            ]
        }
        st.dataframe(df_data, hide_index=True, width='stretch')

        total_amount = sum(s['total_amount'] for s in filtered_sales)
        st.metric('当日总销售额', f'{total_amount:.2f}元')
    else:
        st.warning('今日暂无销售记录！')


def show_monthly_report():
    """月报表"""
    st.subheader('销售月报表')

    sales = data_manager.read_sales()
    users = data_manager.read_users()

    # 获取当前月份
    current_month = datetime.now().strftime('%Y-%m')

    # 根据角色过滤
    filtered_sales = []
    for sale in sales:
        if sale['date'].startswith(current_month):
            if st.session_state.current_user['role'] == 3:
                if sale['seller_id'] == st.session_state.current_user['id']:
                    filtered_sales.append(sale)
            else:
                filtered_sales.append(sale)

    if filtered_sales:
        df_data = {
            '销售ID': [s['id'] for s in filtered_sales],
            '商品名称': [s['product_name'] for s in filtered_sales],
            '销售数量': [s['quantity'] for s in filtered_sales],
            '单价': [f"{s['unit_price']:.2f}元" for s in filtered_sales],
            '总金额': [f"{s['total_amount']:.2f}元" for s in filtered_sales],
            '销售日期': [s['date'] for s in filtered_sales],
            '销售员': [
                next((u['username'] for u in users if u['id'] == s['seller_id']), '未知')
                for s in filtered_sales
            ]
        }
        st.dataframe(df_data, hide_index=True, width='stretch')

        total_amount = sum(s['total_amount'] for s in filtered_sales)
        st.metric('当月总销售额', f'{total_amount:.2f}元')
    else:
        st.warning('本月暂无销售记录！')


def show_product_sales_report():
    """商品销售量报表"""
    st.subheader('商品销售量报表')

    sales = data_manager.read_sales()
    products = data_manager.read_products()

    # 统计每个商品的销售数据
    product_stats = {}
    for sale in sales:
        pid = sale['product_id']
        if pid not in product_stats:
            product_stats[pid] = {
                'name': sale['product_name'],
                'quantity': 0,
                'amount': 0.0
            }
        product_stats[pid]['quantity'] += sale['quantity']
        product_stats[pid]['amount'] += sale['total_amount']

    if product_stats:
        df_data = {
            '商品ID': list(product_stats.keys()),
            '商品名称': [p['name'] for p in product_stats.values()],
            '销售数量': [p['quantity'] for p in product_stats.values()],
            '销售金额': [f"{p['amount']:.2f}元" for p in product_stats.values()]
        }
        st.dataframe(df_data, hide_index=True, width='stretch')
    else:
        st.warning('暂无销售记录！')


def show_seller_performance_report():
    """销售员业绩报表"""
    st.subheader('销售员业绩报表')

    sales = data_manager.read_sales()
    users = [u for u in data_manager.read_users() if u['role'] == 3]  # 只显示销售员

    # 统计每个销售员的业绩
    seller_stats = {}
    for sale in sales:
        sid = sale['seller_id']
        if sid not in seller_stats:
            seller_stats[sid] = {
                'name': next((u['username'] for u in users if u['id'] == sid), '未知'),
                'count': 0,
                'amount': 0.0
            }
        seller_stats[sid]['count'] += 1
        seller_stats[sid]['amount'] += sale['total_amount']

    if seller_stats:
        df_data = {
            '销售员ID': list(seller_stats.keys()),
            '销售员姓名': [s['name'] for s in seller_stats.values()],
            '销售单数': [s['count'] for s in seller_stats.values()],
            '销售总额': [f"{s['amount']:.2f}元" for s in seller_stats.values()]
        }
        st.dataframe(df_data, hide_index=True, width='stretch')

        # 按销售额排序
        sorted_sellers = sorted(seller_stats.values(), key=lambda x: x['amount'], reverse=True)
        st.markdown('### 📊 销售排行榜')
        for i, seller in enumerate(sorted_sellers, 1):
            st.write(f"{i}. **{seller['name']}**: {seller['amount']:.2f}元 ({seller['count']}单)")
    else:
        st.warning('暂无销售记录！')


def modify_password():
    """修改密码"""
    st.subheader('修改密码')

    users = data_manager.read_users()
    current_user = st.session_state.current_user

    with st.form('password_form'):
        old_password = st.text_input('旧密码', type='password')
        new_password = st.text_input('新密码', type='password')
        confirm_password = st.text_input('确认密码', type='password')
        submit = st.form_submit_button('修改密码')

        if submit:
            if not old_password or not new_password:
                st.error('密码不能为空！')
                return

            user = data_manager.verify_user(current_user['username'], old_password)
            if not user:
                st.error('旧密码错误！')
                return

            if new_password != confirm_password:
                st.error('两次密码不一致！')
                return

            for u in users:
                if u['id'] == current_user['id']:
                    u['password'] = new_password
                    break

            data_manager.save_users(users)
            current_user['password'] = new_password
            st.success('密码修改成功！')


def manage_users():
    """用户管理"""
    st.subheader('用户管理')

    users = data_manager.read_users()
    role_names = {1: '管理员', 2: '店长', 3: '销售员'}

    # 选择操作
    action = st.radio('操作', ['查看用户', '添加用户', '修改用户', '删除用户'], horizontal=True)

    if action == '查看用户':
        if users:
            df_data = {
                '用户ID': [u['id'] for u in users],
                '用户名': [u['username'] for u in users],
                '角色': [role_names.get(u['role'], '未知') for u in users]
            }
            st.dataframe(df_data, hide_index=True, width='stretch')
        else:
            st.warning('暂无用户数据！')

    elif action == '添加用户':
        with st.form('add_user_form'):
            username = st.text_input('用户名')
            password = st.text_input('密码', type='password')
            role = st.selectbox('角色', ['管理员', '店长', '销售员'], format_func=lambda x: x)
            submit = st.form_submit_button('添加')

            if submit:
                if not username or not password:
                    st.error('用户名和密码不能为空！')
                    return

                new_id = max(u['id'] for u in users) + 1 if users else 1
                role_map = {'管理员': 1, '店长': 2, '销售员': 3}

                users.append({
                    'id': new_id,
                    'username': username,
                    'password': password,
                    'role': role_map[role]
                })

                data_manager.save_users(users)
                st.success(f'用户添加成功！用户ID: {new_id}')
                st.rerun()

    elif action == '修改用户':
        if not users:
            st.warning('暂无用户数据！')
            return

        user_options = {f"{u['id']} - {u['username']}": u for u in users}
        selected = st.selectbox('选择用户', list(user_options.keys()))
        user = user_options[selected]

        with st.form('edit_user_form'):
            username = st.text_input('用户名', value=user['username'])
            password = st.text_input('新密码（留空不修改）', type='password')
            role = st.selectbox('角色', ['管理员', '店长', '销售员'],
                             index=['管理员', '店长', '销售员'].index(
                                 role_names.get(user['role'], '销售员')
                             ))
            submit = st.form_submit_button('修改')

            if submit:
                if not username:
                    st.error('用户名不能为空！')
                    return

                user['username'] = username
                if password:
                    user['password'] = password
                role_map = {'管理员': 1, '店长': 2, '销售员': 3}
                user['role'] = role_map[role]

                data_manager.save_users(users)
                st.success('用户修改成功！')
                st.rerun()

    elif action == '删除用户':
        if not users:
            st.warning('暂无用户数据！')
            return

        user_options = {f"{u['id']} - {u['username']}": u for u in users}
        selected = st.selectbox('选择用户', list(user_options.keys()))
        user = user_options[selected]

        if st.button('删除', type='primary'):
            users.remove(user)
            data_manager.save_users(users)
            st.success('用户删除成功！')
            st.rerun()


def manage_products():
    """商品管理"""
    st.subheader('商品管理')

    products = data_manager.read_products()

    # 选择操作
    action = st.radio('操作', ['查看商品', '添加商品', '修改商品', '删除商品'], horizontal=True)

    if action == '查看商品':
        if products:
            df_data = {
                '商品ID': [p['id'] for p in products],
                '商品名称': [p['name'] for p in products],
                '单价': [f"{p['price']:.2f}元" for p in products],
                '库存': [p['stock'] for p in products]
            }
            st.dataframe(df_data, hide_index=True, width='stretch')
        else:
            st.warning('暂无商品数据！')

    elif action == '添加商品':
        with st.form('add_product_form'):
            name = st.text_input('商品名称')
            price = st.number_input('单价', min_value=0.01, value=0.01, step=0.01, format='%.2f')
            stock = st.number_input('库存', min_value=0, value=0)
            submit = st.form_submit_button('添加')

            if submit:
                if not name:
                    st.error('商品名称不能为空！')
                    return

                new_id = max(p['id'] for p in products) + 1 if products else 1001

                products.append({
                    'id': new_id,
                    'name': name,
                    'price': price,
                    'stock': stock
                })

                data_manager.save_products(products)
                st.success(f'商品添加成功！商品ID: {new_id}')
                st.rerun()

    elif action == '修改商品':
        if not products:
            st.warning('暂无商品数据！')
            return

        product_options = {f"{p['id']} - {p['name']}": p for p in products}
        selected = st.selectbox('选择商品', list(product_options.keys()))
        product = product_options[selected]

        with st.form('edit_product_form'):
            name = st.text_input('商品名称', value=product['name'])
            price = st.number_input('单价', min_value=0.01, value=product['price'],
                                step=0.01, format='%.2f')
            stock = st.number_input('库存', min_value=0, value=product['stock'])
            submit = st.form_submit_button('修改')

            if submit:
                if not name:
                    st.error('商品名称不能为空！')
                    return

                product['name'] = name
                product['price'] = price
                product['stock'] = stock

                data_manager.save_products(products)
                st.success('商品修改成功！')
                st.rerun()

    elif action == '删除商品':
        if not products:
            st.warning('暂无商品数据！')
            return

        product_options = {f"{p['id']} - {p['name']}": p for p in products}
        selected = st.selectbox('选择商品', list(product_options.keys()))
        product = product_options[selected]

        if st.button('删除', type='primary'):
            products.remove(product)
            data_manager.save_products(products)
            st.success('商品删除成功！')
            st.rerun()


# 主程序
if not st.session_state.logged_in:
    login()
else:
    # 根据角色显示不同菜单
    role = st.session_state.current_user['role']
    role_names = {1: '管理员', 2: '店长', 3: '销售员'}
    st.title(f'🛒 销售系统 - {role_names[role]}')

    # 侧边栏导航
    menu_options = ['修改密码', '商品浏览', '日报表', '月报表']
    if role == 1:
        menu_options.extend(['用户管理', '商品管理', '商品销售量报表', '销售员业绩报表'])
    elif role == 2:
        menu_options.extend(['商品管理', '商品销售量报表', '销售员业绩报表'])
    elif role == 3:
        menu_options.extend(['销售商品'])

    page = st.sidebar.selectbox('选择功能', menu_options)

    # 根据选择显示不同页面
    if page == '修改密码':
        modify_password()
    elif page == '商品浏览':
        show_products()
    elif page == '销售商品':
        if role == 3:
            sell_product()
        else:
            st.warning('只有销售员可以销售商品！')
    elif page == '用户管理' and role == 1:
        manage_users()
    elif page == '商品管理' and role in [1, 2]:
        manage_products()
    elif page == '日报表':
        show_daily_report()
    elif page == '月报表':
        show_monthly_report()
    elif page == '商品销售量报表':
        show_product_sales_report()
    elif page == '销售员业绩报表':
        show_seller_performance_report()

    # 登出按钮
    if st.sidebar.button('退出登录'):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
