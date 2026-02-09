"""
电话簿管理系统 - Streamlit网页版
"""

import streamlit as st
from data_manager import DataManager, Contact


# 初始化
@st.cache_resource
def get_data_manager():
    """获取数据管理器（缓存）"""
    return DataManager()


def show_login_page(data_manager):
    """显示登录页面"""
    st.title("📞 电话簿管理系统")

    st.markdown("---")

    with st.form("login_form"):
        st.subheader("登录")
        password = st.text_input("密码", type="password", placeholder="默认密码: admin123")
        submit = st.form_submit_button("登录", width='stretch')

        if submit:
            if not password:
                st.error("请输入密码！")
                return False

            if data_manager.verify_password(password):
                st.session_state.logged_in = True
                st.session_state.password = password
                st.success("登录成功！")
                st.rerun()
                return True
            else:
                st.error("密码错误！")
                return False

    return False


def show_main_page(data_manager):
    """显示主页面"""
    st.title("📞 电话簿管理系统")

    # 侧边栏
    with st.sidebar:
        st.header("功能菜单")

        page = st.radio(
            "选择功能",
            ["📋 联系人列表", "➕ 添加联系人", "🔍 查询联系人", "🔑 修改密码"],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # 统计信息
        contact_count = data_manager.get_contact_count()
        st.info(f"📊 共 {contact_count} 位联系人")

        st.markdown("---")

        # 退出登录
        if st.button("🚪 退出登录", width='stretch'):
            del st.session_state.logged_in
            del st.session_state.password
            st.rerun()

    # 主内容区域
    if page == "📋 联系人列表":
        show_contacts_list(data_manager)
    elif page == "➕ 添加联系人":
        show_add_contact(data_manager)
    elif page == "🔍 查询联系人":
        show_search_contacts(data_manager)
    elif page == "🔑 修改密码":
        show_change_password(data_manager)


def show_contacts_list(data_manager):
    """显示联系人列表"""
    st.subheader("联系人列表")

    # 加载数据
    contacts = data_manager.get_contacts()

    if not contacts:
        st.warning("电话簿为空！")
        return

    # 排序选项
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        sort_field = st.selectbox("排序方式", ["姓名", "电话号码"])

    with col2:
        search_keyword = st.text_input("搜索关键词", placeholder="输入关键词...")

    with col3:
        if st.button("🔄 刷新", width='stretch'):
            data_manager.load_data()
            st.rerun()

    # 排序
    if sort_field == "姓名":
        data_manager.sort_contacts('name')
    else:
        data_manager.sort_contacts('phone')

    # 搜索
    if search_keyword:
        contacts = data_manager.search_contacts(search_keyword, 'name')
        if not contacts:
            contacts = data_manager.search_contacts(search_keyword, 'phone')

    # 显示表格
    if contacts:
        contact_data = [c.to_dict() for c in contacts]
        st.dataframe(contact_data, width='stretch', height=400)

        col1, col2, col3 = st.columns(3)

        # 修改联系人
        with col1:
            contact_id = st.selectbox(
                "选择要修改的联系人",
                contacts,
                format_func=lambda x: f"{x.name} ({x.phone})"
            )
            if st.button("✏️ 修改联系人", width='stretch'):
                st.session_state.edit_contact = contact_id
                st.rerun()

        # 删除联系人
        with col2:
            delete_id = st.selectbox(
                "选择要删除的联系人",
                contacts,
                format_func=lambda x: f"{x.name} ({x.phone})",
                key="delete_select"
            )
            if st.button("🗑️ 删除联系人", width='stretch'):
                success, message = data_manager.delete_contact(delete_id.id)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

        # 保存数据
        with col3:
            if st.button("💾 保存数据", width='stretch'):
                if data_manager.save_data():
                    st.success("数据保存成功！")
                else:
                    st.error("数据保存失败！")
    else:
        st.info("未找到匹配的联系人")


def show_add_contact(data_manager):
    """显示添加联系人页面"""
    st.subheader("添加联系人")

    with st.form("add_contact_form"):
        name = st.text_input("姓名 *", placeholder="请输入姓名")
        work_unit = st.text_input("工作单位", placeholder="请输入工作单位")
        phone = st.text_input("电话号码 *", placeholder="请输入电话号码（7-15位）")
        email = st.text_input("E-mail地址 *", placeholder="请输入E-mail地址")

        submitted = st.form_submit_button("添加联系人", width='stretch')

        if submitted:
            # 验证数据
            if not name:
                st.error("姓名不能为空！")
                return

            if not phone:
                st.error("电话号码不能为空！")
                return

            if not email:
                st.error("E-mail地址不能为空！")
                return

            if not data_manager.is_valid_phone(phone):
                st.error("电话号码格式错误！\n\n要求：7-15位数字（可包含连字符或空格）")
                return

            if not data_manager.is_valid_email(email):
                st.error("E-mail地址格式错误！")
                return

            # 创建联系人
            contact = Contact(0, name, work_unit, phone, email)

            # 添加联系人
            success, message = data_manager.add_contact(contact)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)


def show_search_contacts(data_manager):
    """显示查询联系人页面"""
    st.subheader("查询联系人")

    # 查询方式
    search_type = st.radio(
        "查询方式",
        ["按姓名查询", "按电话号码查询"],
        horizontal=True
    )

    # 查询关键词
    keyword = st.text_input("查询关键词", placeholder="请输入关键词...")

    # 查询按钮
    search_button = st.button("🔍 查询", width='stretch')

    if search_button or keyword:
        field = 'name' if search_type == "按姓名查询" else 'phone'
        results = data_manager.search_contacts(keyword, field)

        if results:
            st.success(f"找到 {len(results)} 位联系人")

            # 显示结果
            contact_data = [c.to_dict() for c in results]
            st.dataframe(contact_data, width='stretch', height=400)

            # 操作按钮
            for i, contact in enumerate(results):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{contact.name}** - {contact.phone}")
                with col2:
                    if st.button(f"✏️ 编辑", key=f"edit_{i}"):
                        st.session_state.edit_contact = contact.id
                        st.rerun()
                with col3:
                    if st.button(f"🗑️ 删除", key=f"delete_{i}"):
                        success, message = data_manager.delete_contact(contact.id)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.warning("未找到匹配的联系人")


def show_change_password(data_manager):
    """显示修改密码页面"""
    st.subheader("修改密码")

    with st.form("change_password_form"):
        old_password = st.text_input("旧密码 *", type="password")
        new_password = st.text_input("新密码 *", type="password")
        confirm_password = st.text_input("确认新密码 *", type="password")

        submitted = st.form_submit_button("修改密码", width='stretch')

        if submitted:
            # 验证数据
            if not old_password or not new_password or not confirm_password:
                st.error("请填写所有字段！")
                return

            if new_password != confirm_password:
                st.error("两次输入的新密码不一致！")
                return

            # 修改密码
            if data_manager.change_password(old_password, new_password):
                st.success("密码修改成功！")
                st.session_state.password = new_password
            else:
                st.error("旧密码错误！")


def show_edit_contact(data_manager):
    """显示编辑联系人页面"""
    st.subheader("修改联系人")

    if "edit_contact" not in st.session_state:
        st.warning("请先选择要编辑的联系人！")
        return

    contact_id = st.session_state.edit_contact
    contacts = data_manager.get_contacts()

    # 查找联系人
    contact = None
    for c in contacts:
        if c.id == contact_id:
            contact = c
            break

    if not contact:
        st.error("联系人不存在！")
        del st.session_state.edit_contact
        return

    with st.form("edit_contact_form"):
        name = st.text_input("姓名 *", value=contact.name)
        work_unit = st.text_input("工作单位", value=contact.work_unit)
        phone = st.text_input("电话号码 *", value=contact.phone)
        email = st.text_input("E-mail地址 *", value=contact.email)

        col1, col2 = st.columns(2)

        with col1:
            submitted = st.form_submit_button("保存修改", width='stretch')

        with col2:
            cancelled = st.form_submit_button("取消", width='stretch')

        if submitted:
            # 验证数据
            if not name:
                st.error("姓名不能为空！")
                return

            if not phone:
                st.error("电话号码不能为空！")
                return

            if not email:
                st.error("E-mail地址不能为空！")
                return

            if not data_manager.is_valid_phone(phone):
                st.error("电话号码格式错误！\n\n要求：7-15位数字（可包含连字符或空格）")
                return

            if not data_manager.is_valid_email(email):
                st.error("E-mail地址格式错误！")
                return

            # 更新联系人
            new_contact = Contact(contact_id, name, work_unit, phone, email)
            success, message = data_manager.update_contact(new_contact)

            if success:
                st.success(message)
                del st.session_state.edit_contact
                st.rerun()
            else:
                st.error(message)

        if cancelled:
            del st.session_state.edit_contact
            st.rerun()


def main():
    """主函数"""
    # 页面配置
    st.set_page_config(
        page_title="电话簿管理系统",
        page_icon="📞",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 获取数据管理器
    data_manager = get_data_manager()

    # 检查登录状态
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # 显示页面
    if not st.session_state.logged_in:
        show_login_page(data_manager)
    else:
        # 检查是否在编辑联系人
        if "edit_contact" in st.session_state:
            show_edit_contact(data_manager)
        else:
            show_main_page(data_manager)


if __name__ == "__main__":
    main()
