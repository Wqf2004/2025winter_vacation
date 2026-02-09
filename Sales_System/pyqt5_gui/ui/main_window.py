"""
主窗口
"""
import os
from datetime import datetime
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QMessageBox, QTabWidget,
                             QDialog, QFormLayout, QSpinBox, QDoubleSpinBox,
                             QComboBox, QDateEdit, QHeaderView)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont


class PasswordTab(QWidget):
    """密码修改标签页"""

    def __init__(self, data_manager, current_user, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.current_user = current_user
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.old_password_input = QLineEdit()
        self.old_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow('旧密码：', self.old_password_input)
        form_layout.addRow('新密码：', self.new_password_input)
        form_layout.addRow('确认密码：', self.confirm_password_input)

        layout.addLayout(form_layout)

        save_btn = QPushButton('修改密码')
        save_btn.clicked.connect(self.modify_password)
        layout.addWidget(save_btn)

        layout.addStretch()
        self.setLayout(layout)

    def modify_password(self):
        old_password = self.old_password_input.text().strip()
        new_password = self.new_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        if not old_password or not new_password:
            QMessageBox.warning(self, '警告', '密码不能为空！')
            return

        users = self.data_manager.read_users()
        user = self.data_manager.verify_user(
            self.current_user['username'], old_password
        )
        if not user:
            QMessageBox.warning(self, '错误', '旧密码错误！')
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, '错误', '两次密码不一致！')
            return

        for u in users:
            if u['id'] == self.current_user['id']:
                u['password'] = new_password
                break

        self.data_manager.save_users(users)
        self.current_user['password'] = new_password
        QMessageBox.information(self, '成功', '密码修改成功！')

        self.old_password_input.clear()
        self.new_password_input.clear()
        self.confirm_password_input.clear()


class UserManageTab(QWidget):
    """用户管理标签页"""

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.users = []
        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        layout = QVBoxLayout()

        btn_layout = QHBoxLayout()
        add_btn = QPushButton('添加用户')
        add_btn.clicked.connect(lambda: self.user_dialog())
        edit_btn = QPushButton('修改用户')
        edit_btn.clicked.connect(lambda: self.user_dialog(edit=True))
        del_btn = QPushButton('删除用户')
        del_btn.clicked.connect(self.delete_user)
        refresh_btn = QPushButton('刷新')
        refresh_btn.clicked.connect(self.refresh_table)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(del_btn)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', '用户名', '角色', ''])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def refresh_table(self):
        self.users = self.data_manager.read_users()
        role_names = {1: '管理员', 2: '店长', 3: '销售员'}
        self.table.setRowCount(len(self.users))

        for row, user in enumerate(self.users):
            self.table.setItem(row, 0, QTableWidgetItem(str(user['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(user['username']))
            self.table.setItem(row, 2, QTableWidgetItem(
                role_names.get(user['role'], '未知')
            ))

    def user_dialog(self, edit=False):
        dialog = QDialog(self)
        dialog.setWindowTitle('修改用户' if edit else '添加用户')
        dialog.setFixedSize(300, 200)

        layout = QFormLayout()

        if edit:
            user_id_input = QSpinBox()
            user_id_input.setRange(1, 9999)
            layout.addRow('用户ID：', user_id_input)

        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        role_combo = QComboBox()
        role_combo.addItems(['管理员', '店长', '销售员'])

        layout.addRow('用户名：', username_input)
        layout.addRow('密码：', password_input)
        layout.addRow('角色：', role_combo)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton('保存')
        cancel_btn = QPushButton('取消')

        def save_user():
            username = username_input.text().strip()
            password = password_input.text().strip()
            role = role_combo.currentIndex() + 1

            if not username or not password:
                QMessageBox.warning(dialog, '警告', '用户名和密码不能为空！')
                return

            if edit:
                user_id = user_id_input.value()
                for user in self.users:
                    if user['id'] == user_id:
                        user['username'] = username
                        user['password'] = password
                        user['role'] = role
                        break
            else:
                new_id = max(u['id'] for u in self.users) + 1 if self.users else 1
                self.users.append({
                    'id': new_id,
                    'username': username,
                    'password': password,
                    'role': role
                })

            self.data_manager.save_users(self.users)
            self.refresh_table()
            dialog.accept()

        save_btn.clicked.connect(save_user)
        cancel_btn.clicked.connect(dialog.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def delete_user(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, '警告', '请先选择要删除的用户！')
            return

        user_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(
            self, '确认', '确定要删除该用户吗？',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.users = [u for u in self.users if u['id'] != user_id]
            self.data_manager.save_users(self.users)
            self.refresh_table()


class ProductManageTab(QWidget):
    """商品管理标签页"""

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.products = []
        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        layout = QVBoxLayout()

        btn_layout = QHBoxLayout()
        add_btn = QPushButton('添加商品')
        add_btn.clicked.connect(lambda: self.product_dialog())
        edit_btn = QPushButton('修改商品')
        edit_btn.clicked.connect(lambda: self.product_dialog(edit=True))
        del_btn = QPushButton('删除商品')
        del_btn.clicked.connect(self.delete_product)
        refresh_btn = QPushButton('刷新')
        refresh_btn.clicked.connect(self.refresh_table)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(del_btn)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ['商品ID', '商品名称', '单价', '库存']
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def refresh_table(self):
        self.products = self.data_manager.read_products()
        self.table.setRowCount(len(self.products))

        for row, product in enumerate(self.products):
            self.table.setItem(row, 0, QTableWidgetItem(str(product['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(product['name']))
            self.table.setItem(row, 2, QTableWidgetItem(
                f"{product['price']:.2f}"
            ))
            self.table.setItem(row, 3, QTableWidgetItem(str(product['stock'])))

    def product_dialog(self, edit=False):
        dialog = QDialog(self)
        dialog.setWindowTitle('修改商品' if edit else '添加商品')
        dialog.setFixedSize(350, 250)

        layout = QFormLayout()

        if edit:
            product_id_input = QSpinBox()
            product_id_input.setRange(1000, 9999)
            layout.addRow('商品ID：', product_id_input)

        name_input = QLineEdit()
        price_input = QDoubleSpinBox()
        price_input.setRange(0.01, 999999.99)
        price_input.setDecimals(2)
        price_input.setValue(0.00)
        stock_input = QSpinBox()
        stock_input.setRange(0, 99999)

        layout.addRow('商品名称：', name_input)
        layout.addRow('单价：', price_input)
        layout.addRow('库存：', stock_input)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton('保存')
        cancel_btn = QPushButton('取消')

        def save_product():
            name = name_input.text().strip()
            price = price_input.value()
            stock = stock_input.value()

            if not name:
                QMessageBox.warning(dialog, '警告', '商品名称不能为空！')
                return

            if edit:
                product_id = product_id_input.value()
                for product in self.products:
                    if product['id'] == product_id:
                        product['name'] = name
                        product['price'] = price
                        product['stock'] = stock
                        break
            else:
                new_id = max(p['id'] for p in self.products) + 1 if self.products else 1001
                self.products.append({
                    'id': new_id,
                    'name': name,
                    'price': price,
                    'stock': stock
                })

            self.data_manager.save_products(self.products)
            self.refresh_table()
            dialog.accept()

        save_btn.clicked.connect(save_product)
        cancel_btn.clicked.connect(dialog.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def delete_product(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, '警告', '请先选择要删除的商品！')
            return

        product_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(
            self, '确认', '确定要删除该商品吗？',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.products = [p for p in self.products if p['id'] != product_id]
            self.data_manager.save_products(self.products)
            self.refresh_table()


class ProductBrowseTab(QWidget):
    """商品浏览标签页"""

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.products = []
        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ['商品ID', '商品名称', '单价', '库存']
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        refresh_btn = QPushButton('刷新')
        refresh_btn.clicked.connect(self.refresh_table)
        layout.addWidget(refresh_btn)

        self.setLayout(layout)

    def refresh_table(self):
        self.products = self.data_manager.read_products()
        self.table.setRowCount(len(self.products))

        for row, product in enumerate(self.products):
            self.table.setItem(row, 0, QTableWidgetItem(str(product['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(product['name']))
            self.table.setItem(row, 2, QTableWidgetItem(
                f"{product['price']:.2f}"
            ))
            self.table.setItem(row, 3, QTableWidgetItem(str(product['stock'])))


class SellTab(QWidget):
    """销售商品标签页"""

    def __init__(self, data_manager, current_user, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.current_user = current_user
        self.products = []
        self.setup_ui()
        self.refresh_tab()

    def setup_ui(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.product_combo = QComboBox()
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 99999)
        self.quantity_input.setValue(1)

        form_layout.addRow('选择商品：', self.product_combo)
        form_layout.addRow('销售数量：', self.quantity_input)

        layout.addLayout(form_layout)

        sell_btn = QPushButton('确认销售')
        sell_btn.clicked.connect(self.sell_product)
        layout.addWidget(sell_btn)

        self.setLayout(layout)

    def refresh_tab(self):
        self.products = self.data_manager.read_products()
        self.product_combo.clear()

        for product in self.products:
            self.product_combo.addItem(
                f"{product['id']} - {product['name']} (库存: {product['stock']})",
                product
            )

    def sell_product(self):
        product = self.product_combo.currentData()
        quantity = self.quantity_input.value()

        if quantity > product['stock']:
            QMessageBox.warning(self, '错误', '库存不足！')
            return

        product['stock'] -= quantity
        self.data_manager.save_products(self.products)

        sales = self.data_manager.read_sales()
        new_id = len(sales) + 1
        today = datetime.now().strftime('%Y-%m-%d')

        sales.append({
            'id': new_id,
            'product_id': product['id'],
            'product_name': product['name'],
            'quantity': quantity,
            'unit_price': product['price'],
            'total_amount': quantity * product['price'],
            'date': today,
            'seller_id': self.current_user['id']
        })

        self.data_manager.save_sales(sales)

        QMessageBox.information(
            self, '成功',
            f'销售成功！总金额：{quantity * product["price"]:.2f} 元'
        )

        self.refresh_tab()


class DailyReportTab(QWidget):
    """日报表标签页"""

    def __init__(self, data_manager, current_user, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.current_user = current_user
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        date_layout = QHBoxLayout()
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat('yyyy-MM-dd')

        query_btn = QPushButton('查询')
        query_btn.clicked.connect(self.query_report)

        date_layout.addWidget(QLabel('日期：'))
        date_layout.addWidget(self.date_input)
        date_layout.addWidget(query_btn)
        date_layout.addStretch()
        layout.addLayout(date_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ['ID', '商品名称', '数量', '单价', '总金额', '销售员']
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.total_label = QLabel('当日总金额：0.00 元')
        layout.addWidget(self.total_label)

        self.setLayout(layout)

    def query_report(self):
        date_str = self.date_input.date().toString('yyyy-MM-dd')
        sales = self.data_manager.read_sales()
        users = self.data_manager.read_users()

        filtered_sales = []
        total_amount = 0.0

        for sale in sales:
            if sale['date'] != date_str:
                continue

            if (self.current_user['role'] == 3 and
                    sale['seller_id'] != self.current_user['id']):
                continue

            filtered_sales.append(sale)
            total_amount += sale['total_amount']

        self.table.setRowCount(len(filtered_sales))

        for row, sale in enumerate(filtered_sales):
            seller_name = '未知'
            for user in users:
                if user['id'] == sale['seller_id']:
                    seller_name = user['username']
                    break

            self.table.setItem(row, 0, QTableWidgetItem(str(sale['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(sale['product_name']))
            self.table.setItem(row, 2, QTableWidgetItem(str(sale['quantity'])))
            self.table.setItem(row, 3, QTableWidgetItem(
                f"{sale['unit_price']:.2f}"
            ))
            self.table.setItem(row, 4, QTableWidgetItem(
                f"{sale['total_amount']:.2f}"
            ))
            self.table.setItem(row, 5, QTableWidgetItem(seller_name))

        self.total_label.setText(f'当日总金额：{total_amount:.2f} 元')


class MonthlyReportTab(QWidget):
    """月报表标签页"""

    def __init__(self, data_manager, current_user, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.current_user = current_user
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        month_layout = QHBoxLayout()
        self.year_input = QSpinBox()
        self.year_input.setRange(2020, 2099)
        self.year_input.setValue(QDate.currentDate().year())
        self.month_input = QSpinBox()
        self.month_input.setRange(1, 12)
        self.month_input.setValue(QDate.currentDate().month())

        query_btn = QPushButton('查询')
        query_btn.clicked.connect(self.query_report)

        month_layout.addWidget(QLabel('年份：'))
        month_layout.addWidget(self.year_input)
        month_layout.addWidget(QLabel('月份：'))
        month_layout.addWidget(self.month_input)
        month_layout.addWidget(query_btn)
        month_layout.addStretch()
        layout.addLayout(month_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ['ID', '商品名称', '数量', '单价', '总金额', '销售日期', '销售员']
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.total_label = QLabel('当月总金额：0.00 元')
        layout.addWidget(self.total_label)

        self.setLayout(layout)

    def query_report(self):
        year = self.year_input.value()
        month = self.month_input.value()
        month_str = f'{year:04d}-{month:02d}'

        sales = self.data_manager.read_sales()
        users = self.data_manager.read_users()

        filtered_sales = []
        total_amount = 0.0

        for sale in sales:
            if not sale['date'].startswith(month_str):
                continue

            if (self.current_user['role'] == 3 and
                    sale['seller_id'] != self.current_user['id']):
                continue

            filtered_sales.append(sale)
            total_amount += sale['total_amount']

        self.table.setRowCount(len(filtered_sales))

        for row, sale in enumerate(filtered_sales):
            seller_name = '未知'
            for user in users:
                if user['id'] == sale['seller_id']:
                    seller_name = user['username']
                    break

            self.table.setItem(row, 0, QTableWidgetItem(str(sale['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(sale['product_name']))
            self.table.setItem(row, 2, QTableWidgetItem(str(sale['quantity'])))
            self.table.setItem(row, 3, QTableWidgetItem(
                f"{sale['unit_price']:.2f}"
            ))
            self.table.setItem(row, 4, QTableWidgetItem(
                f"{sale['total_amount']:.2f}"
            ))
            self.table.setItem(row, 5, QTableWidgetItem(sale['date']))
            self.table.setItem(row, 6, QTableWidgetItem(seller_name))

        self.total_label.setText(f'当月总金额：{total_amount:.2f} 元')


class ProductSalesTab(QWidget):
    """商品销售报表标签页"""

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ['商品ID', '商品名称', '销售数量', '销售金额']
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        refresh_btn = QPushButton('刷新')
        refresh_btn.clicked.connect(self.refresh_table)
        layout.addWidget(refresh_btn)

        self.setLayout(layout)

    def refresh_table(self):
        sales = self.data_manager.read_sales()
        products = self.data_manager.read_products()

        stats = {}
        for product in products:
            stats[product['id']] = {'name': product['name'], 'quantity': 0}

        for sale in sales:
            if sale['product_id'] in stats:
                stats[sale['product_id']]['quantity'] += sale['quantity']

        filtered_stats = [
            (pid, data) for pid, data in stats.items() if data['quantity'] > 0
        ]

        self.table.setRowCount(len(filtered_stats))

        for row, (pid, data) in enumerate(filtered_stats):
            product = next(p for p in products if p['id'] == pid)
            amount = data['quantity'] * product['price']

            self.table.setItem(row, 0, QTableWidgetItem(str(pid)))
            self.table.setItem(row, 1, QTableWidgetItem(data['name']))
            self.table.setItem(row, 2, QTableWidgetItem(str(data['quantity'])))
            self.table.setItem(row, 3, QTableWidgetItem(f'{amount:.2f}'))


class SellerPerformanceTab(QWidget):
    """销售员业绩报表标签页"""

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ['销售员ID', '销售员姓名', '销售单数', '销售金额']
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        refresh_btn = QPushButton('刷新')
        refresh_btn.clicked.connect(self.refresh_table)
        layout.addWidget(refresh_btn)

        self.setLayout(layout)

    def refresh_table(self):
        sales = self.data_manager.read_sales()
        users = self.data_manager.read_users()

        stats = {}
        for user in users:
            if user['role'] == 3:
                stats[user['id']] = {
                    'name': user['username'],
                    'count': 0,
                    'amount': 0.0
                }

        for sale in sales:
            if sale['seller_id'] in stats:
                stats[sale['seller_id']]['count'] += 1
                stats[sale['seller_id']]['amount'] += sale['total_amount']

        filtered_stats = [
            (uid, data) for uid, data in stats.items() if data['count'] > 0
        ]

        self.table.setRowCount(len(filtered_stats))

        for row, (uid, data) in enumerate(filtered_stats):
            self.table.setItem(row, 0, QTableWidgetItem(str(uid)))
            self.table.setItem(row, 1, QTableWidgetItem(data['name']))
            self.table.setItem(row, 2, QTableWidgetItem(str(data['count'])))
            self.table.setItem(row, 3, QTableWidgetItem(f'{data["amount"]:.2f}'))


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self, data_manager, current_user):
        super().__init__()
        self.data_manager = data_manager
        self.current_user = current_user
        self.setup_ui()

    def setup_ui(self):
        """初始化UI"""
        role_names = {1: '管理员', 2: '店长', 3: '销售员'}
        role_name = role_names.get(self.current_user['role'], '用户')

        self.setWindowTitle(f'销售系统 - {role_name}')
        self.setGeometry(100, 100, 1000, 700)

        self.tab_widget = QTabWidget()

        self.add_tab('修改密码', PasswordTab(self.data_manager, self.current_user))

        if self.current_user['role'] == 1:
            self.add_tab('用户管理', UserManageTab(self.data_manager))

        if self.current_user['role'] in [1, 2]:
            self.add_tab('商品管理', ProductManageTab(self.data_manager))
            self.add_tab('商品销售报表', ProductSalesTab(self.data_manager))
            self.add_tab('销售员业绩报表', SellerPerformanceTab(self.data_manager))

        if self.current_user['role'] == 3:
            self.add_tab('商品浏览', ProductBrowseTab(self.data_manager))
            self.add_tab('销售商品', SellTab(self.data_manager, self.current_user))

        self.add_tab('日报表', DailyReportTab(self.data_manager, self.current_user))
        self.add_tab('月报表', MonthlyReportTab(self.data_manager, self.current_user))

        self.setCentralWidget(self.tab_widget)

    def add_tab(self, title, widget):
        self.tab_widget.addTab(widget, title)
