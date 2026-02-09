from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QTabWidget,
                             QWidget)
from PyQt5.QtCore import Qt
from data_manager import DataManager

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_user = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('扫雷游戏 - 用户登录')
        self.setFixedSize(350, 300)
        
        layout = QVBoxLayout()
        
        # 创建标签页
        tab_widget = QTabWidget()
        
        # 登录页
        login_widget = QWidget()
        login_layout = QVBoxLayout()
        
        login_label = QLabel('用户登录')
        login_label.setAlignment(Qt.AlignCenter)
        login_label.setStyleSheet('font-size: 18px; font-weight: bold; margin: 10px;')
        login_layout.addWidget(login_label)
        
        self.login_name_edit = QLineEdit()
        self.login_name_edit.setPlaceholderText('请输入用户名')
        login_layout.addWidget(QLabel('用户名:'))
        login_layout.addWidget(self.login_name_edit)
        
        self.login_pass_edit = QLineEdit()
        self.login_pass_edit.setPlaceholderText('请输入密码')
        self.login_pass_edit.setEchoMode(QLineEdit.Password)
        login_layout.addWidget(QLabel('密码:'))
        login_layout.addWidget(self.login_pass_edit)
        
        login_btn = QPushButton('登录')
        login_btn.clicked.connect(self.login)
        login_btn.setStyleSheet('padding: 10px; font-size: 14px; margin-top: 20px;')
        login_layout.addWidget(login_btn)
        
        login_widget.setLayout(login_layout)
        tab_widget.addTab(login_widget, '登录')
        
        # 注册页
        register_widget = QWidget()
        register_layout = QVBoxLayout()
        
        register_label = QLabel('用户注册')
        register_label.setAlignment(Qt.AlignCenter)
        register_label.setStyleSheet('font-size: 18px; font-weight: bold; margin: 10px;')
        register_layout.addWidget(register_label)
        
        self.reg_name_edit = QLineEdit()
        self.reg_name_edit.setPlaceholderText('请输入用户名')
        register_layout.addWidget(QLabel('用户名:'))
        register_layout.addWidget(self.reg_name_edit)
        
        self.reg_pass_edit = QLineEdit()
        self.reg_pass_edit.setPlaceholderText('请输入密码')
        self.reg_pass_edit.setEchoMode(QLineEdit.Password)
        register_layout.addWidget(QLabel('密码:'))
        register_layout.addWidget(self.reg_pass_edit)
        
        self.reg_confirm_edit = QLineEdit()
        self.reg_confirm_edit.setPlaceholderText('请确认密码')
        self.reg_confirm_edit.setEchoMode(QLineEdit.Password)
        register_layout.addWidget(QLabel('确认密码:'))
        register_layout.addWidget(self.reg_confirm_edit)
        
        reg_btn = QPushButton('注册')
        reg_btn.clicked.connect(self.register)
        reg_btn.setStyleSheet('padding: 10px; font-size: 14px; margin-top: 20px;')
        register_layout.addWidget(reg_btn)
        
        register_widget.setLayout(register_layout)
        tab_widget.addTab(register_widget, '注册')
        
        layout.addWidget(tab_widget)
        
        self.setLayout(layout)
    
    def login(self):
        name = self.login_name_edit.text().strip()
        password = self.login_pass_edit.text().strip()
        
        if not name or not password:
            QMessageBox.warning(self, '警告', '请输入用户名和密码')
            return
        
        success, user = DataManager.login_user(name, password)
        if success:
            self.current_user = user
            self.accept()
        else:
            QMessageBox.warning(self, '警告', '用户名或密码错误')
    
    def register(self):
        name = self.reg_name_edit.text().strip()
        password = self.reg_pass_edit.text().strip()
        confirm = self.reg_confirm_edit.text().strip()
        
        if not name or not password:
            QMessageBox.warning(self, '警告', '请输入用户名和密码')
            return
        
        if password != confirm:
            QMessageBox.warning(self, '警告', '两次密码不一致')
            return
        
        success, message = DataManager.register_user(name, password)
        if success:
            QMessageBox.information(self, '成功', '注册成功！请登录')
            # 切换到登录页
            self.parent().tab_widget.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, '警告', message)
