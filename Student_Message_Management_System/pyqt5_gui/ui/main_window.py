#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主窗口
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QDialog,
                             QPushButton, QLabel, QStackedWidget, QMessageBox,
                             QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from .login_dialog import LoginDialog
from .grade_entry_page import GradeEntryPage
from .sort_page import SortPage
from .student_query_page import StudentQueryPage
from .score_query_page import ScoreQueryPage
from .delete_page import DeletePage


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self.setup_ui()
        self.setWindowTitle('学生信息管理系统 (SMMS)')
        self.setMinimumSize(1200, 800)
        
        # 显示登录对话框
        self.show_login()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 创建侧边栏
        self.sidebar = self.create_sidebar()
        splitter.addWidget(self.sidebar)
        
        # 创建内容区域
        self.content_area = QStackedWidget()
        self.content_area.setStyleSheet('background-color: white;')
        splitter.addWidget(self.content_area)
        
        # 设置分割器比例
        splitter.setSizes([200, 1000])
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        
        main_layout.addWidget(splitter)
        
        # 创建各个功能页面
        self.create_pages()
    
    def create_sidebar(self) -> QWidget:
        """创建侧边栏
        
        Returns:
            侧边栏部件
        """
        sidebar = QWidget()
        sidebar.setStyleSheet('''
            QWidget {
                background-color: #2c3e50;
                color: white;
            }
            QPushButton {
                background-color: #34495e;
                border: none;
                padding: 15px;
                text-align: left;
                border-radius: 5px;
                margin: 5px 10px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
            QLabel {
                color: white;
                padding: 20px;
                font-size: 16px;
                font-weight: bold;
            }
        ''')
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # 标题
        title_label = QLabel('系统菜单')
        layout.addWidget(title_label)
        
        # 按钮列表
        self.btn_grade_entry = QPushButton('📝 成绩录入')
        self.btn_grade_entry.clicked.connect(lambda: self.switch_page(0))
        layout.addWidget(self.btn_grade_entry)
        
        self.btn_sort = QPushButton('📊 成绩排序')
        self.btn_sort.clicked.connect(lambda: self.switch_page(1))
        layout.addWidget(self.btn_sort)
        
        self.btn_student_query = QPushButton('👤 学生查询')
        self.btn_student_query.clicked.connect(lambda: self.switch_page(2))
        layout.addWidget(self.btn_student_query)
        
        self.btn_score_query = QPushButton('📈 成绩查询')
        self.btn_score_query.clicked.connect(lambda: self.switch_page(3))
        layout.addWidget(self.btn_score_query)
        
        self.btn_delete = QPushButton('🗑️ 信息删除')
        self.btn_delete.clicked.connect(lambda: self.switch_page(4))
        layout.addWidget(self.btn_delete)
        
        # 添加弹簧
        layout.addStretch()
        
        # 退出按钮
        self.btn_exit = QPushButton('❌ 退出系统')
        self.btn_exit.setStyleSheet('background-color: #e74c3c;')
        self.btn_exit.clicked.connect(self.close)
        layout.addWidget(self.btn_exit)
        
        return sidebar
    
    def create_pages(self):
        """创建功能页面"""
        # 成绩录入页面
        self.grade_entry_page = GradeEntryPage()
        self.content_area.addWidget(self.grade_entry_page)
        
        # 成绩排序页面
        self.sort_page = SortPage()
        self.content_area.addWidget(self.sort_page)
        
        # 学生查询页面
        self.student_query_page = StudentQueryPage()
        self.content_area.addWidget(self.student_query_page)
        
        # 成绩查询页面
        self.score_query_page = ScoreQueryPage()
        self.content_area.addWidget(self.score_query_page)
        
        # 删除页面
        self.delete_page = DeletePage()
        self.content_area.addWidget(self.delete_page)
    
    def switch_page(self, index: int):
        """切换页面
        
        Args:
            index: 页面索引
        """
        self.content_area.setCurrentIndex(index)
        
        # 刷新页面数据
        if index == 0:
            self.grade_entry_page.refresh_data()
        elif index == 1:
            self.sort_page.refresh_data()
    
    def show_login(self):
        """显示登录对话框"""
        dialog = LoginDialog(self)
        if dialog.exec_() != QDialog.Accepted:
            # 登录失败，退出程序
            self.close()
    
    def closeEvent(self, event):
        """关闭事件
        
        Args:
            event: 关闭事件
        """
        reply = QMessageBox.question(
            self, '确认退出', 
            '确定要退出系统吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
