"""
登录对话框
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt


class LoginDialog(QDialog):
    """登录对话框"""

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.password = ""
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('登录 - 班级同学信息管理系统')
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        # 标题
        title_label = QLabel('班级同学信息管理系统')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 20px; font-weight: bold; margin: 20px;')
        layout.addWidget(title_label)

        # 密码输入
        password_label = QLabel('请输入密码：')
        password_label.setStyleSheet('margin-left: 20px;')
        layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText('默认密码: admin123')
        self.password_input.setStyleSheet('margin: 0 20px 10px 20px;')
        layout.addWidget(self.password_input)

        # 登录按钮
        login_button = QPushButton('登录')
        login_button.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 1px solid #45a049;
                padding: 12px;
                margin: 20px;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
                border: 1px solid #3d8b40;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        ''')
        login_button.setMinimumHeight(50)
        login_button.clicked.connect(self.on_login)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def on_login(self):
        """登录处理"""
        password = self.password_input.text()

        if not password:
            QMessageBox.warning(self, '警告', '请输入密码！')
            return

        if self.data_manager.verify_password(password):
            self.password = password
            self.accept()
        else:
            QMessageBox.warning(self, '错误', '密码错误！')
            self.password_input.clear()
            self.password_input.setFocus()
