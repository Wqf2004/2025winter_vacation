"""
期末成绩管理系统 - 数据管理模块
"""
import os


class DataManager:
    """数据管理类"""

    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.dataset_dir = os.path.join(base_dir, 'dataset')
        self.basic_file = os.path.join(self.dataset_dir, 'StudentBasic.txt')
        self.grade_file = os.path.join(self.dataset_dir, 'StudentGrade.txt')
        self.password_file = os.path.join(self.dataset_dir, 'password.txt')

    def read_student_basics_df(self):
        """读取学生基本情况为DataFrame"""
        import pandas as pd

        if not os.path.exists(self.basic_file):
            return pd.DataFrame(columns=['学号', '姓名', '性别', '出生日期', '入学日期', '受奖次数', '补考次数', '留级次数'])

        df = pd.read_csv(self.basic_file, sep=' ', encoding='gb2312', skipinitialspace=True,
                         names=['学号', '姓名', '性别', '出生日期', '入学日期', '受奖次数', '补考次数', '留级次数'])
        df['学号'] = df['学号'].astype(str)
        return df

    def read_student_grades_df(self):
        """读取学生成绩为DataFrame"""
        import pandas as pd

        if not os.path.exists(self.grade_file):
            return pd.DataFrame(columns=['学号', '计算机', '高等数学', '外语', '体育', '平均分'])

        df = pd.read_csv(self.grade_file, sep=' ', encoding='utf-8', skipinitialspace=True,
                         names=['学号', '计算机', '高等数学', '外语', '体育', '平均分'], dtype={'学号': str})
        return df

    def save_student_grade_df(self, df):
        """保存学生成绩"""
        import pandas as pd
        df.to_csv(self.grade_file, sep=' ', index=False, header=False, encoding='utf-8')

    def verify_password(self, password):
        """验证密码"""
        if not os.path.exists(self.password_file):
            return False

        with open(self.password_file, 'r', encoding='gbk') as f:
            stored_password = f.read().strip()
            return password == stored_password

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
