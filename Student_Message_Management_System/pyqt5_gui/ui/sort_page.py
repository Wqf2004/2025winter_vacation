#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
成绩排序页面
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QGroupBox, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from data_manager import DataManager, Grade


class SortPage(QWidget):
    """成绩排序页面类"""
    
    def __init__(self):
        """初始化成绩排序页面"""
        super().__init__()
        self.data_manager = DataManager()
        self.grades = []
        self.students = []
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title_label = QLabel('学生成绩排序')
        title_font = QFont('Microsoft YaHei', 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 排序选项
        sort_group = QGroupBox('排序选项')
        sort_layout = QHBoxLayout(sort_group)
        
        sort_label = QLabel('排序方式：')
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            '按综合成绩升序排列',
            '按综合成绩降序排列',
            '按实得学分升序排列',
            '按实得学分降序排列'
        ])
        self.sort_combo.setFixedWidth(200)
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_combo)
        
        sort_btn = QPushButton('开始排序')
        sort_btn.setStyleSheet('''
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
        sort_btn.clicked.connect(self.on_sort)
        sort_layout.addWidget(sort_btn)
        
        sort_layout.addStretch()
        layout.addWidget(sort_group)
        
        # 结果表格
        table_group = QGroupBox('排序结果')
        table_layout = QVBoxLayout(table_group)
        
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels([
            '学号', '姓名', '课程编号', '课程名称', '实得学分', '综合成绩'
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
    
    def refresh_data(self):
        """刷新数据"""
        self.grades = self.data_manager.read_grades()
        self.students = self.data_manager.read_students()
    
    def on_sort(self):
        """排序按钮点击事件"""
        self.refresh_data()
        
        if not self.grades:
            QMessageBox.warning(self, '提示', '没有成绩记录可排序！')
            return
        
        # 获取排序选项
        option = self.sort_combo.currentIndex()
        
        # 排序
        if option == 0:
            self.grades.sort(key=lambda x: x.total_score, reverse=False)
        elif option == 1:
            self.grades.sort(key=lambda x: x.total_score, reverse=True)
        elif option == 2:
            self.grades.sort(key=lambda x: x.credits, reverse=False)
        elif option == 3:
            self.grades.sort(key=lambda x: x.credits, reverse=True)
        
        # 更新表格
        self.result_table.setRowCount(len(self.grades))
        for row, grade in enumerate(self.grades):
            name = self.data_manager.get_student_name(grade.id)
            self.result_table.setItem(row, 0, QTableWidgetItem(grade.id))
            self.result_table.setItem(row, 1, QTableWidgetItem(name))
            self.result_table.setItem(row, 2, QTableWidgetItem(grade.course_id))
            self.result_table.setItem(row, 3, QTableWidgetItem(grade.course_name))
            self.result_table.setItem(row, 4, QTableWidgetItem(f'{grade.credits:.2f}'))
            self.result_table.setItem(row, 5, QTableWidgetItem(f'{grade.total_score:.1f}'))
        
        # 更新状态
        self.status_label.setText(f'共 {len(self.grades)} 条记录')
