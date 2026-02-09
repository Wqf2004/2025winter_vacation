#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据管理模块
负责学生信息和成绩的读取、写入、验证等操作
"""

import os
from typing import List, Optional, Tuple


class Student:
    """学生信息类"""
    
    def __init__(self, student_id: str = '', name: str = '', 
                 sex: str = '', room: str = '', phone: str = ''):
        self.id = student_id
        self.name = name
        self.sex = sex
        self.room = room
        self.phone = phone
    
    def __str__(self):
        return f'{self.id} {self.name} {self.sex} {self.room} {self.phone}'


class Grade:
    """成绩信息类"""
    
    def __init__(self, student_id: str = '', course_id: str = '', 
                 course_name: str = '', credits: float = 0.0,
                 usual_score: float = 0.0, lab_score: float = -1.0,
                 exam_score: float = 0.0, total_score: float = 0.0):
        self.id = student_id
        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits
        self.usual_score = usual_score
        self.lab_score = lab_score
        self.exam_score = exam_score
        self.total_score = total_score
    
    def __str__(self):
        return f'{self.id} {self.course_id} {self.course_name} {self.credits:.1f} {self.usual_score:.1f} {self.lab_score:.1f} {self.exam_score:.1f} {self.total_score:.1f}'


class DataManager:
    """数据管理器类"""
    
    def __init__(self, data_dir: str = '../dataset'):
        """初始化数据管理器
        
        Args:
            data_dir: 数据文件目录
        """
        self.data_dir = data_dir
        self.student_file = os.path.join(data_dir, 'a.txt')
        self.grade_file = os.path.join(data_dir, 'b.txt')
        self.password_file = os.path.join(data_dir, 'password.txt')
        
        # 确保数据目录存在
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def read_students(self) -> List[Student]:
        """读取学生信息文件
        
        Returns:
            学生信息列表
        """
        if not os.path.exists(self.student_file):
            return []
        
        students = []
        try:
            with open(self.student_file, 'r', encoding='gbk') as f:
                # 跳过表头
                next(f)
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split()
                        if len(parts) >= 5:
                            student = Student(
                                parts[0], parts[1], parts[2], 
                                parts[3], parts[4]
                            )
                            students.append(student)
        except Exception as e:
            print(f'读取学生文件错误: {e}')
        
        return students
    
    def write_students(self, students: List[Student]) -> bool:
        """写入学生信息文件
        
        Args:
            students: 学生信息列表
            
        Returns:
            是否写入成功
        """
        try:
            with open(self.student_file, 'w', encoding='gbk') as f:
                # 写入表头
                f.write('学号 姓名 性别 宿舍号码 电话号码\n')
                # 写入数据
                for student in students:
                    f.write(f'{student}\n')
            return True
        except Exception as e:
            print(f'写入学生文件错误: {e}')
            return False
    
    def read_grades(self) -> List[Grade]:
        """读取成绩信息文件
        
        Returns:
            成绩信息列表
        """
        if not os.path.exists(self.grade_file):
            return []
        
        grades = []
        try:
            with open(self.grade_file, 'r', encoding='gbk') as f:
                # 跳过表头
                next(f)
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split()
                        if len(parts) >= 8:
                            grade = Grade(
                                parts[0], parts[1], parts[2],
                                float(parts[3]), float(parts[4]),
                                float(parts[5]), float(parts[6]),
                                float(parts[7])
                            )
                            grades.append(grade)
        except Exception as e:
            print(f'读取成绩文件错误: {e}')
        
        return grades
    
    def write_grades(self, grades: List[Grade]) -> bool:
        """写入成绩信息文件
        
        Args:
            grades: 成绩信息列表
            
        Returns:
            是否写入成功
        """
        try:
            with open(self.grade_file, 'w', encoding='gbk') as f:
                # 写入表头
                f.write('学号 课程编号 课程名称 学分 平时成绩 实验成绩 卷面成绩 综合成绩\n')
                # 写入数据
                for grade in grades:
                    f.write(f'{grade}\n')
            return True
        except Exception as e:
            print(f'写入成绩文件错误: {e}')
            return False
    
    def check_student_id(self, student_id: str) -> bool:
        """检查学号是否存在
        
        Args:
            student_id: 学号
            
        Returns:
            是否存在
        """
        students = self.read_students()
        return any(student.id == student_id for student in students)
    
    def get_student_name(self, student_id: str) -> str:
        """根据学号获取学生姓名
        
        Args:
            student_id: 学号
            
        Returns:
            学生姓名，如果不存在返回空字符串
        """
        students = self.read_students()
        for student in students:
            if student.id == student_id:
                return student.name
        return ''
    
    def add_grade(self, grade: Grade) -> Tuple[bool, str]:
        """添加成绩记录
        
        Args:
            grade: 成绩对象
            
        Returns:
            (是否成功, 消息)
        """
        # 检查学号是否存在
        if not self.check_student_id(grade.id):
            return False, '该学号不存在于学生信息表中！'
        
        # 计算综合成绩
        grade.total_score = self.calculate_total_score(
            grade.usual_score, grade.lab_score, grade.exam_score
        )
        
        # 计算实得学分
        earned_credits = self.calculate_credits(grade.credits, grade.total_score)
        
        # 读取现有成绩
        grades = self.read_grades()
        
        # 添加新成绩（实得学分替换原学分）
        new_grade = Grade(
            grade.id, grade.course_id, grade.course_name,
            earned_credits, grade.usual_score, grade.lab_score,
            grade.exam_score, grade.total_score
        )
        grades.append(new_grade)
        
        # 写入文件
        if self.write_grades(grades):
            return True, f'成绩记录添加成功！综合成绩：{grade.total_score:.1f}，实得学分：{earned_credits:.1f}'
        else:
            return False, '写入文件失败！'
    
    def delete_student(self, student_id: str) -> Tuple[bool, str]:
        """删除学生及其所有成绩
        
        Args:
            student_id: 学号
            
        Returns:
            (是否成功, 消息)
        """
        # 检查学号是否存在
        if not self.check_student_id(student_id):
            return False, f'未找到学号为 {student_id} 的学生'
        
        # 读取数据
        students = self.read_students()
        grades = self.read_grades()
        
        # 过滤掉该学生的信息
        new_students = [s for s in students if s.id != student_id]
        new_grades = [g for g in grades if g.id != student_id]
        
        # 写入文件
        if self.write_students(new_students) and self.write_grades(new_grades):
            return True, f'学号为 {student_id} 的学生及其所有成绩已成功删除'
        else:
            return False, '删除失败，写入文件错误'
    
    @staticmethod
    def calculate_total_score(usual: float, lab: float, exam: float) -> float:
        """计算综合成绩
        
        Args:
            usual: 平时成绩
            lab: 实验成绩（-1表示无实验）
            exam: 卷面成绩
            
        Returns:
            综合成绩
        """
        if lab != -1:
            return usual * 0.15 + lab * 0.15 + exam * 0.7
        return usual * 0.3 + exam * 0.7
    
    @staticmethod
    def calculate_credits(credit: float, total_score: float) -> float:
        """计算实得学分（等级学分制）
        
        Args:
            credit: 原始学分
            total_score: 综合成绩
            
        Returns:
            实得学分
        """
        if total_score >= 90:
            return credit * 1.0
        elif total_score >= 80:
            return credit * 0.8
        elif total_score >= 70:
            return credit * 0.75
        elif total_score >= 60:
            return credit * 0.6
        else:
            return 0.0
    
    @staticmethod
    def validate_phone_number(phone: str) -> bool:
        """验证手机号码格式
        
        Args:
            phone: 手机号码
            
        Returns:
            是否有效
        """
        if len(phone) != 11:
            return False
        if phone[0] != '1':
            return False
        if phone[1] < '3' or phone[1] > '9':
            return False
        if not phone.isdigit():
            return False
        return True
    
    def read_password(self) -> str:
        """读取密码
        
        Returns:
            密码字符串
        """
        if not os.path.exists(self.password_file):
            # 创建默认密码
            default_password = 'admin123'
            try:
                with open(self.password_file, 'w', encoding='utf-8') as f:
                    f.write(default_password)
            except Exception as e:
                print(f'创建密码文件错误: {e}')
            return default_password
        
        try:
            with open(self.password_file, 'r', encoding='utf-8') as f:
                password = f.read().strip()
                return password
        except Exception as e:
            print(f'读取密码文件错误: {e}')
            return 'admin123'
    
    def write_password(self, password: str) -> bool:
        """写入密码
        
        Args:
            password: 密码
            
        Returns:
            是否写入成功
        """
        try:
            with open(self.password_file, 'w', encoding='utf-8') as f:
                f.write(password.strip())
            return True
        except Exception as e:
            print(f'写入密码文件错误: {e}')
            return False
