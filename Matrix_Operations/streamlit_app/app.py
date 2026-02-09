"""
矩阵运算系统 - Streamlit网页版
"""
import numpy as np
import streamlit as st
import pandas as pd


def create_empty_matrix(rows, cols):
    """创建空矩阵"""
    return np.zeros((rows, cols))


def parse_matrix_from_dataframe(df):
    """从DataFrame解析矩阵"""
    try:
        matrix = df.values.astype(float)
        return matrix
    except Exception as e:
        st.error(f"错误：解析矩阵时出错 - {str(e)}")
        return None


def display_matrix(matrix, title, color_theme="purple"):
    """显示矩阵"""
    st.subheader(title)

    # 转换为DataFrame
    df = pd.DataFrame(matrix)
    df.index = [f"行{i+1}" for i in range(len(matrix))]
    df.columns = [f"列{j+1}" for j in range(matrix.shape[1])]

    # 根据主题设置样式
    if color_theme == "blue":
        df_style = df.style.set_properties(
            **{'background-color': '#e6f0ff', 'text-align': 'center'}
        )
    elif color_theme == "green":
        df_style = df.style.set_properties(
            **{'background-color': '#e6ffe6', 'text-align': 'center'}
        )
    elif color_theme == "purple":
        df_style = df.style.set_properties(
            **{'background-color': '#f5ebff', 'text-align': 'center'}
        )
    elif color_theme == "orange":
        df_style = df.style.set_properties(
            **{'background-color': '#fffadc', 'text-align': 'center'}
        )
    elif color_theme == "yellow":
        df_style = df.style.set_properties(
            **{'background-color': '#ffffe6', 'text-align': 'center'}
        )
    elif color_theme == "pink":
        df_style = df.style.set_properties(
            **{'background-color': '#ffe6e6', 'text-align': 'center'}
        )
    elif color_theme == "cyan":
        df_style = df.style.set_properties(
            **{'background-color': '#e6fafa', 'text-align': 'center'}
        )
    else:
        df_style = df.style.set_properties(
            **{'background-color': '#f0f0f0', 'text-align': 'center'}
        )

    st.dataframe(df_style, width='stretch')


def matrix_input_widget(key_prefix, title, color_theme="blue", default_rows=2, default_cols=2,
                     sync_rows_key=None, sync_cols_key=None):
    """矩阵输入控件

    Args:
        key_prefix: 控件key前缀
        title: 标题
        color_theme: 颜色主题
        default_rows: 默认行数
        default_cols: 默认列数
        sync_rows_key: 同步行数的session_state key
        sync_cols_key: 同步列数的session_state key
    """
    st.markdown(f"### {title}")

    # 尺寸控制
    col_size1, col_size2 = st.columns(2)

    # 初始化当前矩阵的尺寸
    if f"{key_prefix}_rows" not in st.session_state:
        st.session_state[f"{key_prefix}_rows"] = default_rows
    if f"{key_prefix}_cols" not in st.session_state:
        st.session_state[f"{key_prefix}_cols"] = default_cols

    # 联调回调函数
    def on_rows_change():
        # 保存当前值
        st.session_state[f"{key_prefix}_rows_saved"] = st.session_state[f"{key_prefix}_rows"]
        # 联调：如果有同步key，更新对应的值
        if sync_rows_key:
            st.session_state[sync_rows_key] = st.session_state[f"{key_prefix}_rows"]
            # 刷新其他矩阵的显示值
            target_prefix = sync_rows_key.replace("_rows_saved", "")
            if f"{target_prefix}_rows" in st.session_state:
                st.session_state[f"{target_prefix}_rows"] = st.session_state[f"{key_prefix}_rows"]

    def on_cols_change():
        # 保存当前值
        st.session_state[f"{key_prefix}_cols_saved"] = st.session_state[f"{key_prefix}_cols"]
        # 联调：如果有同步key，更新对应的值
        if sync_cols_key:
            st.session_state[sync_cols_key] = st.session_state[f"{key_prefix}_cols"]
            # 刷新其他矩阵的显示值
            target_prefix = sync_cols_key.replace("_cols_saved", "")
            if f"{target_prefix}_cols" in st.session_state:
                st.session_state[f"{target_prefix}_cols"] = st.session_state[f"{key_prefix}_cols"]

    with col_size1:
        rows = st.number_input(
            "行数",
            min_value=1,
            max_value=20,
            value=int(st.session_state[f"{key_prefix}_rows"]),
            key=f"{key_prefix}_rows",
            on_change=on_rows_change
        )

    with col_size2:
        cols = st.number_input(
            "列数",
            min_value=1,
            max_value=20,
            value=int(st.session_state[f"{key_prefix}_cols"]),
            key=f"{key_prefix}_cols",
            on_change=on_cols_change
        )

    # 统一设置区域
    with st.expander("📝 统一设置所有单元格"):
        fill_value = st.text_input(
            "输入数值",
            key=f"{key_prefix}_fill_value"
        )
        if st.button("填充", key=f"{key_prefix}_fill_btn"):
            if fill_value:
                try:
                    val = float(fill_value)
                    # 创建全为val的矩阵
                    matrix = np.full((rows, cols), val)
                    df = pd.DataFrame(matrix)
                    st.session_state[f"{key_prefix}_df"] = df
                    st.success(f"已将 {val} 填充到所有单元格")
                except ValueError:
                    st.error("请输入有效的数字")

    # 获取或创建DataFrame（根据当前尺寸）
    current_rows = st.session_state[f"{key_prefix}_rows"]
    current_cols = st.session_state[f"{key_prefix}_cols"]

    if f"{key_prefix}_df" not in st.session_state:
        df = pd.DataFrame(
            create_empty_matrix(current_rows, current_cols),
            columns=[f"列{j+1}" for j in range(current_cols)],
            index=[f"行{i+1}" for i in range(current_rows)]
        )
        st.session_state[f"{key_prefix}_df"] = df
    else:
        # 检查尺寸是否变化，如果变化则重建DataFrame
        existing_df = st.session_state[f"{key_prefix}_df"]
        if existing_df.shape != (current_rows, current_cols):
            df = pd.DataFrame(
                create_empty_matrix(current_rows, current_cols),
                columns=[f"列{j+1}" for j in range(current_cols)],
                index=[f"行{i+1}" for i in range(current_rows)]
            )
            st.session_state[f"{key_prefix}_df"] = df

    # 显示编辑框
    st.info("📌 直接编辑下方表格中的数值")
    edited_df = st.data_editor(
        st.session_state[f"{key_prefix}_df"],
        num_rows="fixed",
        width='stretch',
        hide_index=False,
        key=f"{key_prefix}_editor"
    )

    return edited_df, current_rows, current_cols


def matrix_add(matrix1, matrix2):
    """矩阵加法"""
    return matrix1 + matrix2


def matrix_subtract(matrix1, matrix2):
    """矩阵减法"""
    return matrix1 - matrix2


def matrix_multiply(matrix1, matrix2):
    """矩阵乘法"""
    return np.dot(matrix1, matrix2)


def matrix_transpose(matrix):
    """矩阵转置"""
    return matrix.T


def matrix_inverse(matrix):
    """矩阵求逆"""
    return np.linalg.inv(matrix)


def matrix_gaussian(matrix):
    """矩阵三角化（高斯消元法）"""
    result = matrix.copy().astype(float)
    rows, cols = result.shape

    for i in range(min(rows, cols)):
        # 找到主元
        if abs(result[i][i]) < 1e-10:
            # 找非零行交换
            swap_row = -1
            for k in range(i + 1, rows):
                if abs(result[k][i]) > 1e-10:
                    swap_row = k
                    break

            if swap_row == -1:
                continue

            # 交换行
            result[[i, swap_row]] = result[[swap_row, i]]

        # 消元
        for k in range(i + 1, rows):
            if abs(result[i][i]) > 1e-10:
                factor = result[k][i] / result[i][i]
                result[k] = result[k] - factor * result[i]

    return result


def main():
    """主函数"""
    st.set_page_config(
        page_title="矩阵运算系统",
        page_icon="🔢",
        layout="wide"
    )

    # 顶部：标题和运算选择
    st.title("🔢 矩阵运算系统")

    # 运算类型选择（顶部横向）
    col_left, col_center, col_right = st.columns([2, 4, 2])
    with col_center:
        operation = st.selectbox(
            "选择运算类型",
            ["矩阵加法", "矩阵减法", "矩阵乘法", "矩阵转置", "矩阵求逆", "矩阵三角化"],
            label_visibility="collapsed",
            key="operation_select"
        )

    st.markdown("---")

    # 根据运算类型显示不同的界面
    if operation == "矩阵加法":
        # 联调提示信息
        rows1_current = st.session_state.get("matrix1_rows", 2)
        cols1_current = st.session_state.get("matrix1_cols", 2)
        st.info(f"💡 加法：矩阵1({rows1_current}×{cols1_current}) 和 矩阵2({rows1_current}×{cols1_current}) 必须尺寸相同")

        # 矩阵输入区域（双列布局）
        col1, col2 = st.columns(2)

        with col1:
            df1, rows1, cols1 = matrix_input_widget(
                "matrix1",
                "🟦 矩阵1（蓝色）",
                color_theme="blue",
                default_rows=2,
                default_cols=2,
                sync_rows_key="matrix2_rows_saved",
                sync_cols_key="matrix2_cols_saved"
            )

        with col2:
            # 联调：矩阵2的尺寸与矩阵1相同，且支持双向同步
            df2, rows2, cols2 = matrix_input_widget(
                "matrix2",
                "🟩 矩阵2（绿色）",
                color_theme="green",
                default_rows=2,
                default_cols=2,
                sync_rows_key="matrix1_rows_saved",
                sync_cols_key="matrix1_cols_saved"
            )

        # 计算和清空按钮（底部）
        st.markdown("---")
        col_left_btn, col_center_btn, col_right_btn = st.columns([3, 2, 3])
        with col_center_btn:
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                calculate = st.button("🧮 计算", key="add_calculate", width='stretch')
            with btn_col2:
                clear = st.button("🗑️ 清空", key="add_clear", width='stretch')

        if calculate:
            matrix1 = parse_matrix_from_dataframe(df1)
            matrix2 = parse_matrix_from_dataframe(df2)

            if matrix1 is not None and matrix2 is not None:
                # 检查实际矩阵维度
                if matrix1.shape != matrix2.shape:
                    st.error(f"错误：矩阵维度不匹配！矩阵1为{matrix1.shape[0]}×{matrix1.shape[1]}，矩阵2为{matrix2.shape[0]}×{matrix2.shape[1]}，必须具有相同的行数和列数。")
                else:
                    result = matrix_add(matrix1, matrix2)
                    st.markdown("---")
                    display_matrix(result, f"✅ 加法结果 ({matrix1.shape[0]}×{matrix1.shape[1]})", color_theme="purple")

        if clear:
            for key in ["matrix1_df", "matrix2_df"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    elif operation == "矩阵减法":
        # 联调提示信息
        rows1_current = st.session_state.get("matrix1_sub_rows", 2)
        cols1_current = st.session_state.get("matrix1_sub_cols", 2)
        st.info(f"💡 减法：矩阵1({rows1_current}×{cols1_current}) 和 矩阵2({rows1_current}×{cols1_current}) 必须尺寸相同")

        # 矩阵输入区域（双列布局）
        col1, col2 = st.columns(2)

        with col1:
            df1, rows1, cols1 = matrix_input_widget(
                "matrix1_sub",
                "🟦 矩阵1（蓝色）",
                color_theme="blue",
                default_rows=2,
                default_cols=2,
                sync_rows_key="matrix2_sub_rows_saved",
                sync_cols_key="matrix2_sub_cols_saved"
            )

        with col2:
            # 联调：矩阵2的尺寸与矩阵1相同，且支持双向同步
            df2, rows2, cols2 = matrix_input_widget(
                "matrix2_sub",
                "🟩 矩阵2（绿色）",
                color_theme="green",
                default_rows=2,
                default_cols=2,
                sync_rows_key="matrix1_sub_rows_saved",
                sync_cols_key="matrix1_sub_cols_saved"
            )

        # 计算和清空按钮（底部）
        st.markdown("---")
        col_left_btn, col_center_btn, col_right_btn = st.columns([3, 2, 3])
        with col_center_btn:
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                calculate = st.button("🧮 计算", key="sub_calculate", width='stretch')
            with btn_col2:
                clear = st.button("🗑️ 清空", key="sub_clear", width='stretch')

        if calculate:
            matrix1 = parse_matrix_from_dataframe(df1)
            matrix2 = parse_matrix_from_dataframe(df2)

            if matrix1 is not None and matrix2 is not None:
                # 检查实际矩阵维度
                if matrix1.shape != matrix2.shape:
                    st.error(f"错误：矩阵维度不匹配！矩阵1为{matrix1.shape[0]}×{matrix1.shape[1]}，矩阵2为{matrix2.shape[0]}×{matrix2.shape[1]}，必须具有相同的行数和列数。")
                else:
                    result = matrix_subtract(matrix1, matrix2)
                    st.markdown("---")
                    display_matrix(result, f"✅ 减法结果 ({matrix1.shape[0]}×{matrix1.shape[1]})", color_theme="purple")

        if clear:
            for key in ["matrix1_sub_df", "matrix2_sub_df"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    elif operation == "矩阵乘法":
        # 联调提示信息
        rows1_current = st.session_state.get("matrix1_mul_rows", 2)
        cols1_current = st.session_state.get("matrix1_mul_cols", 2)
        cols2_current = st.session_state.get("matrix2_mul_cols", 2)
        st.info(f"💡 乘法：矩阵1({rows1_current}×{cols1_current}) × 矩阵2({cols1_current}×{cols2_current})")

        # 矩阵输入区域（双列布局）
        col1, col2 = st.columns(2)

        with col1:
            df1, rows1, cols1 = matrix_input_widget(
                "matrix1_mul",
                "🟦 矩阵1（蓝色）",
                color_theme="blue",
                default_rows=2,
                default_cols=2,
                sync_cols_key="matrix2_mul_rows_saved"
            )

        with col2:
            # 联调：矩阵2的行数等于矩阵1的列数，且支持双向同步
            df2, rows2, cols2 = matrix_input_widget(
                "matrix2_mul",
                "🟩 矩阵2（绿色）",
                color_theme="green",
                default_rows=2,
                default_cols=2,
                sync_rows_key="matrix1_mul_cols_saved",
                sync_cols_key="matrix1_mul_rows_saved"
            )

        # 计算和清空按钮（底部）
        st.markdown("---")
        col_left_btn, col_center_btn, col_right_btn = st.columns([3, 2, 3])
        with col_center_btn:
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                calculate = st.button("🧮 计算", key="mul_calculate", width='stretch')
            with btn_col2:
                clear = st.button("🗑️ 清空", key="mul_clear", width='stretch')

        if calculate:
            matrix1 = parse_matrix_from_dataframe(df1)
            matrix2 = parse_matrix_from_dataframe(df2)

            if matrix1 is not None and matrix2 is not None:
                # 检查实际矩阵维度
                if matrix1.shape[1] != matrix2.shape[0]:
                    st.error(
                        f"错误：矩阵维度不匹配！矩阵1为{matrix1.shape[0]}×{matrix1.shape[1]}，矩阵2为{matrix2.shape[0]}×{matrix2.shape[1]}。"
                        f"第一个矩阵的列数({matrix1.shape[1]})必须等于第二个矩阵的行数({matrix2.shape[0]})。"
                    )
                else:
                    result = matrix_multiply(matrix1, matrix2)
                    st.markdown("---")
                    display_matrix(result, f"✅ 乘法结果 ({matrix1.shape[0]}×{matrix2.shape[1]})", color_theme="orange")

        if clear:
            for key in ["matrix1_mul_df", "matrix2_mul_df"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    elif operation == "矩阵转置":
        st.info("💡 转置：将矩阵的行和列互换")

        st.markdown("### 🟦 输入矩阵")

        col_size1, col_size2 = st.columns(2)
        with col_size1:
            rows = st.number_input("行数", min_value=1, max_value=20, value=2, key="trans_rows")
        with col_size2:
            cols = st.number_input("列数", min_value=1, max_value=20, value=2, key="trans_cols")

        # 统一设置区域
        with st.expander("📝 统一设置所有单元格"):
            fill_value = st.text_input("输入数值", key="trans_fill_value")
            if st.button("填充", key="trans_fill_btn"):
                if fill_value:
                    try:
                        val = float(fill_value)
                        matrix = np.full((rows, cols), val)
                        df = pd.DataFrame(matrix)
                        st.session_state["trans_df"] = df
                        st.success(f"已将 {val} 填充到所有单元格")
                    except ValueError:
                        st.error("请输入有效的数字")

        # 编辑框
        if "trans_df" not in st.session_state:
            df = pd.DataFrame(
                create_empty_matrix(2, 2),
                columns=[f"列{j+1}" for j in range(2)],
                index=[f"行{i+1}" for i in range(2)]
            )
            st.session_state["trans_df"] = df

        st.info("📌 直接编辑下方表格中的数值")
        df = st.data_editor(
            st.session_state["trans_df"],
            num_rows="fixed",
            width='stretch',
            hide_index=False,
            key="trans_editor"
        )

        # 计算和清空按钮（底部）
        st.markdown("---")
        col_left_btn, col_center_btn, col_right_btn = st.columns([3, 2, 3])
        with col_center_btn:
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                calculate = st.button("🧮 计算", key="trans_calculate", width='stretch')
            with btn_col2:
                clear = st.button("🗑️ 清空", key="trans_clear", width='stretch')

        if calculate:
            matrix = parse_matrix_from_dataframe(df)
            if matrix is not None:
                result = matrix_transpose(matrix)
                st.markdown("---")
                display_matrix(result, f"✅ 转置结果 ({matrix.shape[1]}×{matrix.shape[0]})", color_theme="yellow")

        if clear:
            if "trans_df" in st.session_state:
                del st.session_state["trans_df"]
            st.rerun()

    elif operation == "矩阵求逆":
        st.info("💡 求逆：仅适用于方阵（行数=列数），且行列式不为零")

        st.markdown("### 🟦 输入方阵")

        size = st.number_input("矩阵尺寸", min_value=1, max_value=20, value=2, key="inv_size")
        rows = cols = size

        # 统一设置区域
        with st.expander("📝 统一设置所有单元格"):
            fill_value = st.text_input("输入数值", key="inv_fill_value")
            if st.button("填充", key="inv_fill_btn"):
                if fill_value:
                    try:
                        val = float(fill_value)
                        matrix = np.full((rows, cols), val)
                        df = pd.DataFrame(matrix)
                        st.session_state["inv_df"] = df
                        st.success(f"已将 {val} 填充到所有单元格")
                    except ValueError:
                        st.error("请输入有效的数字")

        # 编辑框
        if "inv_df" not in st.session_state:
            df = pd.DataFrame(
                create_empty_matrix(2, 2),
                columns=[f"列{j+1}" for j in range(2)],
                index=[f"行{i+1}" for i in range(2)]
            )
            st.session_state["inv_df"] = df

        st.info("📌 直接编辑下方表格中的数值")
        df = st.data_editor(
            st.session_state["inv_df"],
            num_rows="fixed",
            width='stretch',
            hide_index=False,
            key="inv_editor"
        )

        # 计算和清空按钮（底部）
        st.markdown("---")
        col_left_btn, col_center_btn, col_right_btn = st.columns([3, 2, 3])
        with col_center_btn:
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                calculate = st.button("🧮 计算", key="inv_calculate", width='stretch')
            with btn_col2:
                clear = st.button("🗑️ 清空", key="inv_clear", width='stretch')

        if calculate:
            matrix = parse_matrix_from_dataframe(df)
            if matrix is not None:
                if matrix.shape[0] != matrix.shape[1]:
                    st.error(f"错误：只能对方阵求逆！当前矩阵为{matrix.shape[0]}×{matrix.shape[1]}。")
                else:
                    try:
                        result = matrix_inverse(matrix)
                        st.markdown("---")
                        display_matrix(result, f"✅ 逆矩阵 ({matrix.shape[0]}×{matrix.shape[0]})", color_theme="pink")
                    except np.linalg.LinAlgError:
                        st.error("错误：矩阵不可逆（行列式为零）！")

        if clear:
            if "inv_df" in st.session_state:
                del st.session_state["inv_df"]
            st.rerun()

    elif operation == "矩阵三角化":
        st.info("💡 三角化：将矩阵转换为上三角形式")

        st.markdown("### 🟦 输入矩阵")

        col_size1, col_size2 = st.columns(2)
        with col_size1:
            rows = st.number_input("行数", min_value=1, max_value=20, value=3, key="gauss_rows")
        with col_size2:
            cols = st.number_input("列数", min_value=1, max_value=20, value=3, key="gauss_cols")

        # 统一设置区域
        with st.expander("📝 统一设置所有单元格"):
            fill_value = st.text_input("输入数值", key="gauss_fill_value")
            if st.button("填充", key="gauss_fill_btn"):
                if fill_value:
                    try:
                        val = float(fill_value)
                        matrix = np.full((rows, cols), val)
                        df = pd.DataFrame(matrix)
                        st.session_state["gauss_df"] = df
                        st.success(f"已将 {val} 填充到所有单元格")
                    except ValueError:
                        st.error("请输入有效的数字")

        # 编辑框
        if "gauss_df" not in st.session_state:
            df = pd.DataFrame(
                create_empty_matrix(3, 3),
                columns=[f"列{j+1}" for j in range(3)],
                index=[f"行{i+1}" for i in range(3)]
            )
            st.session_state["gauss_df"] = df

        st.info("📌 直接编辑下方表格中的数值")
        df = st.data_editor(
            st.session_state["gauss_df"],
            num_rows="fixed",
            width='stretch',
            hide_index=False,
            key="gauss_editor"
        )

        # 计算和清空按钮（底部）
        st.markdown("---")
        col_left_btn, col_center_btn, col_right_btn = st.columns([3, 2, 3])
        with col_center_btn:
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                calculate = st.button("🧮 计算", key="gauss_calculate", width='stretch')
            with btn_col2:
                clear = st.button("🗑️ 清空", key="gauss_clear", width='stretch')

        if calculate:
            matrix = parse_matrix_from_dataframe(df)
            if matrix is not None:
                result = matrix_gaussian(matrix)
                st.markdown("---")
                display_matrix(result, f"✅ 三角化结果 ({matrix.shape[0]}×{matrix.shape[1]})", color_theme="cyan")

        if clear:
            if "gauss_df" in st.session_state:
                del st.session_state["gauss_df"]
            st.rerun()

    # 页脚
    st.markdown("---")
    st.caption("矩阵运算系统 - Streamlit网页版 | 支持矩阵加、减、乘、转置、求逆、三角化")


if __name__ == "__main__":
    main()
