"""
登录对话框
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox)
from PyQt5.QtCore import Qt


class LoginDialog(QDialog):
    """登录对话框"""

    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.current_user = None
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('销售系统 - 登录')
        self.setFixedWidth(350)

        layout = QVBoxLayout()

        title_label = QLabel('🛒 销售系统')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 20px;')
        layout.addWidget(title_label)

        form_layout = QVBoxLayout()

        username_layout = QVBoxLayout()
        username_label = QLabel('用户名：')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('请输入用户名')
        self.username_input.setStyleSheet('padding: 8px;')
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)

        password_layout = QVBoxLayout()
        password_label = QLabel('密码：')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('请输入密码')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet('padding: 8px;')
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)

        form_layout.addLayout(username_layout)
        form_layout.addLayout(password_layout)
        layout.addLayout(form_layout)

        login_btn = QPushButton('登录')
        login_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)

        self.setLayout(layout)

    def login(self):
        """登录验证"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, '警告', '用户名和密码不能为空！')
            return

        user = self.data_manager.verify_user(username, password)
        if user:
            self.current_user = user
            self.accept()
        else:
            QMessageBox.warning(self, '错误', '用户名或密码错误！')
