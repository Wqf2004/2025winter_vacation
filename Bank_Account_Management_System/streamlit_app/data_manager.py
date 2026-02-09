"""
数据管理模块
"""
import os


class DataManager:
    """数据管理类"""

    def __init__(self, base_dir):
        self.base_dir = base_dir

    def read_password(self):
        """读取密码"""
        password_file = os.path.join(self.base_dir, 'dataset', 'password.txt')
        try:
            with open(password_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            return None

    def verify_password(self, input_password):
        """验证密码"""
        stored_password = self.read_password()
        return input_password == stored_password

    def read_accounts(self):
        """读取账户数据"""
        basic_file = os.path.join(self.base_dir, 'dataset', 'AccountBasic.txt')
        balance_file = os.path.join(self.base_dir, 'dataset', 'AccountBalance.txt')
        accounts = []

        try:
            with open(basic_file, 'r', encoding='gb2312') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split('|')
                    if len(parts) >= 4:
                        accounts.append({
                            'account_no': int(parts[0]),
                            'name': parts[1],
                            'id_card': parts[2],
                            'create_date': parts[3],
                            'balance': 0.0
                        })

            with open(balance_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split('|')
                    if len(parts) >= 2:
                        account_no = int(parts[0])
                        for acc in accounts:
                            if acc['account_no'] == account_no:
                                acc['balance'] = float(parts[1])
                                break

            return accounts
        except Exception as e:
            return []

    def save_accounts(self, accounts):
        """保存账户数据"""
        basic_file = os.path.join(self.base_dir, 'dataset', 'AccountBasic.txt')
        balance_file = os.path.join(self.base_dir, 'dataset', 'AccountBalance.txt')

        try:
            with open(basic_file, 'w', encoding='gb2312') as f:
                for acc in accounts:
                    if acc['account_no'] != -1:
                        f.write(f"{acc['account_no']}|{acc['name']}|{acc['id_card']}|{acc['create_date']}\n")

            with open(balance_file, 'w', encoding='utf-8') as f:
                for acc in accounts:
                    if acc['account_no'] != -1:
                        f.write(f"{acc['account_no']}|{acc['balance']:.2f}\n")

            return True
        except Exception as e:
            return False

    def get_next_account_no(self, accounts):
        """获取下一个账号"""
        max_no = 10000
        for acc in accounts:
            if acc['account_no'] > max_no:
                max_no = acc['account_no']
        return max_no + 1
