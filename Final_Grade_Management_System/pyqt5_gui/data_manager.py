"""
期末成绩管理系统 - 数据管理模块
"""
import os


class StudentBasic:
    """学生基本情况类"""

    def __init__(self, student_id, name, sex, birth_date, enroll_date, award_count=0, makeup_count=0, retain_count=0):
        self.id = student_id
        self.name = name
        self.sex = sex
        self.birth_date = birth_date
        self.enroll_date = enroll_date
        self.award_count = award_count
        self.makeup_count = makeup_count
        self.retain_count = retain_count


class StudentGrade:
    """学生成绩类"""

    def __init__(self, student_id, computer_score, math_score, english_score, pe_score, average_score):
        self.id = student_id
        self.computer_score = computer_score
        self.math_score = math_score
        self.english_score = english_score
        self.pe_score = pe_score
        self.average_score = average_score


class DataManager:
    """数据管理类"""

    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.dataset_dir = os.path.join(base_dir, 'dataset')
        self.basic_file = os.path.join(self.dataset_dir, 'StudentBasic.txt')
        self.grade_file = os.path.join(self.dataset_dir, 'StudentGrade.txt')
        self.password_file = os.path.join(self.dataset_dir, 'password.txt')

    def read_student_basics(self):
        """读取学生基本情况"""
        basics = []
        if not os.path.exists(self.basic_file):
            return basics

        with open(self.basic_file, 'r', encoding='gb2312') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 8:
                    basic = StudentBasic(
                        parts[0], parts[1], parts[2], parts[3], parts[4],
                        int(parts[5]), int(parts[6]), int(parts[7])
                    )
                    basics.append(basic)
        return basics

    def read_student_grades(self):
        """读取学生成绩"""
        grades = []
        if not os.path.exists(self.grade_file):
            return grades

        with open(self.grade_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 6:
                    grade = StudentGrade(
                        parts[0], float(parts[1]), float(parts[2]),
                        float(parts[3]), float(parts[4]), float(parts[5])
                    )
                    grades.append(grade)
        return grades

    def save_student_grades(self, grades):
        """保存学生成绩"""
        with open(self.grade_file, 'w', encoding='utf-8') as f:
            for grade in grades:
                f.write(f"{grade.id} {grade.computer_score:.2f} {grade.math_score:.2f} "
                        f"{grade.english_score:.2f} {grade.pe_score:.2f} {grade.average_score:.2f}\n")

    def verify_password(self, password):
        """验证密码"""
        if not os.path.exists(self.password_file):
            return False

        with open(self.password_file, 'r', encoding='gbk') as f:
            stored_password = f.read().strip()
            return password == stored_password

    def get_student_basic_by_id(self, basics, student_id):
        """根据学号获取学生基本情况"""
        for basic in basics:
            if basic.id == student_id:
                return basic
        return None

    def get_student_grade_by_id(self, grades, student_id):
        """根据学号获取学生成绩"""
        for grade in grades:
            if grade.id == student_id:
                return grade
        return None

    def validate_phone(self, phone):
        """验证手机号码格式"""
        if len(phone) != 11:
            return False
        return phone.isdigit()

    def validate_birth_date(self, date_str):
        """验证出生日期格式（YYYYMMDD）"""
        if len(date_str) != 8:
            return False
        if not date_str.isdigit():
            return False

        # 验证月份
        month = int(date_str[4:6])
        if month < 1 or month > 12:
            return False

        # 验证日期
        day = int(date_str[6:8])
        if day < 1 or day > 31:
            return False

        return True

    def calculate_award(self, average_score):
        """计算奖励金额"""
        if average_score >= 95:
            return 1200
        elif average_score >= 90:
            return 800
        elif average_score >= 85:
            return 400
        else:
            return 0
