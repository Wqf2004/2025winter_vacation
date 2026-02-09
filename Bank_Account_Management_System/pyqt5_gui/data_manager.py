"""
数据管理模块
"""
import os
import hashlib


class AccountBasic:
    """账户基本信息类"""

    def __init__(self, account_no, name, id_card, create_date):
        self.account_no = account_no
        self.name = name
        self.id_card = id_card
        self.create_date = create_date


class AccountBalance:
    """账户余额类"""

    def __init__(self, account_no, balance):
        self.account_no = account_no
        self.balance = balance


class DataManager:
    """数据管理类"""

    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.basics = []
        self.balances = []
        self.next_account_no = 10001

    def read_password(self):
        """读取密码"""
        password_file = os.path.join(self.base_dir, 'dataset', 'password.txt')
        try:
            with open(password_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            print(f'读取密码文件失败：{e}')
            return None

    def verify_password(self, input_password):
        """验证密码"""
        stored_password = self.read_password()
        return input_password == stored_password

    def read_account_basics(self):
        """读取账户基本信息"""
        basic_file = os.path.join(self.base_dir, 'dataset', 'AccountBasic.txt')
        basics = []

        try:
            with open(basic_file, 'r', encoding='gb2312') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split('|')
                    if len(parts) >= 4:
                        account_no = int(parts[0])
                        if account_no >= self.next_account_no:
                            self.next_account_no = account_no + 1

                        basic = AccountBasic(
                            account_no,
                            parts[1],
                            parts[2],
                            parts[3]
                        )
                        basics.append(basic)
        except Exception as e:
            print(f'读取账户基本信息失败：{e}')

        return basics

    def read_account_balances(self):
        """读取账户余额"""
        balance_file = os.path.join(self.base_dir, 'dataset', 'AccountBalance.txt')
        balances = []

        try:
            with open(balance_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split('|')
                    if len(parts) >= 2:
                        balance = AccountBalance(
                            int(parts[0]),
                            float(parts[1])
                        )
                        balances.append(balance)
        except Exception as e:
            print(f'读取账户余额失败：{e}')

        return balances

    def save_account_basics(self, basics):
        """保存账户基本信息"""
        basic_file = os.path.join(self.base_dir, 'dataset', 'AccountBasic.txt')

        try:
            with open(basic_file, 'w', encoding='gb2312') as f:
                for basic in basics:
                    if basic.account_no != -1:
                        f.write(f'{basic.account_no}|{basic.name}|{basic.id_card}|{basic.create_date}\n')
            return True
        except Exception as e:
            print(f'保存账户基本信息失败：{e}')
            return False

    def save_account_balances(self, balances):
        """保存账户余额"""
        balance_file = os.path.join(self.base_dir, 'dataset', 'AccountBalance.txt')

        try:
            with open(balance_file, 'w', encoding='utf-8') as f:
                for balance in balances:
                    if balance.account_no != -1:
                        f.write(f'{balance.account_no}|{balance.balance:.2f}\n')
            return True
        except Exception as e:
            print(f'保存账户余额失败：{e}')
            return False

    def get_account_basic_by_no(self, basics, account_no):
        """根据账号获取基本信息"""
        for basic in basics:
            if basic.account_no == account_no:
                return basic
        return None

    def get_account_balance_by_no(self, balances, account_no):
        """根据账号获取余额"""
        for balance in balances:
            if balance.account_no == account_no:
                return balance
        return None

    def validate_id_card(self, id_card):
        """验证身份证号"""
        if len(id_card) != 18:
            return False

        # 检查前17位是否为数字
        for i in range(17):
            if not id_card[i].isdigit():
                return False

        # 检查第18位是否为数字或X
        if not id_card[17].isdigit() and id_card[17].upper() != 'X':
            return False

        return True

    def validate_date(self, date):
        """验证日期格式"""
        if len(date) != 10:
            return False

        if date[4] != '-' or date[7] != '-':
            return False

        try:
            year = int(date[0:4])
            month = int(date[5:7])
            day = int(date[8:10])

            # 检查年份范围
            if year < 1900 or year > 2100:
                return False

            # 检查月份范围
            if month < 1 or month > 12:
                return False

            # 检查日期范围
            if day < 1 or day > 31:
                return False

            return True
        except ValueError:
            return False

    def get_warning_accounts(self, basics, balances):
        """获取预警账户（借款超过5万元）"""
        warnings = []

        for i, basic in enumerate(basics):
            if basic.account_no == -1:
                continue

            balance = self.get_account_balance_by_no(balances, basic.account_no)
            if balance and balance.balance < -50000:
                warnings.append((basic, balance))

        return warnings

    def get_max_borrower(self, basics, balances):
        """获取最大借款账户"""
        max_borrower = None
        max_borrow = 0

        for basic in basics:
            if basic.account_no == -1:
                continue

            balance = self.get_account_balance_by_no(balances, basic.account_no)
            if balance and balance.balance < 0:
                if balance.balance < max_borrow:
                    max_borrow = balance.balance
                    max_borrower = (basic, balance)

        return max_borrower

    def get_max_depositor(self, basics, balances):
        """获取最大存款账户"""
        max_depositor = None
        max_deposit = 0

        for basic in basics:
            if basic.account_no == -1:
                continue

            balance = self.get_account_balance_by_no(balances, basic.account_no)
            if balance and balance.balance > 0:
                if balance.balance > max_deposit:
                    max_deposit = balance.balance
                    max_depositor = (basic, balance)

        return max_depositor
