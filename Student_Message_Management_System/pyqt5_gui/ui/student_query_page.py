#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
学生查询页面
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QGroupBox,
                             QRadioButton, QButtonGroup, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from data_manager import DataManager, Student


class StudentQueryPage(QWidget):
    """学生查询页面类"""
    
    def __init__(self):
        """初始化学生查询页面"""
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
        title_label = QLabel('学生基本信息查询')
        title_font = QFont('Microsoft YaHei', 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 查询选项
        query_group = QGroupBox('查询选项')
        query_layout = QVBoxLayout(query_group)
        
        # 查询方式选择
        radio_layout = QHBoxLayout()
        self.radio_id = QRadioButton('按学号查询')
        self.radio_name = QRadioButton('按姓名查询')
        self.radio_dorm = QRadioButton('按宿舍号查询')
        self.radio_id.setChecked(True)
        
        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.radio_id, 0)
        self.radio_group.addButton(self.radio_name, 1)
        self.radio_group.addButton(self.radio_dorm, 2)
        
        radio_layout.addWidget(self.radio_id)
        radio_layout.addWidget(self.radio_name)
        radio_layout.addWidget(self.radio_dorm)
        radio_layout.addStretch()
        query_layout.addLayout(radio_layout)
        
        # 输入框和按钮
        input_layout = QHBoxLayout()
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText('请输入学号')
        input_layout.addWidget(self.input_edit)
        
        query_btn = QPushButton('查询')
        query_btn.setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1a5276;
            }
        ''')
        query_btn.clicked.connect(self.on_query)
        input_layout.addWidget(query_btn)
        
        query_layout.addLayout(input_layout)
        layout.addWidget(query_group)
        
        # 结果表格
        table_group = QGroupBox('查询结果')
        table_layout = QVBoxLayout(table_group)
        
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(5)
        self.result_table.setHorizontalHeaderLabels([
            '学号', '姓名', '性别', '宿舍号', '电话号码'
        ])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.result_table.setStyleSheet('''
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
        table_layout.addWidget(self.result_table)
        layout.addWidget(table_group)
        
        # 统计信息
        self.status_label = QLabel('共 0 条记录')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet('color: #7f8c8d; font-size: 12px;')
        layout.addWidget(self.status_label)
        
        # 连接单选按钮事件
        self.radio_group.buttonClicked.connect(self.on_radio_changed)
        
        # 回车查询
        self.input_edit.returnPressed.connect(self.on_query)
    
    def on_radio_changed(self, button):
        """单选按钮切换事件
        
        Args:
            button: 被点击的按钮
        """
        if button == self.radio_id:
            self.input_edit.setPlaceholderText('请输入学号')
        elif button == self.radio_name:
            self.input_edit.setPlaceholderText('请输入姓名')
        elif button == self.radio_dorm:
            self.input_edit.setPlaceholderText('请输入宿舍号')
    
    def on_query(self):
        """查询按钮点击事件"""
        keyword = self.input_edit.text().strip()
        
        if not keyword:
            QMessageBox.warning(self, '输入错误', '请输入查询内容！')
            return
        
        # 读取学生数据
        self.students = self.data_manager.read_students()
        
        # 根据查询方式筛选
        results = []
        if self.radio_id.isChecked():
            results = [s for s in self.students if s.id == keyword]
        elif self.radio_name.isChecked():
            results = [s for s in self.students if s.name == keyword]
        elif self.radio_dorm.isChecked():
            results = [s for s in self.students if s.room == keyword]
        
        # 更新表格
        self.result_table.setRowCount(len(results))
        for row, student in enumerate(results):
            self.result_table.setItem(row, 0, QTableWidgetItem(student.id))
            self.result_table.setItem(row, 1, QTableWidgetItem(student.name))
            self.result_table.setItem(row, 2, QTableWidgetItem(student.sex))
            self.result_table.setItem(row, 3, QTableWidgetItem(student.room))
            self.result_table.setItem(row, 4, QTableWidgetItem(student.phone))
            
            # 验证手机号码格式
            is_valid = self.data_manager.validate_phone_number(student.phone)
            phone_item = self.result_table.item(row, 4)
            if is_valid:
                phone_item.setForeground(Qt.darkGreen)
            else:
                phone_item.setForeground(Qt.red)
        
        # 更新状态
        self.status_label.setText(f'共 {len(results)} 条记录')
