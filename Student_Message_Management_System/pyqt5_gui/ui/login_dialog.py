#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
登录对话框
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from data_manager import DataManager


class LoginDialog(QDialog):
    """登录对话框类"""
    
    def __init__(self, parent=None):
        """初始化登录对话框
        
        Args:
            parent: 父窗口
        """
        super().__init__(parent)
        self.data_manager = DataManager()
        self.attempts = 3
        self.setup_ui()
        self.setWindowTitle('系统登录')
        self.setFixedSize(400, 250)
    
    def setup_ui(self):
        """设置用户界面"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title_label = QLabel('学生信息管理系统')
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont('Microsoft YaHei', 16, QFont.Bold)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # 用户名输入
        username_layout = QHBoxLayout()
        username_label = QLabel('用户名：')
        username_label.setFixedWidth(80)
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText('请输入用户名')
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_edit)
        layout.addLayout(username_layout)
        
        # 密码输入
        password_layout = QHBoxLayout()
        password_label = QLabel('密码：')
        password_label.setFixedWidth(80)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText('请输入密码')
        self.password_edit.returnPressed.connect(self.on_login)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_edit)
        layout.addLayout(password_layout)
        
        # 登录按钮
        login_btn = QPushButton('登录')
        login_btn.setFixedHeight(40)
        login_btn.clicked.connect(self.on_login)
        layout.addWidget(login_btn)
        
        # 提示标签
        self.hint_label = QLabel('')
        self.hint_label.setAlignment(Qt.AlignCenter)
        self.hint_label.setStyleSheet('color: red;')
        layout.addWidget(self.hint_label)
        
        self.setLayout(layout)
    
    def on_login(self):
        """登录按钮点击事件"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        
        if not username or not password:
            self.show_hint('请输入用户名和密码！')
            return
        
        # 读取密码文件
        correct_password = self.data_manager.read_password()
        
        # 验证密码
        if password == correct_password:
            QMessageBox.information(self, '登录成功', '登录成功！正在进入系统...')
            self.accept()
        else:
            self.attempts -= 1
            if self.attempts > 0:
                self.show_hint(f'密码错误！剩余尝试次数：{self.attempts}')
                self.password_edit.clear()
                self.password_edit.setFocus()
            else:
                QMessageBox.warning(self, '登录失败', '登录失败！系统退出。')
                self.reject()
    
    def show_hint(self, message: str):
        """显示提示信息
        
        Args:
            message: 提示消息
        """
        self.hint_label.setText(message)
