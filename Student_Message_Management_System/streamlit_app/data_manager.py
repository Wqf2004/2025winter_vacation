#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据管理模块
负责学生信息和成绩的读取、写入、验证等操作
"""

import os
from typing import List, Tuple
import pandas as pd


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
    
    def read_students(self) -> pd.DataFrame:
        """读取学生信息文件
        
        Returns:
            学生信息DataFrame
        """
        if not os.path.exists(self.student_file):
            return pd.DataFrame(columns=['学号', '姓名', '性别', '宿舍号码', '电话号码'])
        
        try:
            # 使用dtype=str确保所有列都作为字符串读取
            df = pd.read_csv(self.student_file, sep=' ', encoding='gbk', 
                           skipinitialspace=True, dtype=str)
            return df
        except Exception as e:
            print(f'读取学生文件错误: {e}')
            return pd.DataFrame(columns=['学号', '姓名', '性别', '宿舍号码', '电话号码'])
    
    def write_students(self, df: pd.DataFrame) -> bool:
        """写入学生信息文件
        
        Args:
            df: 学生信息DataFrame
            
        Returns:
            是否写入成功
        """
        try:
            df.to_csv(self.student_file, sep=' ', index=False, encoding='gbk')
            return True
        except Exception as e:
            print(f'写入学生文件错误: {e}')
            return False
    
    def read_grades(self) -> pd.DataFrame:
        """读取成绩信息文件
        
        Returns:
            成绩信息DataFrame
        """
        if not os.path.exists(self.grade_file):
            return pd.DataFrame(columns=['学号', '课程编号', '课程名称', '学分', 
                                         '平时成绩', '实验成绩', '卷面成绩', '综合成绩'])
        
        try:
            # 使用dtype=str确保学号、课程编号等作为字符串读取
            # 数值列保持数值类型以便计算
            dtype_dict = {
                '学号': str,
                '课程编号': str,
                '课程名称': str
            }
            df = pd.read_csv(self.grade_file, sep=' ', encoding='gbk', 
                           skipinitialspace=True, dtype=dtype_dict)
            return df
        except Exception as e:
            print(f'读取成绩文件错误: {e}')
            return pd.DataFrame(columns=['学号', '课程编号', '课程名称', '学分', 
                                        '平时成绩', '实验成绩', '卷面成绩', '综合成绩'])
    
    def write_grades(self, df: pd.DataFrame) -> bool:
        """写入成绩信息文件
        
        Args:
            df: 成绩信息DataFrame
            
        Returns:
            是否写入成功
        """
        try:
            df.to_csv(self.grade_file, sep=' ', index=False, encoding='gbk')
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
        df = self.read_students()
        return student_id in df['学号'].values
    
    def get_student_name(self, student_id: str) -> str:
        """根据学号获取学生姓名
        
        Args:
            student_id: 学号
            
        Returns:
            学生姓名，如果不存在返回空字符串
        """
        df = self.read_students()
        student = df[df['学号'] == student_id]
        if not student.empty:
            return student['姓名'].iloc[0]
        return ''
    
    def add_grade(self, grade_data: dict) -> Tuple[bool, str]:
        """添加成绩记录
        
        Args:
            grade_data: 成绩数据字典
            
        Returns:
            (是否成功, 消息)
        """
        # 检查学号是否存在
        if not self.check_student_id(grade_data['学号']):
            return False, '该学号不存在于学生信息表中！'
        
        # 计算综合成绩
        total_score = self.calculate_total_score(
            grade_data['平时成绩'], 
            grade_data['实验成绩'], 
            grade_data['卷面成绩']
        )
        
        # 计算实得学分
        earned_credits = self.calculate_credits(
            grade_data['学分'], 
            total_score
        )
        
        # 读取现有成绩
        df = self.read_grades()
        
        # 添加新成绩
        new_row = {
            '学号': grade_data['学号'],
            '课程编号': grade_data['课程编号'],
            '课程名称': grade_data['课程名称'],
            '学分': earned_credits,
            '平时成绩': grade_data['平时成绩'],
            '实验成绩': grade_data['实验成绩'],
            '卷面成绩': grade_data['卷面成绩'],
            '综合成绩': total_score
        }
        
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        # 写入文件
        if self.write_grades(df):
            return True, f'成绩记录添加成功！综合成绩：{total_score:.1f}，实得学分：{earned_credits:.1f}'
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
        student_df = self.read_students()
        grade_df = self.read_grades()
        
        # 过滤掉该学生的信息
        new_student_df = student_df[student_df['学号'] != student_id]
        new_grade_df = grade_df[grade_df['学号'] != student_id]
        
        # 写入文件
        if self.write_students(new_student_df) and self.write_grades(new_grade_df):
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
