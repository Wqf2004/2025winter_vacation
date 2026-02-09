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
        self.init_ui()
        self.is_logged_in = False

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('系统登录')
        self.setFixedSize(350, 200)

        layout = QVBoxLayout()

        title_label = QLabel('期末成绩管理系统')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 18px; font-weight: bold; margin: 10px;')

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText('请输入密码')
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.returnPressed.connect(self.on_login)
        self.password_edit.setStyleSheet('padding: 8px; font-size: 12px;')

        login_btn = QPushButton('登录')
        login_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        login_btn.clicked.connect(self.on_login)

        cancel_btn = QPushButton('取消')
        cancel_btn.setStyleSheet('''
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        ''')
        cancel_btn.clicked.connect(self.reject)

        layout.addWidget(title_label)
        layout.addWidget(QLabel('密码：'))
        layout.addWidget(self.password_edit)
        layout.addWidget(login_btn)
        layout.addWidget(cancel_btn)
        layout.addSpacing(20)

        self.setLayout(layout)

    def on_login(self):
        """登录按钮点击事件"""
        password = self.password_edit.text().strip()

        if not password:
            QMessageBox.warning(self, '提示', '请输入密码！')
            return

        if self.data_manager.verify_password(password):
            self.is_logged_in = True
            self.accept()
        else:
            QMessageBox.warning(self, '错误', '密码错误！')
            self.password_edit.clear()
