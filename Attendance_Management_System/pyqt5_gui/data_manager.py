"""
出勤管理系统 - 数据管理模块
"""
import os
from datetime import datetime


class Employee:
    """职工基本信息类"""

    def __init__(self, emp_id, name, sex, birth_date, level, department):
        self.id = emp_id
        self.name = name
        self.sex = sex
        self.birth_date = birth_date
        self.level = level
        self.department = department


class Attendance:
    """职工月出勤情况类"""

    def __init__(self, emp_id, late_count=0, leave_days=0, absent_days=0):
        self.id = emp_id
        self.late_count = late_count
        self.leave_days = leave_days
        self.absent_days = absent_days


class PunchRecord:
    """当日打卡记录类"""

    def __init__(self, emp_id, hour, minute, second):
        self.id = emp_id
        self.hour = hour
        self.minute = minute
        self.second = second


class DataManager:
    """数据管理类"""

    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.dataset_dir = os.path.join(base_dir, 'dataset')
        self.emp_file = os.path.join(self.dataset_dir, 'EmpBasic.txt')
        self.att_file = os.path.join(self.dataset_dir, 'Attendance.txt')
        self.punch_file = os.path.join(self.dataset_dir, 'punchIn.txt')
        self.month_file = os.path.join(self.dataset_dir, 'MonthPunchIn.txt')
        self.password_file = os.path.join(self.dataset_dir, 'password.txt')

    def read_employees(self):
        """读取职工基本信息"""
        employees = []
        if not os.path.exists(self.emp_file):
            return employees

        with open(self.emp_file, 'r', encoding='gb2312') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 6:
                    emp = Employee(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5])
                    employees.append(emp)
        return employees

    def read_attendance(self):
        """读取出勤信息"""
        attendances = []
        if not os.path.exists(self.att_file):
            return attendances

        with open(self.att_file, 'r', encoding='gbk') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 4:
                    att = Attendance(parts[0], int(parts[1]), int(parts[2]), int(parts[3]))
                    attendances.append(att)
        return attendances

    def read_punch_records(self):
        """读取打卡记录"""
        records = []
        if not os.path.exists(self.punch_file):
            return records

        with open(self.punch_file, 'r', encoding='gbk') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 4:
                    record = PunchRecord(parts[0], int(parts[1]), int(parts[2]), int(parts[3]))
                    records.append(record)
        return records

    def save_attendance(self, attendances):
        """保存出勤信息"""
        with open(self.att_file, 'w', encoding='gbk') as f:
            for att in attendances:
                f.write(f"{att.id} {att.late_count} {att.leave_days} {att.absent_days}\n")

    def append_month_records(self, records):
        """追加到月打卡记录"""
        with open(self.month_file, 'a', encoding='gbk') as f:
            for record in records:
                f.write(f"{record.id} {record.hour} {record.minute} {record.second}\n")

    def verify_password(self, password):
        """验证密码"""
        if not os.path.exists(self.password_file):
            return False

        with open(self.password_file, 'r', encoding='gbk') as f:
            stored_password = f.read().strip()
            return password == stored_password

    def calculate_age(self, birth_date):
        """计算年龄"""
        try:
            year = int(birth_date[:4])
            month = int(birth_date[4:6])
            day = int(birth_date[6:8])

            today = datetime.now()
            age = today.year - year

            if today.month < month or (today.month == month and today.day < day):
                age -= 1

            return age
        except:
            return 0

    def get_allowed_leave_days(self, employee):
        """获取允许请假天数"""
        allowed = 0
        age = self.calculate_age(employee.birth_date)

        if employee.sex == '女':
            allowed += 3

        if employee.sex == '男' and age >= 55:
            allowed += 2

        today = datetime.now()
        birth_month = int(employee.birth_date[4:6])

        if today.month == birth_month:
            allowed += 1

        return allowed

    def process_punch_records(self, employees, attendances, records):
        """处理打卡记录，更新出勤情况"""
        for emp in employees:
            punched = False
            late_time = 0

            for record in records:
                if record.id == emp.id:
                    punched = True
                    arrival_time = record.hour * 3600 + record.minute * 60 + record.second
                    standard_time = 8 * 3600

                    if arrival_time > standard_time:
                        late_time = arrival_time - standard_time
                    break

            att = next((a for a in attendances if a.id == emp.id), None)

            if att:
                if not punched or late_time >= 3600:
                    att.absent_days += 1
                elif late_time > 0:
                    late_minutes = late_time // 60
                    late_count = (late_minutes + 9) // 10
                    att.late_count += late_count

        return attendances

    def get_employee_by_id(self, employees, emp_id):
        """根据ID获取职工信息"""
        for emp in employees:
            if emp.id == emp_id:
                return emp
        return None

    def get_attendance_by_id(self, attendances, emp_id):
        """根据ID获取出勤信息"""
        for att in attendances:
            if att.id == emp_id:
                return att
        return None

    def get_punch_record_by_id(self, records, emp_id):
        """根据ID获取当日打卡记录"""
        for record in records:
            if record.id == emp_id:
                return record
        return None
