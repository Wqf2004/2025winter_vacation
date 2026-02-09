"""
班级同学信息管理系统 - 数据管理模块
"""

import os


class Student:
    """学生数据类"""

    def __init__(self, student_id=0, name="", student_number="", dorm="", qq="", phone=""):
        self.id = student_id
        self.name = name
        self.student_number = student_number
        self.dorm = dorm
        self.qq = qq
        self.phone = phone

    def to_string(self):
        """转换为字符串"""
        return f"{self.id}|{self.name}|{self.student_number}|{self.dorm}|{self.qq}|{self.phone}"

    @staticmethod
    def from_string(s):
        """从字符串创建学生"""
        parts = s.strip().split('|')
        if len(parts) >= 6:
            return Student(
                int(parts[0]),
                parts[1],
                parts[2],
                parts[3],
                parts[4],
                parts[5]
            )
        return None


class DataManager:
    """数据管理器"""

    def __init__(self):
        self.students = []
        self.password_file = "../dataset/password.txt"
        self.students_file = "../dataset/students.txt"
        self.load_data()

    def load_data(self):
        """加载数据"""
        self.students = []

        # 加载学生数据
        if os.path.exists(self.students_file):
            try:
                with open(self.students_file, 'r', encoding='gbk') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            student = Student.from_string(line)
                            if student:
                                self.students.append(student)
            except Exception as e:
                print(f"加载学生数据失败: {e}")

    def save_data(self):
        """保存数据"""
        try:
            # 保存学生数据
            with open(self.students_file, 'w', encoding='gbk') as f:
                for student in self.students:
                    f.write(student.to_string() + '\n')
            return True
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False

    def verify_password(self, password):
        """验证密码"""
        try:
            if os.path.exists(self.password_file):
                with open(self.password_file, 'r', encoding='utf-8') as f:
                    stored_password = f.read().strip()
                return self.encrypt_password(password) == stored_password
            else:
                # 首次使用，创建默认密码
                with open(self.password_file, 'w', encoding='utf-8') as f:
                    f.write(self.encrypt_password("admin123"))
                return password == "admin123"
        except Exception as e:
            print(f"验证密码失败: {e}")
            return False

    def change_password(self, old_password, new_password):
        """修改密码"""
        if not self.verify_password(old_password):
            return False

        try:
            with open(self.password_file, 'w', encoding='utf-8') as f:
                f.write(self.encrypt_password(new_password))
            return True
        except Exception as e:
            print(f"修改密码失败: {e}")
            return False

    @staticmethod
    def encrypt_password(password):
        """密码加密"""
        encrypted = ""
        for char in password:
            encrypted += chr(ord(char) ^ 0x55)
        return encrypted

    def add_student(self, student):
        """添加学生"""
        # 生成新ID
        max_id = 0
        for s in self.students:
            if s.id > max_id:
                max_id = s.id
        student.id = max_id + 1

        # 检查学号是否重复
        for s in self.students:
            if s.student_number == student.student_number:
                return False, "该学号已存在！"

        # 检查QQ是否重复
        for s in self.students:
            if s.qq == student.qq:
                return False, "该QQ号码已存在！"

        # 检查电话是否重复
        for s in self.students:
            if s.phone == student.phone:
                return False, "该电话号码已存在！"

        self.students.append(student)
        return True, "添加成功"

    def delete_student(self, student_id):
        """删除学生"""
        for i, s in enumerate(self.students):
            if s.id == student_id:
                self.students.pop(i)
                return True, "删除成功"
        return False, "学生不存在"

    def update_student(self, student):
        """更新学生"""
        for i, s in enumerate(self.students):
            if s.id == student.id:
                # 检查学号是否与其他学生重复
                for j, other in enumerate(self.students):
                    if j != i and other.student_number == student.student_number:
                        return False, "该学号已存在！"

                # 检查QQ是否与其他学生重复
                for j, other in enumerate(self.students):
                    if j != i and other.qq == student.qq:
                        return False, "该QQ号码已存在！"

                # 检查电话是否与其他学生重复
                for j, other in enumerate(self.students):
                    if j != i and other.phone == student.phone:
                        return False, "该电话号码已存在！"

                self.students[i] = student
                return True, "更新成功"
        return False, "学生不存在"

    def search_students(self, keyword, field='name'):
        """搜索学生"""
        results = []
        keyword = keyword.lower()
        for s in self.students:
            if field == 'name':
                if keyword in s.name.lower():
                    results.append(s)
            elif field == 'student_number':
                if keyword in s.student_number.lower():
                    results.append(s)
            elif field == 'phone':
                if keyword in s.phone:
                    results.append(s)
        return results

    def get_students(self):
        """获取所有学生"""
        return self.students

    def sort_students(self, field='name'):
        """排序学生"""
        if field == 'name':
            self.students.sort(key=lambda s: s.name)
        elif field == 'student_number':
            self.students.sort(key=lambda s: s.student_number)

    @staticmethod
    def is_valid_phone(phone):
        """验证电话号码"""
        phone = phone.replace('-', '').replace(' ', '')
        if len(phone) < 7 or len(phone) > 15:
            return False
        return phone.isdigit()

    @staticmethod
    def is_valid_qq(qq):
        """验证QQ号码"""
        if len(qq) < 5 or len(qq) > 12:
            return False
        return qq.isdigit()

    def get_student_count(self):
        """获取学生数量"""
        return len(self.students)
