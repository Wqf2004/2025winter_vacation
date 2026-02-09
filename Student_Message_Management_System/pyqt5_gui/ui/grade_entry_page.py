#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
成绩录入页面
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox,
                             QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from data_manager import DataManager, Student, Grade


class GradeEntryPage(QWidget):
    """成绩录入页面类"""
    
    def __init__(self):
        """初始化成绩录入页面"""
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
        title_label = QLabel('学生成绩录入')
        title_font = QFont('Microsoft YaHei', 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 学生列表
        student_group = QGroupBox('当前系统中的学生信息')
        student_layout = QVBoxLayout(student_group)
        
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(5)
        self.student_table.setHorizontalHeaderLabels(['学号', '姓名', '性别', '宿舍号', '电话号码'])
        self.student_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.student_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.student_table.setSelectionBehavior(QTableWidget.SelectRows)
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
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        ''')
        student_layout.addWidget(self.student_table)
        layout.addWidget(student_group)
        
        # 录入表单
        form_group = QGroupBox('录入成绩')
        form_layout = QFormLayout(form_group)
        
        self.student_id_edit = QLineEdit()
        self.student_id_edit.setPlaceholderText('从上方表格选择或手动输入学号')
        self.student_id_edit.setReadOnly(True)
        form_layout.addRow('学号：', self.student_id_edit)
        
        self.course_id_edit = QLineEdit()
        self.course_id_edit.setPlaceholderText('请输入课程编号')
        form_layout.addRow('课程编号：', self.course_id_edit)
        
        self.course_name_edit = QLineEdit()
        self.course_name_edit.setPlaceholderText('请输入课程名称')
        form_layout.addRow('课程名称：', self.course_name_edit)
        
        self.credits_edit = QLineEdit()
        self.credits_edit.setPlaceholderText('请输入学分')
        form_layout.addRow('学分：', self.credits_edit)
        
        self.usual_score_edit = QLineEdit()
        self.usual_score_edit.setPlaceholderText('请输入平时成绩（0-100）')
        form_layout.addRow('平时成绩：', self.usual_score_edit)
        
        self.lab_score_edit = QLineEdit()
        self.lab_score_edit.setPlaceholderText('请输入实验成绩（无实验请输入-1）')
        form_layout.addRow('实验成绩：', self.lab_score_edit)
        
        self.exam_score_edit = QLineEdit()
        self.exam_score_edit.setPlaceholderText('请输入卷面成绩（0-100）')
        form_layout.addRow('卷面成绩：', self.exam_score_edit)
        
        layout.addWidget(form_group)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        submit_btn = QPushButton('提交')
        submit_btn.setFixedWidth(100)
        submit_btn.setStyleSheet('''
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:pressed {
                background-color: #229954;
            }
        ''')
        submit_btn.clicked.connect(self.on_submit)
        button_layout.addWidget(submit_btn)
        
        clear_btn = QPushButton('清空')
        clear_btn.setFixedWidth(100)
        clear_btn.setStyleSheet('''
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #b03a2e;
            }
        ''')
        clear_btn.clicked.connect(self.on_clear)
        button_layout.addWidget(clear_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # 连接表格点击事件
        self.student_table.cellClicked.connect(self.on_student_selected)
        
        # 刷新数据
        self.refresh_data()
    
    def refresh_data(self):
        """刷新数据"""
        # 读取学生信息
        self.students = self.data_manager.read_students()
        
        # 更新表格
        self.student_table.setRowCount(len(self.students))
        for row, student in enumerate(self.students):
            self.student_table.setItem(row, 0, QTableWidgetItem(student.id))
            self.student_table.setItem(row, 1, QTableWidgetItem(student.name))
            self.student_table.setItem(row, 2, QTableWidgetItem(student.sex))
            self.student_table.setItem(row, 3, QTableWidgetItem(student.room))
            self.student_table.setItem(row, 4, QTableWidgetItem(student.phone))
    
    def on_student_selected(self, row: int, column: int):
        """学生选中事件
        
        Args:
            row: 行号
            column: 列号
        """
        student_id = self.student_table.item(row, 0).text()
        self.student_id_edit.setText(student_id)
    
    def on_submit(self):
        """提交按钮点击事件"""
        # 获取输入
        student_id = self.student_id_edit.text().strip()
        course_id = self.course_id_edit.text().strip()
        course_name = self.course_name_edit.text().strip()
        credits_str = self.credits_edit.text().strip()
        usual_str = self.usual_score_edit.text().strip()
        lab_str = self.lab_score_edit.text().strip()
        exam_str = self.exam_score_edit.text().strip()
        
        # 验证输入
        if not student_id:
            QMessageBox.warning(self, '输入错误', '请选择或输入学号！')
            return
        
        if not course_id:
            QMessageBox.warning(self, '输入错误', '请输入课程编号！')
            return
        
        if not course_name:
            QMessageBox.warning(self, '输入错误', '请输入课程名称！')
            return
        
        try:
            credits = float(credits_str)
            if credits <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, '输入错误', '学分必须是正数！')
            return
        
        try:
            usual = float(usual_str)
            if not (0 <= usual <= 100):
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, '输入错误', '平时成绩必须是0-100之间的数字！')
            return
        
        try:
            lab = float(lab_str)
            if lab != -1 and not (0 <= lab <= 100):
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, '输入错误', '实验成绩必须是-1或0-100之间的数字！')
            return
        
        try:
            exam = float(exam_str)
            if not (0 <= exam <= 100):
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, '输入错误', '卷面成绩必须是0-100之间的数字！')
            return
        
        # 创建成绩对象
        grade = Grade(student_id, course_id, course_name, credits,
                      usual, lab, exam)
        
        # 添加成绩
        success, message = self.data_manager.add_grade(grade)
        
        if success:
            QMessageBox.information(self, '成功', message)
            self.on_clear()
        else:
            QMessageBox.warning(self, '失败', message)
    
    def on_clear(self):
        """清空输入"""
        self.student_id_edit.clear()
        self.course_id_edit.clear()
        self.course_name_edit.clear()
        self.credits_edit.clear()
        self.usual_score_edit.clear()
        self.lab_score_edit.clear()
        self.exam_score_edit.clear()
