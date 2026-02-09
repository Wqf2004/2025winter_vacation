"""
矩阵运算系统 - 主窗口
"""
import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QMessageBox,
    QGroupBox, QLineEdit, QGridLayout, QComboBox, QSpinBox, QDoubleSpinBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QBrush


class MatrixInputWidget(QWidget):
    """矩阵输入控件"""

    def __init__(self, title, max_size=20, color_theme="blue"):
        super().__init__()
        self.max_size = max_size
        self.title = title
        self.color_theme = color_theme
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 标题和尺寸控制
        header_layout = QHBoxLayout()
        self.title_label = QLabel(f"{self.title}")
        self.title_label.setFont(QFont("Arial", 12, QFont.Bold))

        # 设置标题颜色
        if self.color_theme == "blue":
            self.title_label.setStyleSheet("color: #0066cc;")
        elif self.color_theme == "green":
            self.title_label.setStyleSheet("color: #009933;")
        elif self.color_theme == "purple":
            self.title_label.setStyleSheet("color: #9933cc;")

        header_layout.addWidget(self.title_label)

        header_layout.addWidget(QLabel("行数:"))
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(1, self.max_size)
        self.rows_spin.setValue(2)
        self.rows_spin.valueChanged.connect(self.update_table_size)
        header_layout.addWidget(self.rows_spin)

        header_layout.addWidget(QLabel("列数:"))
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(1, self.max_size)
        self.cols_spin.setValue(2)
        self.cols_spin.valueChanged.connect(self.update_table_size)
        header_layout.addWidget(self.cols_spin)

        header_layout.addStretch()
        layout.addLayout(header_layout)

        # 统一输入行
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("统一设置所有单元格:"))
        self.fill_edit = QLineEdit()
        self.fill_edit.setPlaceholderText("输入数值...")
        self.fill_edit.setMaximumWidth(150)
        input_layout.addWidget(self.fill_edit)

        self.fill_btn = QPushButton("填充选中")
        self.fill_btn.setMaximumWidth(80)
        self.fill_btn.setToolTip("填充选中的单元格（Ctrl+点击多选，未选则填充全部）")
        self.fill_btn.clicked.connect(self.fill_selected_cells)
        input_layout.addWidget(self.fill_btn)

        self.clear_btn = QPushButton("清空")
        self.clear_btn.setMaximumWidth(60)
        self.clear_btn.clicked.connect(self.clear_all_cells)
        input_layout.addWidget(self.clear_btn)

        input_layout.addStretch()
        layout.addLayout(input_layout)

        # 矩阵表格
        self.table = QTableWidget()
        self.table.setRowCount(2)
        self.table.setColumnCount(2)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)

        # 启用多选（Ctrl+点击）
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)
        self.table.setSelectionBehavior(QTableWidget.SelectItems)

        # 设置表格样式
        self.apply_table_style()

        layout.addWidget(self.table)
        self.setLayout(layout)

        # 初始化表格
        self.update_table_size()

    def apply_table_style(self):
        """应用表格颜色样式"""
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                item = self.table.item(i, j)
                if item:
                    if self.color_theme == "blue":
                        item.setBackground(QColor(230, 240, 255))
                    elif self.color_theme == "green":
                        item.setBackground(QColor(230, 255, 230))
                    elif self.color_theme == "purple":
                        item.setBackground(QColor(245, 230, 255))

    def update_table_size(self):
        """更新表格大小"""
        rows = self.rows_spin.value()
        cols = self.cols_spin.value()
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols)

        # 调整单元格大小
        for i in range(rows):
            for j in range(cols):
                if self.table.item(i, j) is None:
                    item = QTableWidgetItem("0")
                    item.setTextAlignment(Qt.AlignCenter)
                    # 设置背景颜色
                    if self.color_theme == "blue":
                        item.setBackground(QColor(230, 240, 255))
                    elif self.color_theme == "green":
                        item.setBackground(QColor(230, 255, 230))
                    elif self.color_theme == "purple":
                        item.setBackground(QColor(245, 230, 255))
                    self.table.setItem(i, j, item)

        # 调整列宽
        for j in range(cols):
            self.table.setColumnWidth(j, 80)

    def get_matrix(self):
        """获取矩阵数据"""
        rows = self.rows_spin.value()
        cols = self.cols_spin.value()
        matrix = np.zeros((rows, cols))

        for i in range(rows):
            for j in range(cols):
                item = self.table.item(i, j)
                if item:
                    try:
                        matrix[i][j] = float(item.text())
                    except ValueError:
                        matrix[i][j] = 0.0

        return matrix

    def set_matrix(self, matrix):
        """设置矩阵数据"""
        rows, cols = matrix.shape
        self.rows_spin.setValue(rows)
        self.cols_spin.setValue(cols)

        for i in range(rows):
            for j in range(cols):
                item = self.table.item(i, j)
                if item:
                    item.setText(f"{matrix[i][j]:.4g}")

    def fill_selected_cells(self):
        """将统一值填充到选中的单元格"""
        value_text = self.fill_edit.text().strip()

        if not value_text:
            return

        try:
            value = float(value_text)
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的数字！")
            return

        selected_items = self.table.selectedItems()

        if selected_items:
            # 填充选中的单元格
            for item in selected_items:
                item.setText(f"{value:.6g}")
        else:
            # 没有选中则填充全部单元格
            rows = self.rows_spin.value()
            cols = self.cols_spin.value()

            for i in range(rows):
                for j in range(cols):
                    item = self.table.item(i, j)
                    if item:
                        item.setText(f"{value:.6g}")

    def clear_all_cells(self):
        """清空所有单元格为0"""
        rows = self.rows_spin.value()
        cols = self.cols_spin.value()

        for i in range(rows):
            for j in range(cols):
                item = self.table.item(i, j)
                if item:
                    item.setText("0")

        # 清空输入框
        self.fill_edit.clear()


class MatrixResultWidget(QWidget):
    """矩阵结果显示控件"""

    def __init__(self, title, max_size=20):
        super().__init__()
        self.max_size = max_size
        self.title = title
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 标题
        self.title_label = QLabel(f"{self.title}")
        self.title_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.title_label.setStyleSheet("color: #cc6600;")
        layout.addWidget(self.title_label)

        # 结果表格
        self.table = QTableWidget()
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("矩阵运算系统 - PyQt5版")
        self.setGeometry(100, 100, 1200, 800)

        # 主控件
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # 操作选择
        operation_group = QGroupBox("选择运算类型")
        operation_layout = QHBoxLayout()

        self.operation_combo = QComboBox()
        self.operation_combo.addItems([
            "矩阵加法",
            "矩阵减法",
            "矩阵乘法",
            "矩阵转置",
            "矩阵求逆",
            "矩阵三角化"
        ])
        self.operation_combo.currentIndexChanged.connect(self.on_operation_changed)
        operation_layout.addWidget(self.operation_combo)

        self.calculate_btn = QPushButton("计算")
        self.calculate_btn.setFont(QFont("Arial", 12))
        self.calculate_btn.setMinimumHeight(40)
        self.calculate_btn.clicked.connect(self.calculate)
        operation_layout.addWidget(self.calculate_btn)

        self.clear_btn = QPushButton("清空")
        self.clear_btn.setMinimumHeight(40)
        self.clear_btn.clicked.connect(self.clear_all)
        operation_layout.addWidget(self.clear_btn)

        operation_layout.addStretch()
        operation_group.setLayout(operation_layout)
        main_layout.addWidget(operation_group)

        # 矩阵输入区域
        self.matrix_group = QGroupBox("矩阵输入")
        matrix_layout = QGridLayout()

        # 第一个矩阵 - 蓝色主题
        self.matrix1_widget = MatrixInputWidget("矩阵1（蓝色）", max_size=20, color_theme="blue")
        matrix_layout.addWidget(self.matrix1_widget, 0, 0)

        # 第二个矩阵 - 绿色主题
        self.matrix2_widget = MatrixInputWidget("矩阵2（绿色）", max_size=20, color_theme="green")
        matrix_layout.addWidget(self.matrix2_widget, 0, 1)

        # 连接尺寸变化信号，实现双向实时联调
        self.matrix1_widget.rows_spin.valueChanged.connect(self.on_matrix1_size_changed)
        self.matrix1_widget.cols_spin.valueChanged.connect(self.on_matrix1_size_changed)

        self.matrix2_widget.rows_spin.valueChanged.connect(self.on_matrix2_size_changed)
        self.matrix2_widget.cols_spin.valueChanged.connect(self.on_matrix2_size_changed)

        self.matrix_group.setLayout(matrix_layout)
        main_layout.addWidget(self.matrix_group)

        # 结果区域
        result_group = QGroupBox("运算结果")
        result_layout = QVBoxLayout()

        self.result_label = QLabel("请选择运算类型并输入矩阵，然后点击'计算'按钮")
        self.result_label.setFont(QFont("Arial", 12))
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("color: gray; padding: 20px;")
        result_layout.addWidget(self.result_label)

        self.result_table = QTableWidget()
        self.result_table.horizontalHeader().setVisible(False)
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setVisible(False)
        result_layout.addWidget(self.result_table)

        result_group.setLayout(result_layout)
        main_layout.addWidget(result_group)

        # 说明标签
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("color: blue; padding: 10px;")
        main_layout.addWidget(self.info_label)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 初始化界面
        self.on_operation_changed()

    def on_matrix1_size_changed(self):
        """矩阵1尺寸变化时的联调处理"""
        operation = self.operation_combo.currentText()

        if operation == "矩阵加法" or operation == "矩阵减法":
            # 加减法：矩阵2的行数和列数都与矩阵1相同
            rows1 = self.matrix1_widget.rows_spin.value()
            cols1 = self.matrix1_widget.cols_spin.value()
            # 阻止信号以避免循环触发
            self.matrix2_widget.rows_spin.blockSignals(True)
            self.matrix2_widget.cols_spin.blockSignals(True)
            self.matrix2_widget.rows_spin.setValue(rows1)
            self.matrix2_widget.cols_spin.setValue(cols1)
            self.matrix2_widget.rows_spin.blockSignals(False)
            self.matrix2_widget.cols_spin.blockSignals(False)
            # 刷新矩阵2的表格
            self.matrix2_widget.update_table_size()
        elif operation == "矩阵乘法":
            # 乘法：矩阵2的行数等于矩阵1的列数
            cols1 = self.matrix1_widget.cols_spin.value()
            self.matrix2_widget.rows_spin.blockSignals(True)
            self.matrix2_widget.rows_spin.setValue(cols1)
            self.matrix2_widget.rows_spin.blockSignals(False)
            # 刷新矩阵2的表格
            self.matrix2_widget.update_table_size()

        # 刷新矩阵1的表格（因为可能是行数或列数改变）
        self.matrix1_widget.update_table_size()

        # 更新提示信息，反映当前联调关系
        self.update_sync_info()

    def on_matrix2_size_changed(self):
        """矩阵2尺寸变化时的联调处理"""
        operation = self.operation_combo.currentText()

        if operation == "矩阵加法" or operation == "矩阵减法":
            # 加减法：矩阵1的行数和列数都与矩阵2相同
            rows2 = self.matrix2_widget.rows_spin.value()
            cols2 = self.matrix2_widget.cols_spin.value()
            # 阻止信号以避免循环触发
            self.matrix1_widget.rows_spin.blockSignals(True)
            self.matrix1_widget.cols_spin.blockSignals(True)
            self.matrix1_widget.rows_spin.setValue(rows2)
            self.matrix1_widget.cols_spin.setValue(cols2)
            self.matrix1_widget.rows_spin.blockSignals(False)
            self.matrix1_widget.cols_spin.blockSignals(False)
            # 刷新矩阵1的表格
            self.matrix1_widget.update_table_size()
        elif operation == "矩阵乘法":
            # 乘法：矩阵1的列数等于矩阵2的行数
            rows2 = self.matrix2_widget.rows_spin.value()
            self.matrix1_widget.cols_spin.blockSignals(True)
            self.matrix1_widget.cols_spin.setValue(rows2)
            self.matrix1_widget.cols_spin.blockSignals(False)
            # 刷新矩阵1的表格
            self.matrix1_widget.update_table_size()

        # 刷新矩阵2的表格（因为可能是行数或列数改变）
        self.matrix2_widget.update_table_size()

        # 更新提示信息，反映当前联调关系
        self.update_sync_info()

    def update_sync_info(self):
        """更新联调提示信息"""
        operation = self.operation_combo.currentText()

        if operation == "矩阵加法":
            rows1 = self.matrix1_widget.rows_spin.value()
            cols1 = self.matrix1_widget.cols_spin.value()
            self.info_label.setText(f"加法：矩阵1({rows1}×{cols1}) 和 矩阵2({rows1}×{cols1}) 必须尺寸相同")
        elif operation == "矩阵减法":
            rows1 = self.matrix1_widget.rows_spin.value()
            cols1 = self.matrix1_widget.cols_spin.value()
            self.info_label.setText(f"减法：矩阵1({rows1}×{cols1}) 和 矩阵2({rows1}×{cols1}) 必须尺寸相同")
        elif operation == "矩阵乘法":
            rows1 = self.matrix1_widget.rows_spin.value()
            cols1 = self.matrix1_widget.cols_spin.value()
            cols2 = self.matrix2_widget.cols_spin.value()
            self.info_label.setText(f"乘法：矩阵1({rows1}×{cols1}) × 矩阵2({cols1}×{cols2})")

    def on_operation_changed(self):
        """运算类型改变时更新界面"""
        operation = self.operation_combo.currentText()

        if operation == "矩阵转置":
            self.matrix2_widget.setVisible(False)
            self.info_label.setText("转置：将矩阵的行和列互换")
        elif operation == "矩阵求逆":
            self.matrix2_widget.setVisible(False)
            self.info_label.setText("求逆：仅适用于方阵（行数=列数），且行列式不为零")
        elif operation == "矩阵三角化":
            self.matrix2_widget.setVisible(False)
            self.info_label.setText("三角化：将矩阵转换为上三角形式")
        elif operation == "矩阵加法":
            self.matrix2_widget.setVisible(True)
            # 联调：设置第二个矩阵尺寸与第一个矩阵相同
            rows1 = self.matrix1_widget.rows_spin.value()
            cols1 = self.matrix1_widget.cols_spin.value()
            self.matrix2_widget.rows_spin.blockSignals(True)
            self.matrix2_widget.cols_spin.blockSignals(True)
            self.matrix2_widget.rows_spin.setValue(rows1)
            self.matrix2_widget.cols_spin.setValue(cols1)
            self.matrix2_widget.rows_spin.blockSignals(False)
            self.matrix2_widget.cols_spin.blockSignals(False)
            # 刷新矩阵2的表格
            self.matrix2_widget.update_table_size()
            self.update_sync_info()
        elif operation == "矩阵减法":
            self.matrix2_widget.setVisible(True)
            # 联调：设置第二个矩阵尺寸与第一个矩阵相同
            rows1 = self.matrix1_widget.rows_spin.value()
            cols1 = self.matrix1_widget.cols_spin.value()
            self.matrix2_widget.rows_spin.blockSignals(True)
            self.matrix2_widget.cols_spin.blockSignals(True)
            self.matrix2_widget.rows_spin.setValue(rows1)
            self.matrix2_widget.cols_spin.setValue(cols1)
            self.matrix2_widget.rows_spin.blockSignals(False)
            self.matrix2_widget.cols_spin.blockSignals(False)
            # 刷新矩阵2的表格
            self.matrix2_widget.update_table_size()
            self.update_sync_info()
        elif operation == "矩阵乘法":
            self.matrix2_widget.setVisible(True)
            # 联调：设置第二个矩阵的行数等于第一个矩阵的列数
            cols1 = self.matrix1_widget.cols_spin.value()
            self.matrix2_widget.rows_spin.blockSignals(True)
            self.matrix2_widget.rows_spin.setValue(cols1)
            self.matrix2_widget.rows_spin.blockSignals(False)
            # 刷新矩阵2的表格
            self.matrix2_widget.update_table_size()
            self.update_sync_info()

        # 清空结果
        self.result_label.setVisible(True)
        self.result_label.setText("请选择运算类型并输入矩阵，然后点击'计算'按钮")
        self.result_table.setVisible(False)

    def calculate(self):
        """执行矩阵运算"""
        try:
            operation = self.operation_combo.currentText()
            matrix1 = self.matrix1_widget.get_matrix()
            rows1, cols1 = matrix1.shape

            if operation == "矩阵加法":
                matrix2 = self.matrix2_widget.get_matrix()
                rows2, cols2 = matrix2.shape

                if rows1 != rows2 or cols1 != cols2:
                    QMessageBox.warning(self, "错误", "矩阵维度不匹配！两个矩阵必须具有相同的行数和列数。")
                    return

                result = matrix1 + matrix2
                self.display_result(result, f"矩阵加法结果 ({rows1}×{cols1})")

            elif operation == "矩阵减法":
                matrix2 = self.matrix2_widget.get_matrix()
                rows2, cols2 = matrix2.shape

                if rows1 != rows2 or cols1 != cols2:
                    QMessageBox.warning(self, "错误", "矩阵维度不匹配！两个矩阵必须具有相同的行数和列数。")
                    return

                result = matrix1 - matrix2
                self.display_result(result, f"矩阵减法结果 ({rows1}×{cols1})")

            elif operation == "矩阵乘法":
                matrix2 = self.matrix2_widget.get_matrix()
                rows2, cols2 = matrix2.shape

                if cols1 != rows2:
                    QMessageBox.warning(self, "错误",
                                       f"矩阵维度不匹配！第一个矩阵的列数({cols1})必须等于第二个矩阵的行数({rows2})。")
                    return

                result = np.dot(matrix1, matrix2)
                self.display_result(result, f"矩阵乘法结果 ({rows1}×{cols2})")

            elif operation == "矩阵转置":
                result = matrix1.T
                self.display_result(result, f"矩阵转置结果 ({cols1}×{rows1})")

            elif operation == "矩阵求逆":
                if rows1 != cols1:
                    QMessageBox.warning(self, "错误", "只能对方阵求逆（行数必须等于列数）！")
                    return

                try:
                    result = np.linalg.inv(matrix1)
                    self.display_result(result, f"矩阵逆矩阵 ({rows1}×{cols1})")
                except np.linalg.LinAlgError:
                    QMessageBox.warning(self, "错误", "矩阵不可逆（行列式为零）！")
                    return

            elif operation == "矩阵三角化":
                # 使用高斯消元法将矩阵转换为上三角形式
                result = matrix1.copy().astype(float)
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

                self.display_result(result, f"矩阵三角化结果 ({rows}×{cols})")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"计算时发生错误：{str(e)}")

    def display_result(self, matrix, title):
        """显示结果矩阵"""
        rows, cols = matrix.shape

        self.result_label.setVisible(False)
        self.result_table.setVisible(True)

        self.result_table.setRowCount(rows)
        self.result_table.setColumnCount(cols)

        # 根据运算类型设置结果矩阵的配色
        operation = self.operation_combo.currentText()
        if operation == "矩阵加法":
            # 加法结果：紫色（蓝色+绿色混合）
            bg_color = QColor(235, 235, 255)
        elif operation == "矩阵减法":
            # 减法结果：浅紫色
            bg_color = QColor(245, 235, 255)
        elif operation == "矩阵乘法":
            # 乘法结果：橙黄色
            bg_color = QColor(255, 250, 220)
        elif operation == "矩阵转置":
            # 转置结果：浅黄色
            bg_color = QColor(255, 255, 230)
        elif operation == "矩阵求逆":
            # 求逆结果：浅粉色
            bg_color = QColor(255, 230, 230)
        elif operation == "矩阵三角化":
            # 三角化结果：浅青色
            bg_color = QColor(230, 250, 250)
        else:
            bg_color = QColor(240, 240, 240)

        for i in range(rows):
            for j in range(cols):
                item = QTableWidgetItem(f"{matrix[i][j]:.6g}")
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(bg_color)
                self.result_table.setItem(i, j, item)

        # 调整列宽
        for j in range(cols):
            self.result_table.setColumnWidth(j, 100)

        # 更新联调信息
        self.update_sync_info()
        self.info_label.setText(f"{title} - 运算成功完成！")

    def clear_all(self):
        """清空所有输入和结果"""
        # 重置第一个矩阵
        self.matrix1_widget.rows_spin.setValue(2)
        self.matrix1_widget.cols_spin.setValue(2)
        rows1, cols1 = self.matrix1_widget.rows_spin.value(), self.matrix1_widget.cols_spin.value()
        for i in range(rows1):
            for j in range(cols1):
                item = self.matrix1_widget.table.item(i, j)
                if item:
                    item.setText("0")

        # 重置第二个矩阵
        self.matrix2_widget.rows_spin.setValue(2)
        self.matrix2_widget.cols_spin.setValue(2)
        rows2, cols2 = self.matrix2_widget.rows_spin.value(), self.matrix2_widget.cols_spin.value()
        for i in range(rows2):
            for j in range(cols2):
                item = self.matrix2_widget.table.item(i, j)
                if item:
                    item.setText("0")

        # 清空结果
        self.result_label.setVisible(True)
        self.result_label.setText("请选择运算类型并输入矩阵，然后点击'计算'按钮")
        self.result_table.setVisible(False)

        self.on_operation_changed()

        # 清空后更新联调信息
        self.update_sync_info()
        self.info_label.setText("所有数据已清空")
