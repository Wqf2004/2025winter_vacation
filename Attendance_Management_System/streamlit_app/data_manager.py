"""
出勤管理系统 - 数据管理模块
"""
import os
from datetime import datetime
import pandas as pd


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

    def read_employees_df(self):
        """读取职工基本信息为DataFrame"""
        if not os.path.exists(self.emp_file):
            return pd.DataFrame(columns=['编号', '姓名', '性别', '出生日期', '职务级别', '所在部门'])

        df = pd.read_csv(self.emp_file, sep=' ', encoding='gbk', skipinitialspace=True,
                         names=['编号', '姓名', '性别', '出生日期', '职务级别', '所在部门'])
        df['编号'] = df['编号'].astype(str)
        return df

    def read_attendance_df(self):
        """读取出勤信息为DataFrame"""
        if not os.path.exists(self.att_file):
            return pd.DataFrame(columns=['编号', '迟到次数', '请假天数', '旷工天数'])

        df = pd.read_csv(self.att_file, sep=' ', encoding='gbk', skipinitialspace=True,
                         names=['编号', '迟到次数', '请假天数', '旷工天数'], dtype={'编号': str})
        return df

    def read_punch_records_df(self):
        """读取打卡记录为DataFrame"""
        if not os.path.exists(self.punch_file):
            return pd.DataFrame(columns=['编号', '时', '分', '秒'])

        df = pd.read_csv(self.punch_file, sep=' ', encoding='gbk', skipinitialspace=True,
                         names=['编号', '时', '分', '秒'], dtype={'编号': str})
        return df

    def save_attendance_df(self, df):
        """保存出勤信息"""
        df.to_csv(self.att_file, sep=' ', index=False, header=False, encoding='gbk')

    def append_month_records_df(self, df):
        """追加到月打卡记录"""
        df.to_csv(self.month_file, sep=' ', index=False, header=False, mode='a', encoding='gbk')

    def verify_password(self, password):
        """验证密码"""
        if not os.path.exists(self.password_file):
            return False

        with open(self.password_file, 'r', encoding='utf-8') as f:
            stored_password = f.read().strip()
            return password == stored_password

    def calculate_age(self, birth_date_str):
        """计算年龄"""
        try:
            birth_date_str = str(birth_date_str)
            year = int(birth_date_str[:4])
            month = int(birth_date_str[4:6])
            day = int(birth_date_str[6:8])

            today = datetime.now()
            age = today.year - year

            if today.month < month or (today.month == month and today.day < day):
                age -= 1

            return age
        except:
            return 0

    def get_allowed_leave_days(self, sex, birth_date_str):
        """获取允许请假天数"""
        allowed = 0
        age = self.calculate_age(birth_date_str)

        if sex == '女':
            allowed += 3

        if sex == '男' and age >= 55:
            allowed += 2

        today = datetime.now()
        birth_date_str = str(birth_date_str)
        birth_month = int(birth_date_str[4:6])

        if today.month == birth_month:
            allowed += 1

        return allowed

    def process_punch_records_df(self, emp_df, att_df, punch_df):
        """处理打卡记录，更新出勤情况"""
        att_df = att_df.copy()

        for idx, emp in emp_df.iterrows():
            emp_id = emp['编号']
            punched = False
            late_time = 0

            emp_punch = punch_df[punch_df['编号'] == emp_id]
            if not emp_punch.empty:
                punched = True
                record = emp_punch.iloc[0]
                arrival_time = record['时'] * 3600 + record['分'] * 60 + record['秒']
                standard_time = 8 * 3600

                if arrival_time > standard_time:
                    late_time = arrival_time - standard_time

            att_idx = att_df[att_df['编号'] == emp_id].index

            if len(att_idx) > 0:
                idx_val = att_idx[0]

                if not punched or late_time >= 3600:
                    att_df.at[idx_val, '旷工天数'] += 1
                elif late_time > 0:
                    late_minutes = late_time // 60
                    late_count = (late_minutes + 9) // 10
                    att_df.at[idx_val, '迟到次数'] += late_count

        return att_df

    def query_by_id(self, emp_df, att_df, punch_df, emp_id):
        """按编号查询"""
        emp = emp_df[emp_df['编号'] == emp_id]

        if emp.empty:
            return None, None, None

        att = att_df[att_df['编号'] == emp_id]
        punch = punch_df[punch_df['编号'] == emp_id]

        punch_info = None
        if not punch.empty:
            record = punch.iloc[0]
            punch_info = f"{record['时']:02d}:{record['分']:02d}:{record['秒']:02d}"

        return emp, att, punch_info

    def get_perfect_attendance(self, emp_df, att_df):
        """获取全勤职工"""
        perfect_df = att_df[(att_df['迟到次数'] == 0) &
                           (att_df['请假天数'] == 0) &
                           (att_df['旷工天数'] == 0)]

        if perfect_df.empty:
            return pd.DataFrame()

        return emp_df[emp_df['编号'].isin(perfect_df['编号'])][
            ['编号', '姓名', '性别', '出生日期']
        ]

    def get_excessive_leave(self, emp_df, att_df):
        """获取请假天数超过5天的职工"""
        results = []

        for idx, emp in emp_df.iterrows():
            emp_id = emp['编号']
            att = att_df[att_df['编号'] == emp_id]

            if not att.empty:
                allowed = self.get_allowed_leave_days(emp['性别'], emp['出生日期'])
                actual = att.iloc[0]['请假天数']
                exceeded = actual - allowed

                if actual > 5:
                    results.append({
                        '编号': emp_id,
                        '姓名': emp['姓名'],
                        '性别': emp['性别'],
                        '出生日期': emp['出生日期'],
                        '允许天数': allowed,
                        '实际天数': actual,
                        '超出天数': exceeded
                    })

        return pd.DataFrame(results)

    def get_absent_employees(self, emp_df, att_df):
        """获取旷工职工"""
        absent_df = att_df[att_df['旷工天数'] > 0]

        if absent_df.empty:
            return pd.DataFrame()

        merged_df = emp_df.merge(absent_df, on='编号')
        return merged_df[['编号', '姓名', '性别', '出生日期', '迟到次数', '请假天数', '旷工天数']]

    def calculate_statistics(self, emp_df, att_df, punch_df):
        """计算统计信息"""
        total_emp = len(emp_df)
        perfect_count = len(att_df[(att_df['迟到次数'] == 0) &
                                   (att_df['请假天数'] == 0) &
                                   (att_df['旷工天数'] == 0)])

        max_late_minutes = 0
        late_today_count = 0

        for idx, record in punch_df.iterrows():
            arrival_time = record['时'] * 3600 + record['分'] * 60 + record['秒']
            standard_time = 8 * 3600

            if arrival_time > standard_time:
                late_time = arrival_time - standard_time
                if late_time > max_late_minutes:
                    max_late_minutes = late_time
                late_today_count += 1

        max_leave_days = att_df['请假天数'].max() if not att_df.empty else 0
        max_late_count = att_df['迟到次数'].max() if not att_df.empty else 0
        max_absent_days = att_df['旷工天数'].max() if not att_df.empty else 0

        perfect_rate = (perfect_count / total_emp * 100) if total_emp > 0 else 0
        late_today_rate = (late_today_count / total_emp * 100) if total_emp > 0 else 0

        return {
            'total_emp': total_emp,
            'perfect_count': perfect_count,
            'perfect_rate': perfect_rate,
            'max_late_minutes': max_late_minutes,
            'late_today_count': late_today_count,
            'late_today_rate': late_today_rate,
            'max_leave_days': max_leave_days,
            'max_late_count': max_late_count,
            'max_absent_days': max_absent_days
        }

    def get_earliest_arrival(self, emp_df, punch_df):
        """获取最早到厂的职工"""
        if punch_df.empty:
            return None

        punch_df['arrival_time'] = punch_df['时'] * 3600 + punch_df['分'] * 60 + punch_df['秒']
        earliest_idx = punch_df['arrival_time'].idxmin()
        earliest = punch_df.loc[earliest_idx]

        emp = emp_df[emp_df['编号'] == earliest['编号']]

        if emp.empty:
            return None

        emp_data = emp.iloc[0]
        return {
            '编号': emp_data['编号'],
            '姓名': emp_data['姓名'],
            '到厂时间': f"{earliest['时']:02d}:{earliest['分']:02d}:{earliest['秒']:02d}"
        }

    def sort_by_birth_date(self, emp_df, ascending=True, female_only=False):
        """按出生日期排序"""
        df = emp_df.copy()

        if female_only:
            df = df[df['性别'] == '女']

        if df.empty:
            return pd.DataFrame()

        df = df.sort_values('出生日期', ascending=ascending)
        return df[['编号', '姓名', '性别', '出生日期', '职务级别', '所在部门']]
