#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
信息删除页面
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QGroupBox,
                             QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from data_manager import DataManager, Student


class DeletePage(QWidget):
    """信息删除页面类"""
    
    def __init__(self):
        """初始化信息删除页面"""
        super().__init__()
        self.data_manager = DataManager()
        self.students = []
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title_label = QLabel('学生信息删除')
        title_font = QFont('Microsoft YaHei', 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 警告信息
        warning_label = QLabel('⚠️ 警告：删除操作不可恢复，请谨慎操作！')
        warning_label.setAlignment(Qt.AlignCenter)
        warning_label.setStyleSheet('color: #e74c3c; font-weight: bold; font-size: 14px;')
        layout.addWidget(warning_label)
        
        # 删除选项
        delete_group = QGroupBox('删除选项')
        delete_layout = QHBoxLayout(delete_group)
        
        delete_label = QLabel('请输入要删除的学生学号：')
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText('请输入学号')
        delete_layout.addWidget(delete_label)
        delete_layout.addWidget(self.input_edit)
        
        search_btn = QPushButton('查询')
        search_btn.setStyleSheet('''
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            QPushButton:pressed {
                background-color: #d68910;
            }
        ''')
        search_btn.clicked.connect(self.on_search)
        delete_layout.addWidget(search_btn)
        
        layout.addWidget(delete_group)
        
        # 学生信息表格
        table_group = QGroupBox('学生信息')
        table_layout = QVBoxLayout(table_group)
        
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(5)
        self.student_table.setHorizontalHeaderLabels([
            '学号', '姓名', '性别', '宿舍号', '电话号码'
        ])
        self.student_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.student_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.student_table.setStyleSheet('''
            QTableWidget {
                gridline-color: #bdc3c7;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
        ''')
        table_layout.addWidget(self.student_table)
        layout.addWidget(table_group)
        
        # 删除按钮
        button_layout = QHBoxLayout()
        self.delete_btn = QPushButton('删除该学生及其所有成绩')
        self.delete_btn.setFixedWidth(200)
        self.delete_btn.setEnabled(False)
        self.delete_btn.setStyleSheet('''
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #b03a2e;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        ''')
        self.delete_btn.clicked.connect(self.on_delete)
        button_layout.addWidget(self.delete_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # 当前学号
        self.current_id = ''
        
        # 回车查询
        self.input_edit.returnPressed.connect(self.on_search)
    
    def on_search(self):
        """查询按钮点击事件"""
        student_id = self.input_edit.text().strip()
        
        if not student_id:
            QMessageBox.warning(self, '输入错误', '请输入学号！')
            return
        
        # 读取学生数据
        self.students = self.data_manager.read_students()
        
        # 查找学生
        found = None
        for student in self.students:
            if student.id == student_id:
                found = student
                break
        
        if found is None:
            QMessageBox.warning(self, '查询失败', f'未找到学号为 {student_id} 的学生！')
            self.student_table.setRowCount(0)
            self.delete_btn.setEnabled(False)
            self.current_id = ''
            return
        
        # 显示学生信息
        self.student_table.setRowCount(1)
        self.student_table.setItem(0, 0, QTableWidgetItem(found.id))
        self.student_table.setItem(0, 1, QTableWidgetItem(found.name))
        self.student_table.setItem(0, 2, QTableWidgetItem(found.sex))
        self.student_table.setItem(0, 3, QTableWidgetItem(found.room))
        self.student_table.setItem(0, 4, QTableWidgetItem(found.phone))
        
        # 启用删除按钮
        self.delete_btn.setEnabled(True)
        self.current_id = student_id
    
    def on_delete(self):
        """删除按钮点击事件"""
        if not self.current_id:
            return
        
        # 确认删除
        reply = QMessageBox.question(
            self, '确认删除',
            f'确定要删除学号为 {self.current_id} 的学生及其所有成绩吗？\n\n此操作不可恢复！',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        # 执行删除
        success, message = self.data_manager.delete_student(self.current_id)
        
        if success:
            QMessageBox.information(self, '成功', message)
            # 清空界面
            self.input_edit.clear()
            self.student_table.setRowCount(0)
            self.delete_btn.setEnabled(False)
            self.current_id = ''
        else:
            QMessageBox.warning(self, '失败', message)
