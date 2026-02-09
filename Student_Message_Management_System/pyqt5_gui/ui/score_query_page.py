#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
成绩查询页面
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QGroupBox,
                             QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from data_manager import DataManager, Grade


class ScoreQueryPage(QWidget):
    """成绩查询页面类"""
    
    def __init__(self):
        """初始化成绩查询页面"""
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
        title_label = QLabel('学生成绩信息查询')
        title_font = QFont('Microsoft YaHei', 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 查询选项
        query_group = QGroupBox('查询选项')
        query_layout = QHBoxLayout(query_group)
        
        query_label = QLabel('请输入学号：')
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText('请输入要查询的学号')
        query_layout.addWidget(query_label)
        query_layout.addWidget(self.input_edit)
        
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
        query_layout.addWidget(query_btn)
        
        layout.addWidget(query_group)
        
        # 结果表格
        table_group = QGroupBox('查询结果')
        table_layout = QVBoxLayout(table_group)
        
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(5)
        self.result_table.setHorizontalHeaderLabels([
            '课程编号', '课程名称', '学分', '平时成绩', '综合成绩'
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
        
        # 回车查询
        self.input_edit.returnPressed.connect(self.on_query)
    
    def on_query(self):
        """查询按钮点击事件"""
        student_id = self.input_edit.text().strip()
        
        if not student_id:
            QMessageBox.warning(self, '输入错误', '请输入学号！')
            return
        
        # 检查学号是否存在
        if not self.data_manager.check_student_id(student_id):
            QMessageBox.warning(self, '查询失败', f'未找到学号为 {student_id} 的学生！')
            return
        
        # 读取成绩数据
        self.grades = self.data_manager.read_grades()
        
        # 筛选该学生的成绩
        results = [g for g in self.grades if g.id == student_id]
        
        if not results:
            QMessageBox.information(self, '提示', f'学号为 {student_id} 的学生暂无成绩记录！')
            self.result_table.setRowCount(0)
            self.status_label.setText('共 0 条记录')
            return
        
        # 计算总学分
        total_credits = sum(g.credits for g in results)
        
        # 更新表格
        self.result_table.setRowCount(len(results))
        for row, grade in enumerate(results):
            self.result_table.setItem(row, 0, QTableWidgetItem(grade.course_id))
            self.result_table.setItem(row, 1, QTableWidgetItem(grade.course_name))
            self.result_table.setItem(row, 2, QTableWidgetItem(f'{grade.credits:.2f}'))
            self.result_table.setItem(row, 3, QTableWidgetItem(f'{grade.usual_score:.1f}'))
            self.result_table.setItem(row, 4, QTableWidgetItem(f'{grade.total_score:.1f}'))
        
        # 更新状态
        self.status_label.setText(f'共 {len(results)} 科，实得总学分为：{total_credits:.2f}')
