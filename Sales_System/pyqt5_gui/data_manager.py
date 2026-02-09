"""
销售系统 - 数据管理模块（PyQt5版）
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

    def read_users(self):
        """读取用户数据"""
        users_file = os.path.join(self.base_dir, 'dataset', 'users.txt')
        users = []

        try:
            with open(users_file, 'r', encoding='gbk') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    parts = line.split('|')
                    # 处理行号格式
                    if len(parts) >= 5 and parts[0].isdigit() and len(parts[0]) <= 3:
                        parts = parts[1:]

                    if len(parts) >= 4:
                        users.append({
                            'id': int(parts[0]),
                            'username': parts[1],
                            'password': parts[2],
                            'role': int(parts[3])
                        })
            return users
        except FileNotFoundError:
            print(f'用户文件不存在: {users_file}')
            return []
        except Exception as e:
            print(f'读取用户文件错误: {e}')
            return []

    def save_users(self, users):
        """保存用户数据"""
        users_file = os.path.join(self.base_dir, 'dataset', 'users.txt')
        try:
            with open(users_file, 'w', encoding='gbk') as f:
                for user in users:
                    f.write(f"{user['id']}|{user['username']}|{user['password']}|{user['role']}\n")
            return True
        except Exception as e:
            return False

    def read_products(self):
        """读取商品数据"""
        products_file = os.path.join(self.base_dir, 'dataset', 'products.txt')
        products = []

        try:
            with open(products_file, 'r', encoding='gbk') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    # 处理行号格式（如 1|1001|...）
                    parts = line.split('|')
                    # 如果第一个部分是数字且长度较短，可能是行号，跳过
                    if len(parts) >= 5 and parts[0].isdigit() and len(parts[0]) <= 3:
                        parts = parts[1:]  # 跳过行号

                    if len(parts) >= 4:
                        products.append({
                            'id': int(parts[0]),
                            'name': parts[1],
                            'price': float(parts[2]),
                            'stock': int(parts[3])
                        })
            return products
        except FileNotFoundError:
            print(f'商品文件不存在: {products_file}')
            return []
        except Exception as e:
            print(f'读取商品文件错误: {e}')
            return []

    def save_products(self, products):
        """保存商品数据"""
        products_file = os.path.join(self.base_dir, 'dataset', 'products.txt')
        try:
            with open(products_file, 'w', encoding='gbk') as f:
                for product in products:
                    f.write(f"{product['id']}|{product['name']}|{product['price']:.2f}|{product['stock']}\n")
            return True
        except Exception as e:
            return False

    def read_sales(self):
        """读取销售数据"""
        sales_file = os.path.join(self.base_dir, 'dataset', 'sales.txt')
        sales = []

        try:
            with open(sales_file, 'r', encoding='gbk') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    parts = line.split('|')
                    # 处理行号格式
                    if len(parts) >= 9 and parts[0].isdigit() and len(parts[0]) <= 3:
                        parts = parts[1:]

                    if len(parts) >= 8:
                        sales.append({
                            'id': int(parts[0]),
                            'product_id': int(parts[1]),
                            'product_name': parts[2],
                            'quantity': int(parts[3]),
                            'unit_price': float(parts[4]),
                            'total_amount': float(parts[5]),
                            'date': parts[6],
                            'seller_id': int(parts[7])
                        })
            return sales
        except FileNotFoundError:
            print(f'销售文件不存在: {sales_file}')
            return []
        except Exception as e:
            print(f'读取销售文件错误: {e}')
            return []

    def save_sales(self, sales):
        """保存销售数据"""
        sales_file = os.path.join(self.base_dir, 'dataset', 'sales.txt')
        try:
            with open(sales_file, 'w', encoding='gbk') as f:
                for sale in sales:
                    f.write(f"{sale['id']}|{sale['product_id']}|{sale['product_name']}|"
                           f"{sale['quantity']}|{sale['unit_price']:.2f}|{sale['total_amount']:.2f}|"
                           f"{sale['date']}|{sale['seller_id']}\n")
            return True
        except Exception as e:
            return False

    def verify_user(self, username, password):
        """验证用户"""
        users = self.read_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                return user
        return None

    def get_next_id(self, items, id_field):
        """获取下一个ID"""
        if not items:
            return 1001 if id_field == 'product_id' else 1
        return max(item[id_field] for item in items) + 1
