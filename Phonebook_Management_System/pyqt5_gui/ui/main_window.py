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
        self.current_contacts = []
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('电话簿管理系统')
        self.setMinimumSize(1000, 700)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)

        # 标题
        title_label = QLabel('电话簿管理系统')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        title_label.setStyleSheet('padding: 20px; color: #333;')
        main_layout.addWidget(title_label)

        # 功能按钮区域
        button_layout = QHBoxLayout()

        add_btn = QPushButton('添加联系人')
        add_btn.setStyleSheet('background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;')
        add_btn.clicked.connect(self.add_contact)
        button_layout.addWidget(add_btn)

        delete_btn = QPushButton('删除联系人')
        delete_btn.setStyleSheet('background-color: #f44336; color: white; padding: 10px; border-radius: 5px;')
        delete_btn.clicked.connect(self.delete_contact)
        button_layout.addWidget(delete_btn)

        modify_btn = QPushButton('修改联系人')
        modify_btn.setStyleSheet('background-color: #FF9800; color: white; padding: 10px; border-radius: 5px;')
        modify_btn.clicked.connect(self.modify_contact)
        button_layout.addWidget(modify_btn)

        sort_combo = QComboBox()
        sort_combo.addItems(['按姓名排序', '按电话号码排序'])
        sort_combo.setStyleSheet('padding: 10px; border-radius: 5px;')
        sort_combo.currentIndexChanged.connect(self.on_sort_changed)
        button_layout.addWidget(sort_combo)

        refresh_btn = QPushButton('刷新列表')
        refresh_btn.setStyleSheet('background-color: #2196F3; color: white; padding: 10px; border-radius: 5px;')
        refresh_btn.clicked.connect(self.refresh_table)
        button_layout.addWidget(refresh_btn)

        search_input = QLineEdit()
        search_input.setPlaceholderText('搜索联系人...')
        search_input.setStyleSheet('padding: 10px; border-radius: 5px;')
        search_input.textChanged.connect(self.on_search_changed)
        button_layout.addWidget(search_input)

        search_combo = QComboBox()
        search_combo.addItems(['按姓名搜索', '按电话搜索'])
        search_combo.setStyleSheet('padding: 10px; border-radius: 5px;')
        self.search_combo = search_combo
        button_layout.addWidget(search_combo)

        save_btn = QPushButton('保存数据')
        save_btn.setStyleSheet('background-color: #9C27B0; color: white; padding: 10px; border-radius: 5px;')
        save_btn.clicked.connect(self.save_data)
        button_layout.addWidget(save_btn)

        change_pwd_btn = QPushButton('修改密码')
        change_pwd_btn.setStyleSheet('background-color: #607D8B; color: white; padding: 10px; border-radius: 5px;')
        change_pwd_btn.clicked.connect(self.change_password)
        button_layout.addWidget(change_pwd_btn)

        main_layout.addLayout(button_layout)

        # 联系人表格
        self.contact_table = QTableWidget()
        self.contact_table.setColumnCount(5)
        self.contact_table.setHorizontalHeaderLabels(['ID', '姓名', '工作单位', '电话号码', 'E-mail地址'])
        self.contact_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.contact_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.contact_table.setStyleSheet('''
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
        main_layout.addWidget(self.contact_table)

        # 状态栏
        self.status_label = QLabel('就绪')
        self.status_label.setStyleSheet('padding: 10px; color: #666;')
        main_layout.addWidget(self.status_label)

        # 加载数据
        self.refresh_table()

    def refresh_table(self):
        """刷新表格"""
        self.current_contacts = self.data_manager.get_contacts()
        self.update_table()

    def update_table(self):
        """更新表格"""
        self.contact_table.setRowCount(len(self.current_contacts))

        for row, contact in enumerate(self.current_contacts):
            self.contact_table.setItem(row, 0, QTableWidgetItem(str(contact.id)))
            self.contact_table.setItem(row, 1, QTableWidgetItem(contact.name))
            self.contact_table.setItem(row, 2, QTableWidgetItem(contact.work_unit))
            self.contact_table.setItem(row, 3, QTableWidgetItem(contact.phone))
            self.contact_table.setItem(row, 4, QTableWidgetItem(contact.email))

        self.status_label.setText(f'共 {len(self.current_contacts)} 位联系人')

    def add_contact(self):
        """添加联系人"""
        dialog = ContactDialog(self)
        if dialog.exec() == QDialog.Accepted:
            contact = dialog.get_contact()

            # 验证数据
            if not contact.name:
                QMessageBox.warning(self, '错误', '姓名不能为空！')
                return

            if not self.data_manager.is_valid_phone(contact.phone):
                QMessageBox.warning(self, '错误', '电话号码格式错误！\n\n要求：7-15位数字（可包含连字符或空格）')
                return

            if not self.data_manager.is_valid_email(contact.email):
                QMessageBox.warning(self, '错误', 'E-mail地址格式错误！')
                return

            # 添加联系人
            success, message = self.data_manager.add_contact(contact)
            if success:
                self.refresh_table()
                QMessageBox.information(self, '成功', message)
            else:
                QMessageBox.warning(self, '错误', message)

    def delete_contact(self):
        """删除联系人"""
        selected_row = self.contact_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, '警告', '请先选择要删除的联系人！')
            return

        contact = self.current_contacts[selected_row]

        reply = QMessageBox.question(
            self, '确认删除',
            f'确定要删除联系人 "{contact.name}" 吗？',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success, message = self.data_manager.delete_contact(contact.id)
            if success:
                self.refresh_table()
                QMessageBox.information(self, '成功', message)
            else:
                QMessageBox.warning(self, '错误', message)

    def modify_contact(self):
        """修改联系人"""
        selected_row = self.contact_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, '警告', '请先选择要修改的联系人！')
            return

        contact = self.current_contacts[selected_row]

        dialog = ContactDialog(self, contact)
        if dialog.exec() == QDialog.Accepted:
            new_contact = dialog.get_contact()

            # 验证数据
            if not new_contact.name:
                QMessageBox.warning(self, '错误', '姓名不能为空！')
                return

            if not self.data_manager.is_valid_phone(new_contact.phone):
                QMessageBox.warning(self, '错误', '电话号码格式错误！\n\n要求：7-15位数字（可包含连字符或空格）')
                return

            if not self.data_manager.is_valid_email(new_contact.email):
                QMessageBox.warning(self, '错误', 'E-mail地址格式错误！')
                return

            # 更新联系人
            success, message = self.data_manager.update_contact(new_contact)
            if success:
                self.refresh_table()
                QMessageBox.information(self, '成功', message)
            else:
                QMessageBox.warning(self, '错误', message)

    def on_sort_changed(self, index):
        """排序改变"""
        if index == 0:
            self.data_manager.sort_contacts('name')
        else:
            self.data_manager.sort_contacts('phone')
        self.refresh_table()

    def on_search_changed(self, text):
        """搜索改变"""
        if not text:
            self.current_contacts = self.data_manager.get_contacts()
        else:
            field = 'name' if self.search_combo.currentIndex() == 0 else 'phone'
            self.current_contacts = self.data_manager.search_contacts(text, field)
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


class ContactDialog(QDialog):
    """联系人对话框"""

    def __init__(self, parent, contact=None):
        super().__init__(parent)
        self.contact = contact
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('联系人信息')
        self.setFixedSize(500, 300)

        layout = QVBoxLayout()

        # 姓名
        layout.addWidget(QLabel('姓名：'))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('请输入姓名')
        layout.addWidget(self.name_input)

        # 工作单位
        layout.addWidget(QLabel('工作单位：'))
        self.work_input = QLineEdit()
        self.work_input.setPlaceholderText('请输入工作单位')
        layout.addWidget(self.work_input)

        # 电话号码
        layout.addWidget(QLabel('电话号码：'))
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText('请输入电话号码（7-15位）')
        layout.addWidget(self.phone_input)

        # E-mail地址
        layout.addWidget(QLabel('E-mail地址：'))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('请输入E-mail地址')
        layout.addWidget(self.email_input)

        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

        # 如果是编辑模式，填充数据
        if self.contact:
            self.name_input.setText(self.contact.name)
            self.work_input.setText(self.contact.work_unit)
            self.phone_input.setText(self.contact.phone)
            self.email_input.setText(self.contact.email)

    def get_contact(self):
        """获取联系人"""
        from ..data_manager import Contact
        contact_id = self.contact.id if self.contact else 0
        return Contact(
            contact_id,
            self.name_input.text().strip(),
            self.work_input.text().strip(),
            self.phone_input.text().strip(),
            self.email_input.text().strip()
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
