"""
班级同学信息管理系统 - Streamlit网页版
"""

import streamlit as st
from data_manager import DataManager, Student


# 初始化
@st.cache_resource
def get_data_manager():
    """获取数据管理器（缓存）"""
    return DataManager()


def show_login_page(data_manager):
    """显示登录页面"""
    st.title("👥 班级同学信息管理系统")

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
    st.title("👥 班级同学信息管理系统")

    # 侧边栏
    with st.sidebar:
        st.header("功能菜单")

        page = st.radio(
            "选择功能",
            ["📋 同学列表", "➕ 添加同学", "🔍 查询同学", "🔑 修改密码"],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # 统计信息
        student_count = data_manager.get_student_count()
        st.info(f"📊 共 {student_count} 位同学")

        st.markdown("---")

        # 退出登录
        if st.button("🚪 退出登录", width='stretch'):
            del st.session_state.logged_in
            del st.session_state.password
            st.rerun()

    # 主内容区域
    if page == "📋 同学列表":
        show_students_list(data_manager)
    elif page == "➕ 添加同学":
        show_add_student(data_manager)
    elif page == "🔍 查询同学":
        show_search_students(data_manager)
    elif page == "🔑 修改密码":
        show_change_password(data_manager)


def show_students_list(data_manager):
    """显示同学列表"""
    st.subheader("同学列表")

    # 加载数据
    students = data_manager.get_students()

    if not students:
        st.warning("还没有同学信息！")
        return

    # 搜索
    search_keyword = st.text_input("搜索同学", placeholder="输入关键词...")

    if search_keyword:
        students = data_manager.search_students(search_keyword)
        if not students:
            st.warning("未找到匹配的同学")
            return

    # 显示表格
    student_data = [s.to_dict() for s in students]
    st.dataframe(student_data, width='stretch', height=400)

    # 操作按钮
    if not search_keyword:
        col1, col2, col3 = st.columns(3)

        # 修改同学
        with col1:
            student_id = st.selectbox(
                "选择要修改的同学",
                students,
                format_func=lambda x: f"{x.name} ({x.student_number})"
            )
            if st.button("✏️ 修改同学", width='stretch'):
                st.session_state.edit_student = student_id
                st.rerun()

        # 删除同学
        with col2:
            delete_id = st.selectbox(
                "选择要删除的同学",
                students,
                format_func=lambda x: f"{x.name} ({x.student_number})",
                key="delete_select"
            )
            if st.button("🗑️ 删除同学", width='stretch'):
                success, message = data_manager.delete_student(delete_id.id)
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


def show_add_student(data_manager):
    """显示添加同学页面"""
    st.subheader("添加同学")

    with st.form("add_student_form"):
        name = st.text_input("姓名 *", placeholder="请输入姓名")
        student_number = st.text_input("学号 *", placeholder="请输入学号")
        dorm = st.text_input("宿舍", placeholder="请输入宿舍号")
        qq = st.text_input("QQ", placeholder="请输入QQ号")
        phone = st.text_input("电话", placeholder="请输入电话号码")

        submitted = st.form_submit_button("添加同学", width='stretch')

        if submitted:
            # 验证数据
            if not name:
                st.error("姓名不能为空！")
                return

            if not student_number:
                st.error("学号不能为空！")
                return

            # 创建学生
            student = Student(0, name, student_number, dorm, qq, phone)

            # 添加学生
            success, message = data_manager.add_student(student)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)


def show_search_students(data_manager):
    """显示查询同学页面"""
    st.subheader("查询同学")

    # 查询关键词
    keyword = st.text_input("查询关键词", placeholder="请输入关键词...")

    # 查询按钮
    search_button = st.button("🔍 查询", width='stretch')

    if search_button or keyword:
        results = data_manager.search_students(keyword)

        if results:
            st.success(f"找到 {len(results)} 位同学")

            # 显示结果
            student_data = [s.to_dict() for s in results]
            st.dataframe(student_data, width='stretch', height=400)

            # 操作按钮
            for i, student in enumerate(results):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{student.name}** - {student.student_number}")
                with col2:
                    if st.button(f"✏️ 编辑", key=f"edit_{i}"):
                        st.session_state.edit_student = student.id
                        st.rerun()
                with col3:
                    if st.button(f"🗑️ 删除", key=f"delete_{i}"):
                        success, message = data_manager.delete_student(student.id)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.warning("未找到匹配的同学")


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


def show_edit_student(data_manager):
    """显示编辑同学页面"""
    st.subheader("修改同学")

    if "edit_student" not in st.session_state:
        st.warning("请先选择要编辑的同学！")
        return

    student_id = st.session_state.edit_student
    students = data_manager.get_students()

    # 查找学生
    student = None
    for s in students:
        if s.id == student_id:
            student = s
            break

    if not student:
        st.error("学生不存在！")
        del st.session_state.edit_student
        return

    with st.form("edit_student_form"):
        name = st.text_input("姓名 *", value=student.name)
        student_number = st.text_input("学号 *", value=student.student_number)
        dorm = st.text_input("宿舍", value=student.dorm)
        qq = st.text_input("QQ", value=student.qq)
        phone = st.text_input("电话", value=student.phone)

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

            if not student_number:
                st.error("学号不能为空！")
                return

            # 更新学生
            new_student = Student(student_id, name, student_number, dorm, qq, phone)
            success, message = data_manager.update_student(new_student)

            if success:
                st.success(message)
                del st.session_state.edit_student
                st.rerun()
            else:
                st.error(message)

        if cancelled:
            del st.session_state.edit_student
            st.rerun()


def main():
    """主函数"""
    # 页面配置
    st.set_page_config(
        page_title="班级同学信息管理系统",
        page_icon="👥",
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
        # 检查是否在编辑学生
        if "edit_student" in st.session_state:
            show_edit_student(data_manager)
        else:
            show_main_page(data_manager)


if __name__ == "__main__":
    main()
