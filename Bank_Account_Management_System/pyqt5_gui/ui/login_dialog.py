"""
登录对话框
"""
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt


class LoginDialog(QDialog):
    """登录对话框"""

    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.attempts = 0
        self.max_attempts = 3
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('登录')
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        # 标题
        title = QLabel('银行账目管理系统')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 16px; font-weight: bold; padding: 20px;')
        layout.addWidget(title)

        # 密码输入
        label = QLabel('请输入密码：')
        layout.addWidget(label)

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setStyleSheet('padding: 8px;')
        self.password_edit.returnPressed.connect(self.login)
        layout.addWidget(self.password_edit)

        # 登录按钮
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
        password = self.password_edit.text().strip()

        if not password:
            QMessageBox.warning(self, '警告', '请输入密码！')
            return

        if self.data_manager.verify_password(password):
            QMessageBox.information(self, '成功', '登录成功！')
            self.accept()
        else:
            self.attempts += 1
            remaining = self.max_attempts - self.attempts

            if remaining > 0:
                QMessageBox.warning(self, '错误', f'密码错误！还剩 {remaining} 次机会。')
                self.password_edit.clear()
            else:
                QMessageBox.critical(self, '错误', '密码错误次数过多，程序退出！')
                self.reject()
