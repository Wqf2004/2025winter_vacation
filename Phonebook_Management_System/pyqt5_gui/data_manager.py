"""
电话簿管理系统 - 数据管理模块
"""

import os


class Contact:
    """联系人数据类"""

    def __init__(self, contact_id=0, name="", work_unit="", phone="", email=""):
        self.id = contact_id
        self.name = name
        self.work_unit = work_unit
        self.phone = phone
        self.email = email

    def to_string(self):
        """转换为字符串"""
        return f"{self.id}|{self.name}|{self.work_unit}|{self.phone}|{self.email}"

    @staticmethod
    def from_string(s):
        """从字符串创建联系人"""
        parts = s.strip().split('|')
        if len(parts) >= 5:
            return Contact(
                int(parts[0]),
                parts[1],
                parts[2],
                parts[3],
                parts[4]
            )
        return None


class DataManager:
    """数据管理器"""

    def __init__(self):
        self.contacts = []
        self.password_file = "../dataset/password.txt"
        self.contacts_file = "../dataset/contacts.txt"
        self.load_data()

    def load_data(self):
        """加载数据"""
        self.contacts = []

        # 加载联系人数据
        if os.path.exists(self.contacts_file):
            try:
                with open(self.contacts_file, 'r', encoding='gbk') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            contact = Contact.from_string(line)
                            if contact:
                                self.contacts.append(contact)
            except Exception as e:
                print(f"加载联系人数据失败: {e}")

    def save_data(self):
        """保存数据"""
        try:
            # 保存联系人数据
            with open(self.contacts_file, 'w', encoding='gbk') as f:
                for contact in self.contacts:
                    f.write(contact.to_string() + '\n')
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

    def add_contact(self, contact):
        """添加联系人"""
        # 生成新ID
        max_id = 0
        for c in self.contacts:
            if c.id > max_id:
                max_id = c.id
        contact.id = max_id + 1

        # 检查电话号码是否重复
        for c in self.contacts:
            if c.phone == contact.phone:
                return False, "该电话号码已存在！"

        self.contacts.append(contact)
        return True, "添加成功"

    def delete_contact(self, contact_id):
        """删除联系人"""
        for i, c in enumerate(self.contacts):
            if c.id == contact_id:
                self.contacts.pop(i)
                return True, "删除成功"
        return False, "联系人不存在"

    def update_contact(self, contact):
        """更新联系人"""
        for i, c in enumerate(self.contacts):
            if c.id == contact.id:
                # 检查电话号码是否与其他联系人重复
                for j, other in enumerate(self.contacts):
                    if j != i and other.phone == contact.phone:
                        return False, "该电话号码已存在！"
                self.contacts[i] = contact
                return True, "更新成功"
        return False, "联系人不存在"

    def search_contacts(self, keyword, field='name'):
        """搜索联系人"""
        results = []
        keyword = keyword.lower()
        for c in self.contacts:
            if field == 'name':
                if keyword in c.name.lower():
                    results.append(c)
            elif field == 'phone':
                if keyword in c.phone:
                    results.append(c)
        return results

    def get_contacts(self):
        """获取所有联系人"""
        return self.contacts

    def sort_contacts(self, field='name'):
        """排序联系人"""
        if field == 'name':
            self.contacts.sort(key=lambda c: c.name)
        elif field == 'phone':
            self.contacts.sort(key=lambda c: c.phone)

    @staticmethod
    def is_valid_phone(phone):
        """验证电话号码"""
        phone = phone.replace('-', '').replace(' ', '')
        if len(phone) < 7 or len(phone) > 15:
            return False
        return phone.isdigit()

    @staticmethod
    def is_valid_email(email):
        """验证E-mail"""
        if len(email) < 5 or '@' not in email:
            return False
        parts = email.split('@')
        if len(parts) != 2 or '.' not in parts[1]:
            return False
        return True
