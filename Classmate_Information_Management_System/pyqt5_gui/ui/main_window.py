"""
主窗口
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QMessageBox, QComboBox,
                             QDialog, QDialogButtonBox, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self, data_manager, password):
        super().__init__()
        self.data_manager = data_manager
        self.password = password
        self.current_students = []
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('班级同学信息管理系统')
        self.setMinimumSize(1000, 700)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)

        # 标题
        title_label = QLabel('班级同学信息管理系统')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        title_label.setStyleSheet('padding: 20px; color: #333;')
        main_layout.addWidget(title_label)

        # 功能按钮区域
        button_layout = QHBoxLayout()

        add_btn = QPushButton('添加同学')
        add_btn.setStyleSheet('background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;')
        add_btn.clicked.connect(self.add_student)
        button_layout.addWidget(add_btn)

        delete_btn = QPushButton('删除同学')
        delete_btn.setStyleSheet('background-color: #f44336; color: white; padding: 10px; border-radius: 5px;')
        delete_btn.clicked.connect(self.delete_student)
        button_layout.addWidget(delete_btn)

        modify_btn = QPushButton('修改同学')
        modify_btn.setStyleSheet('background-color: #FF9800; color: white; padding: 10px; border-radius: 5px;')
        modify_btn.clicked.connect(self.modify_student)
        button_layout.addWidget(modify_btn)

        refresh_btn = QPushButton('刷新列表')
        refresh_btn.setStyleSheet('background-color: #2196F3; color: white; padding: 10px; border-radius: 5px;')
        refresh_btn.clicked.connect(self.refresh_table)
        button_layout.addWidget(refresh_btn)

        search_input = QLineEdit()
        search_input.setPlaceholderText('搜索同学...')
        search_input.setStyleSheet('padding: 10px; border-radius: 5px;')
        search_input.textChanged.connect(self.on_search_changed)
        button_layout.addWidget(search_input)

        save_btn = QPushButton('保存数据')
        save_btn.setStyleSheet('background-color: #9C27B0; color: white; padding: 10px; border-radius: 5px;')
        save_btn.clicked.connect(self.save_data)
        button_layout.addWidget(save_btn)

        change_pwd_btn = QPushButton('修改密码')
        change_pwd_btn.setStyleSheet('background-color: #607D8B; color: white; padding: 10px; border-radius: 5px;')
        change_pwd_btn.clicked.connect(self.change_password)
        button_layout.addWidget(change_pwd_btn)

        main_layout.addLayout(button_layout)

        # 同学表格
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(6)
        self.student_table.setHorizontalHeaderLabels(['ID', '姓名', '学号', '宿舍', 'QQ', '电话'])
        self.student_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.student_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.student_table.setStyleSheet('''
            QTableWidget {
                gridline-color: #ddd;
                border: 1px solid #ddd;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 10px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
        ''')
        main_layout.addWidget(self.student_table)

        # 状态栏
        self.status_label = QLabel('就绪')
        self.status_label.setStyleSheet('padding: 10px; color: #666;')
        main_layout.addWidget(self.status_label)

        # 加载数据
        self.refresh_table()

    def refresh_table(self):
        """刷新表格"""
        self.current_students = self.data_manager.get_students()
        self.update_table()

    def update_table(self):
        """更新表格"""
        self.student_table.setRowCount(len(self.current_students))

        for row, student in enumerate(self.current_students):
            self.student_table.setItem(row, 0, QTableWidgetItem(str(student.id)))
            self.student_table.setItem(row, 1, QTableWidgetItem(student.name))
            self.student_table.setItem(row, 2, QTableWidgetItem(student.student_number))
            self.student_table.setItem(row, 3, QTableWidgetItem(student.dorm))
            self.student_table.setItem(row, 4, QTableWidgetItem(student.qq))
            self.student_table.setItem(row, 5, QTableWidgetItem(student.phone))

        self.status_label.setText(f'共 {len(self.current_students)} 位同学')

    def add_student(self):
        """添加同学"""
        dialog = StudentDialog(self)
        if dialog.exec() == QDialog.Accepted:
            student = dialog.get_student()

            # 验证数据
            if not student.student_number:
                QMessageBox.warning(self, '错误', '学号不能为空！')
                return

            if not student.name:
                QMessageBox.warning(self, '错误', '姓名不能为空！')
                return

            # 添加同学
            success, message = self.data_manager.add_student(student)
            if success:
                self.refresh_table()
                QMessageBox.information(self, '成功', message)
            else:
                QMessageBox.warning(self, '错误', message)

    def delete_student(self):
        """删除同学"""
        selected_row = self.student_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, '警告', '请先选择要删除的同学！')
            return

        student = self.current_students[selected_row]

        reply = QMessageBox.question(
            self, '确认删除',
            f'确定要删除同学 "{student.name}" 吗？',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success, message = self.data_manager.delete_student(student.id)
            if success:
                self.refresh_table()
                QMessageBox.information(self, '成功', message)
            else:
                QMessageBox.warning(self, '错误', message)

    def modify_student(self):
        """修改同学"""
        selected_row = self.student_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, '警告', '请先选择要修改的同学！')
            return

        student = self.current_students[selected_row]

        dialog = StudentDialog(self, student)
        if dialog.exec() == QDialog.Accepted:
            new_student = dialog.get_student()

            # 验证数据
            if not new_student.student_number:
                QMessageBox.warning(self, '错误', '学号不能为空！')
                return

            if not new_student.name:
                QMessageBox.warning(self, '错误', '姓名不能为空！')
                return

            # 更新同学
            success, message = self.data_manager.update_student(new_student)
            if success:
                self.refresh_table()
                QMessageBox.information(self, '成功', message)
            else:
                QMessageBox.warning(self, '错误', message)

    def on_search_changed(self, text):
        """搜索改变"""
        if not text:
            self.current_students = self.data_manager.get_students()
        else:
            self.current_students = self.data_manager.search_students(text)
        self.update_table()

    def save_data(self):
        """保存数据"""
        if self.data_manager.save_data():
            QMessageBox.information(self, '成功', '数据保存成功！')
        else:
            QMessageBox.warning(self, '错误', '数据保存失败！')

    def change_password(self):
        """修改密码"""
        dialog = PasswordDialog(self)
        if dialog.exec() == QDialog.Accepted:
            old_pwd, new_pwd = dialog.get_passwords()
            if self.data_manager.change_password(old_pwd, new_pwd):
                QMessageBox.information(self, '成功', '密码修改成功！')
            else:
                QMessageBox.warning(self, '错误', '旧密码错误！')


class StudentDialog(QDialog):
    """同学对话框"""

    def __init__(self, parent, student=None):
        super().__init__(parent)
        self.student = student
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('同学信息')
        self.setFixedSize(500, 350)

        layout = QVBoxLayout()

        # 姓名
        layout.addWidget(QLabel('姓名 *：'))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('请输入姓名')
        layout.addWidget(self.name_input)

        # 学号
        layout.addWidget(QLabel('学号 *：'))
        self.student_number_input = QLineEdit()
        self.student_number_input.setPlaceholderText('请输入学号')
        layout.addWidget(self.student_number_input)

        # 宿舍
        layout.addWidget(QLabel('宿舍：'))
        self.dorm_input = QLineEdit()
        self.dorm_input.setPlaceholderText('请输入宿舍号')
        layout.addWidget(self.dorm_input)

        # QQ
        layout.addWidget(QLabel('QQ：'))
        self.qq_input = QLineEdit()
        self.qq_input.setPlaceholderText('请输入QQ号')
        layout.addWidget(self.qq_input)

        # 电话
        layout.addWidget(QLabel('电话：'))
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText('请输入电话号码')
        layout.addWidget(self.phone_input)

        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

        # 如果是编辑模式，填充数据
        if self.student:
            self.name_input.setText(self.student.name)
            self.student_number_input.setText(self.student.student_number)
            self.dorm_input.setText(self.student.dorm)
            self.qq_input.setText(self.student.qq)
            self.phone_input.setText(self.student.phone)

    def get_student(self):
        """获取同学"""
        from ..data_manager import Student
        student_id = self.student.id if self.student else 0
        return Student(
            student_id,
            self.name_input.text().strip(),
            self.student_number_input.text().strip(),
            self.dorm_input.text().strip(),
            self.qq_input.text().strip(),
            self.phone_input.text().strip()
        )


class PasswordDialog(QDialog):
    """密码对话框"""

    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('修改密码')
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        # 旧密码
        layout.addWidget(QLabel('旧密码：'))
        self.old_pwd_input = QLineEdit()
        self.old_pwd_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.old_pwd_input)

        # 新密码
        layout.addWidget(QLabel('新密码：'))
        self.new_pwd_input = QLineEdit()
        self.new_pwd_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.new_pwd_input)

        # 确认密码
        layout.addWidget(QLabel('确认密码：'))
        self.confirm_pwd_input = QLineEdit()
        self.confirm_pwd_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_pwd_input)

        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_passwords(self):
        """获取密码"""
        return (
            self.old_pwd_input.text(),
            self.new_pwd_input.text()
        )

    def accept(self):
        """接受"""
        old_pwd = self.old_pwd_input.text()
        new_pwd = self.new_pwd_input.text()
        confirm_pwd = self.confirm_pwd_input.text()

        if not old_pwd or not new_pwd or not confirm_pwd:
            QMessageBox.warning(self, '错误', '请填写所有字段！')
            return

        if new_pwd != confirm_pwd:
            QMessageBox.warning(self, '错误', '两次输入的新密码不一致！')
            return

        super().accept()
