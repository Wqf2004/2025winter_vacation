"""
主窗口
"""
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                             QStackedWidget, QPushButton, QLabel, QTableWidget,
                             QTableWidgetItem, QMessageBox, QLineEdit)
from PyQt5.QtCore import Qt
from data_manager import DataManager, AccountBasic, AccountBalance


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.data_manager = DataManager(base_dir)
        self.basics = []
        self.balances = []
        self.init_ui()
        self.load_data()
        self.check_warnings()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('银行账目管理系统')
        self.setGeometry(100, 100, 1000, 700)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)

        # 侧边栏
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet('''
            QWidget {
                background-color: #2C3E50;
                color: white;
            }
        ''')
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        title_label = QLabel('银行账目管理系统')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 16px; font-weight: bold; padding: 20px;')
        sidebar_layout.addWidget(title_label)

        btn_style = '''
            QPushButton {
                background-color: transparent;
                color: white;
                text-align: left;
                padding: 12px 20px;
                font-size: 13px;
                border: none;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
        '''

        self.btn_open = QPushButton('开户')
        self.btn_open.setStyleSheet(btn_style)
        self.btn_open.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        sidebar_layout.addWidget(self.btn_open)

        self.btn_borrow = QPushButton('借款')
        self.btn_borrow.setStyleSheet(btn_style)
        self.btn_borrow.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        sidebar_layout.addWidget(self.btn_borrow)

        self.btn_repay = QPushButton('还款')
        self.btn_repay.setStyleSheet(btn_style)
        self.btn_repay.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        sidebar_layout.addWidget(self.btn_repay)

        self.btn_deposit = QPushButton('存款')
        self.btn_deposit.setStyleSheet(btn_style)
        self.btn_deposit.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        sidebar_layout.addWidget(self.btn_deposit)

        self.btn_query = QPushButton('查询账户')
        self.btn_query.setStyleSheet(btn_style)
        self.btn_query.clicked.connect(lambda: self.stack.setCurrentIndex(4))
        sidebar_layout.addWidget(self.btn_query)

        self.btn_max_borrow = QPushButton('最大借款账户')
        self.btn_max_borrow.setStyleSheet(btn_style)
        self.btn_max_borrow.clicked.connect(lambda: [self.stack.setCurrentIndex(5), self.show_max_borrower()])
        sidebar_layout.addWidget(self.btn_max_borrow)

        self.btn_max_deposit = QPushButton('最大存款账户')
        self.btn_max_deposit.setStyleSheet(btn_style)
        self.btn_max_deposit.clicked.connect(lambda: [self.stack.setCurrentIndex(6), self.show_max_depositor()])
        sidebar_layout.addWidget(self.btn_max_deposit)

        self.btn_sort_borrow = QPushButton('按借款余额排序')
        self.btn_sort_borrow.setStyleSheet(btn_style)
        self.btn_sort_borrow.clicked.connect(lambda: [self.stack.setCurrentIndex(7), self.sort_by_borrow()])
        sidebar_layout.addWidget(self.btn_sort_borrow)

        self.btn_sort_deposit = QPushButton('按存款余额排序')
        self.btn_sort_deposit.setStyleSheet(btn_style)
        self.btn_sort_deposit.clicked.connect(lambda: [self.stack.setCurrentIndex(8), self.sort_by_deposit()])
        sidebar_layout.addWidget(self.btn_sort_deposit)

        self.btn_sort_date = QPushButton('按开户日期排序')
        self.btn_sort_date.setStyleSheet(btn_style)
        self.btn_sort_date.clicked.connect(lambda: [self.stack.setCurrentIndex(9), self.sort_by_date()])
        sidebar_layout.addWidget(self.btn_sort_date)

        self.btn_delete = QPushButton('清户')
        self.btn_delete.setStyleSheet(btn_style)
        self.btn_delete.clicked.connect(lambda: self.stack.setCurrentIndex(10))
        sidebar_layout.addWidget(self.btn_delete)

        self.btn_compact = QPushButton('文件紧缩')
        self.btn_compact.setStyleSheet(btn_style)
        self.btn_compact.clicked.connect(lambda: [self.stack.setCurrentIndex(11), self.show_compact_info()])
        sidebar_layout.addWidget(self.btn_compact)

        self.btn_statistics = QPushButton('统计信息')
        self.btn_statistics.setStyleSheet(btn_style)
        self.btn_statistics.clicked.connect(lambda: [self.stack.setCurrentIndex(12), self.show_statistics()])
        sidebar_layout.addWidget(self.btn_statistics)

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # 内容区域
        self.stack = QStackedWidget()

        self.create_open_page()
        self.create_borrow_page()
        self.create_repay_page()
        self.create_deposit_page()
        self.create_query_page()
        self.create_max_borrower_page()
        self.create_max_depositor_page()
        self.create_sort_borrow_page()
        self.create_sort_deposit_page()
        self.create_sort_date_page()
        self.create_delete_page()
        self.create_compact_page()
        self.create_statistics_page()

        main_layout.addWidget(self.stack)

    def create_open_page(self):
        """创建开户页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel('开户')
        label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        layout.addWidget(label)

        self.open_name = QLineEdit()
        self.open_name.setPlaceholderText('姓名')
        self.open_name.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 5px;')
        layout.addWidget(self.open_name)

        self.open_id = QLineEdit()
        self.open_id.setPlaceholderText('身份证号')
        self.open_id.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 5px;')
        layout.addWidget(self.open_id)

        self.open_date = QLineEdit()
        self.open_date.setPlaceholderText('开户日期(YYYY-MM-DD)')
        self.open_date.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 5px;')
        layout.addWidget(self.open_date)

        self.open_amount = QLineEdit()
        self.open_amount.setPlaceholderText('开户金额')
        self.open_amount.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 10px;')
        layout.addWidget(self.open_amount)

        submit_btn = QPushButton('提交')
        submit_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        submit_btn.clicked.connect(self.open_account)
        layout.addWidget(submit_btn)

        layout.addStretch()
        self.stack.addWidget(page)

    def create_borrow_page(self):
        """创建借款页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel('借款')
        label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        layout.addWidget(label)

        self.borrow_no = QLineEdit()
        self.borrow_no.setPlaceholderText('账号')
        self.borrow_no.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 5px;')
        layout.addWidget(self.borrow_no)

        self.borrow_amount = QLineEdit()
        self.borrow_amount.setPlaceholderText('借款金额')
        self.borrow_amount.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 10px;')
        layout.addWidget(self.borrow_amount)

        submit_btn = QPushButton('提交')
        submit_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        submit_btn.clicked.connect(self.borrow_money)
        layout.addWidget(submit_btn)

        layout.addStretch()
        self.stack.addWidget(page)

    def create_repay_page(self):
        """创建还款页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel('还款')
        label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        layout.addWidget(label)

        self.repay_no = QLineEdit()
        self.repay_no.setPlaceholderText('账号')
        self.repay_no.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 5px;')
        layout.addWidget(self.repay_no)

        self.repay_amount = QLineEdit()
        self.repay_amount.setPlaceholderText('还款金额')
        self.repay_amount.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 10px;')
        layout.addWidget(self.repay_amount)

        submit_btn = QPushButton('提交')
        submit_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        submit_btn.clicked.connect(self.repay_money)
        layout.addWidget(submit_btn)

        layout.addStretch()
        self.stack.addWidget(page)

    def create_deposit_page(self):
        """创建存款页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel('存款')
        label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        layout.addWidget(label)

        self.deposit_no = QLineEdit()
        self.deposit_no.setPlaceholderText('账号')
        self.deposit_no.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 5px;')
        layout.addWidget(self.deposit_no)

        self.deposit_amount = QLineEdit()
        self.deposit_amount.setPlaceholderText('存款金额')
        self.deposit_amount.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 10px;')
        layout.addWidget(self.deposit_amount)

        submit_btn = QPushButton('提交')
        submit_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        submit_btn.clicked.connect(self.deposit_money)
        layout.addWidget(submit_btn)

        layout.addStretch()
        self.stack.addWidget(page)

    def create_query_page(self):
        """创建查询页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel('查询账户')
        label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        layout.addWidget(label)

        self.query_no = QLineEdit()
        self.query_no.setPlaceholderText('请输入账号')
        self.query_no.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 10px;')
        layout.addWidget(self.query_no)

        query_btn = QPushButton('查询')
        query_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        query_btn.clicked.connect(self.query_account)
        layout.addWidget(query_btn)

        self.query_table = QTableWidget()
        self.query_table.setStyleSheet('QTableWidget {gridline-color: #ccc; alternate-background-color: #f5f5f5; }')
        layout.addWidget(self.query_table)

        self.stack.addWidget(page)

    def create_max_borrower_page(self):
        """创建最大借款账户页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel('最大借款账户')
        label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        layout.addWidget(label)

        self.max_borrower_table = QTableWidget()
        self.max_borrower_table.setStyleSheet('QTableWidget {gridline-color: #ccc; alternate-background-color: #f5f5f5; }')
        layout.addWidget(self.max_borrower_table)

        self.stack.addWidget(page)

    def create_max_depositor_page(self):
        """创建最大存款账户页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel('最大存款账户')
        label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        layout.addWidget(label)

        self.max_depositor_table = QTableWidget()
        self.max_depositor_table.setStyleSheet('QTableWidget {gridline-color: #ccc; alternate-background-color: #f5f5f5; }')
        layout.addWidget(self.max_depositor_table)

        self.stack.addWidget(page)

    def create_sort_borrow_page(self):
        """创建按借款余额排序页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel('按借款余额排序')
        label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        layout.addWidget(label)

        self.sort_borrow_table = QTableWidget()
        self.sort_borrow_table.setStyleSheet('QTableWidget {gridline-color: #ccc; alternate-background-color: #f5f5f5; }')
        layout.addWidget(self.sort_borrow_table)

        self.stack.addWidget(page)

    def create_sort_deposit_page(self):
        """创建按存款余额排序页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel('按存款余额排序')
        label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        layout.addWidget(label)

        self.sort_deposit_table = QTableWidget()
        self.sort_deposit_table.setStyleSheet('QTableWidget {gridline-color: #ccc; alternate-background-color: #f5f5f5; }')
        layout.addWidget(self.sort_deposit_table)

        self.stack.addWidget(page)

    def create_sort_date_page(self):
        """创建按开户日期排序页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel('按开户日期排序')
        label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        layout.addWidget(label)

        self.sort_date_table = QTableWidget()
        self.sort_date_table.setStyleSheet('QTableWidget {gridline-color: #ccc; alternate-background-color: #f5f5f5; }')
        layout.addWidget(self.sort_date_table)

        self.stack.addWidget(page)

    def create_delete_page(self):
        """创建清户页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel('清户')
        label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        layout.addWidget(label)

        self.delete_no = QLineEdit()
        self.delete_no.setPlaceholderText('请输入要删除的账号')
        self.delete_no.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 10px;')
        layout.addWidget(self.delete_no)

        delete_btn = QPushButton('删除')
        delete_btn.setStyleSheet('''
            QPushButton {
                background-color: #F44336;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        ''')
        delete_btn.clicked.connect(self.delete_account)
        layout.addWidget(delete_btn)

        layout.addStretch()
        self.stack.addWidget(page)

    def create_compact_page(self):
        """创建文件紧缩页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel('文件紧缩')
        label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        layout.addWidget(label)

        self.compact_table = QTableWidget()
        self.compact_table.setStyleSheet('QTableWidget {gridline-color: #ccc; alternate-background-color: #f5f5f5; }')
        layout.addWidget(self.compact_table)

        compact_btn = QPushButton('执行文件紧缩')
        compact_btn.setStyleSheet('''
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        ''')
        compact_btn.clicked.connect(self.compact_files)
        layout.addWidget(compact_btn)

        self.stack.addWidget(page)

    def create_statistics_page(self):
        """创建统计信息页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel('统计信息')
        label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        layout.addWidget(label)

        self.statistics_table = QTableWidget()
        self.statistics_table.setStyleSheet('QTableWidget {gridline-color: #ccc; alternate-background-color: #f5f5f5; }')
        layout.addWidget(self.statistics_table)

        self.stack.addWidget(page)

    def load_data(self):
        """加载数据"""
        self.basics = self.data_manager.read_account_basics()
        self.balances = self.data_manager.read_account_balances()

    def check_warnings(self):
        """检查预警账户"""
        warnings = self.data_manager.get_warning_accounts(self.basics, self.balances)

        if warnings:
            msg = '以下账户借款超过5万元：\n\n'
            for basic, balance in warnings:
                msg += f'账号: {basic.account_no}, 姓名: {basic.name}, 借款: {-balance.balance:.2f}元\n'
            QMessageBox.warning(self, '借款预警', msg)
        else:
            QMessageBox.information(self, '提示', '无借款超额账户。')

    def open_account(self):
        """开户"""
        name = self.open_name.text().strip()
        id_card = self.open_id.text().strip()
        date = self.open_date.text().strip()

        try:
            amount = float(self.open_amount.text().strip())
        except ValueError:
            QMessageBox.warning(self, '警告', '金额必须为数字！')
            return

        if not name or not id_card or not date:
            QMessageBox.warning(self, '警告', '请填写完整信息！')
            return

        if not self.data_manager.validate_id_card(id_card):
            QMessageBox.warning(self, '警告', '身份证号格式不正确！')
            return

        if not self.data_manager.validate_date(date):
            QMessageBox.warning(self, '警告', '日期格式不正确！')
            return

        account_no = self.data_manager.next_account_no

        basic = AccountBasic(account_no, name, id_card, date)
        balance = AccountBalance(account_no, amount)

        self.basics.append(basic)
        self.balances.append(balance)
        self.data_manager.next_account_no = account_no + 1

        self.data_manager.save_account_basics(self.basics)
        self.data_manager.save_account_balances(self.balances)

        QMessageBox.information(self, '成功', f'开户成功！\n账号: {account_no}\n余额: {amount:.2f}元')

        self.open_name.clear()
        self.open_id.clear()
        self.open_date.clear()
        self.open_amount.clear()

    def borrow_money(self):
        """借款"""
        try:
            account_no = int(self.borrow_no.text().strip())
            amount = float(self.borrow_amount.text().strip())
        except ValueError:
            QMessageBox.warning(self, '警告', '请输入有效的账号和金额！')
            return

        if amount <= 0:
            QMessageBox.warning(self, '警告', '借款金额必须大于0！')
            return

        basic = self.data_manager.get_account_basic_by_no(self.basics, account_no)
        if not basic:
            QMessageBox.warning(self, '警告', '未找到该账户！')
            return

        balance = self.data_manager.get_account_balance_by_no(self.balances, account_no)
        if balance:
            balance.balance -= amount
            self.data_manager.save_account_balances(self.balances)
            QMessageBox.information(self, '成功', f'借款成功！\n账号: {account_no}\n当前余额: {balance.balance:.2f}元')

        self.borrow_no.clear()
        self.borrow_amount.clear()

    def repay_money(self):
        """还款"""
        try:
            account_no = int(self.repay_no.text().strip())
            amount = float(self.repay_amount.text().strip())
        except ValueError:
            QMessageBox.warning(self, '警告', '请输入有效的账号和金额！')
            return

        if amount <= 0:
            QMessageBox.warning(self, '警告', '还款金额必须大于0！')
            return

        basic = self.data_manager.get_account_basic_by_no(self.basics, account_no)
        if not basic:
            QMessageBox.warning(self, '警告', '未找到该账户！')
            return

        balance = self.data_manager.get_account_balance_by_no(self.balances, account_no)
        if not balance:
            QMessageBox.warning(self, '警告', '未找到该账户余额！')
            return

        if balance.balance + amount > 0:
            QMessageBox.warning(self, '警告', '还款金额超过借款额！')
            return

        balance.balance += amount
        self.data_manager.save_account_balances(self.balances)
        QMessageBox.information(self, '成功', f'还款成功！\n账号: {account_no}\n当前余额: {balance.balance:.2f}元')

        self.repay_no.clear()
        self.repay_amount.clear()

    def deposit_money(self):
        """存款"""
        try:
            account_no = int(self.deposit_no.text().strip())
            amount = float(self.deposit_amount.text().strip())
        except ValueError:
            QMessageBox.warning(self, '警告', '请输入有效的账号和金额！')
            return

        if amount <= 0:
            QMessageBox.warning(self, '警告', '存款金额必须大于0！')
            return

        basic = self.data_manager.get_account_basic_by_no(self.basics, account_no)
        if not basic:
            QMessageBox.warning(self, '警告', '未找到该账户！')
            return

        balance = self.data_manager.get_account_balance_by_no(self.balances, account_no)
        if balance:
            balance.balance += amount
            self.data_manager.save_account_balances(self.balances)
            QMessageBox.information(self, '成功', f'存款成功！\n账号: {account_no}\n当前余额: {balance.balance:.2f}元')

        self.deposit_no.clear()
        self.deposit_amount.clear()

    def query_account(self):
        """查询账户"""
        try:
            account_no = int(self.query_no.text().strip())
        except ValueError:
            QMessageBox.warning(self, '警告', '请输入有效的账号！')
            return

        basic = self.data_manager.get_account_basic_by_no(self.basics, account_no)
        if not basic:
            QMessageBox.warning(self, '警告', '未找到该账户！')
            return

        balance = self.data_manager.get_account_balance_by_no(self.balances, account_no)

        self.query_table.setRowCount(1)
        self.query_table.setColumnCount(5)
        self.query_table.setHorizontalHeaderLabels(['账号', '姓名', '身份证号', '开户日期', '余额'])

        self.query_table.setItem(0, 0, QTableWidgetItem(str(basic.account_no)))
        self.query_table.setItem(0, 1, QTableWidgetItem(basic.name))
        self.query_table.setItem(0, 2, QTableWidgetItem(basic.id_card))
        self.query_table.setItem(0, 3, QTableWidgetItem(basic.create_date))
        if balance:
            self.query_table.setItem(0, 4, QTableWidgetItem(f'{balance.balance:.2f}元'))

    def show_max_borrower(self):
        """显示最大借款账户"""
        result = self.data_manager.get_max_borrower(self.basics, self.balances)

        if result:
            basic, balance = result
            self.max_borrower_table.setRowCount(1)
            self.max_borrower_table.setColumnCount(5)
            self.max_borrower_table.setHorizontalHeaderLabels(['账号', '姓名', '身份证号', '开户日期', '借款金额'])

            self.max_borrower_table.setItem(0, 0, QTableWidgetItem(str(basic.account_no)))
            self.max_borrower_table.setItem(0, 1, QTableWidgetItem(basic.name))
            self.max_borrower_table.setItem(0, 2, QTableWidgetItem(basic.id_card))
            self.max_borrower_table.setItem(0, 3, QTableWidgetItem(basic.create_date))
            self.max_borrower_table.setItem(0, 4, QTableWidgetItem(f'{-balance.balance:.2f}元'))
        else:
            self.max_borrower_table.setRowCount(1)
            self.max_borrower_table.setColumnCount(1)
            self.max_borrower_table.setHorizontalHeaderLabels(['提示'])
            self.max_borrower_table.setItem(0, 0, QTableWidgetItem('没有借款账户'))

    def show_max_depositor(self):
        """显示最大存款账户"""
        result = self.data_manager.get_max_depositor(self.basics, self.balances)

        if result:
            basic, balance = result
            self.max_depositor_table.setRowCount(1)
            self.max_depositor_table.setColumnCount(5)
            self.max_depositor_table.setHorizontalHeaderLabels(['账号', '姓名', '身份证号', '开户日期', '存款金额'])

            self.max_depositor_table.setItem(0, 0, QTableWidgetItem(str(basic.account_no)))
            self.max_depositor_table.setItem(0, 1, QTableWidgetItem(basic.name))
            self.max_depositor_table.setItem(0, 2, QTableWidgetItem(basic.id_card))
            self.max_depositor_table.setItem(0, 3, QTableWidgetItem(basic.create_date))
            self.max_depositor_table.setItem(0, 4, QTableWidgetItem(f'{balance.balance:.2f}元'))
        else:
            self.max_depositor_table.setRowCount(1)
            self.max_depositor_table.setColumnCount(1)
            self.max_depositor_table.setHorizontalHeaderLabels(['提示'])
            self.max_depositor_table.setItem(0, 0, QTableWidgetItem('没有存款账户'))

    def sort_by_borrow(self):
        """按借款余额排序"""
        borrowers = []

        for basic in self.basics:
            if basic.account_no == -1:
                continue
            balance = self.data_manager.get_account_balance_by_no(self.balances, basic.account_no)
            if balance and balance.balance < 0:
                borrowers.append((basic, balance))

        borrowers.sort(key=lambda x: x[1].balance, reverse=True)

        self.sort_borrow_table.setRowCount(len(borrowers))
        self.sort_borrow_table.setColumnCount(3)
        self.sort_borrow_table.setHorizontalHeaderLabels(['账号', '姓名', '借款金额'])

        for row, (basic, balance) in enumerate(borrowers):
            self.sort_borrow_table.setItem(row, 0, QTableWidgetItem(str(basic.account_no)))
            self.sort_borrow_table.setItem(row, 1, QTableWidgetItem(basic.name))
            self.sort_borrow_table.setItem(row, 2, QTableWidgetItem(f'{-balance.balance:.2f}元'))

    def sort_by_deposit(self):
        """按存款余额排序"""
        depositors = []

        for basic in self.basics:
            if basic.account_no == -1:
                continue
            balance = self.data_manager.get_account_balance_by_no(self.balances, basic.account_no)
            if balance and balance.balance > 0:
                depositors.append((basic, balance))

        depositors.sort(key=lambda x: x[1].balance, reverse=True)

        self.sort_deposit_table.setRowCount(len(depositors))
        self.sort_deposit_table.setColumnCount(3)
        self.sort_deposit_table.setHorizontalHeaderLabels(['账号', '姓名', '存款金额'])

        for row, (basic, balance) in enumerate(depositors):
            self.sort_deposit_table.setItem(row, 0, QTableWidgetItem(str(basic.account_no)))
            self.sort_deposit_table.setItem(row, 1, QTableWidgetItem(basic.name))
            self.sort_deposit_table.setItem(row, 2, QTableWidgetItem(f'{balance.balance:.2f}元'))

    def sort_by_date(self):
        """按开户日期排序"""
        accounts = []

        for basic in self.basics:
            if basic.account_no == -1:
                continue
            balance = self.data_manager.get_account_balance_by_no(self.balances, basic.account_no)
            accounts.append((basic, balance))

        accounts.sort(key=lambda x: x[0].create_date)

        self.sort_date_table.setRowCount(len(accounts))
        self.sort_date_table.setColumnCount(5)
        self.sort_date_table.setHorizontalHeaderLabels(['账号', '姓名', '身份证号', '开户日期', '余额'])

        for row, (basic, balance) in enumerate(accounts):
            self.sort_date_table.setItem(row, 0, QTableWidgetItem(str(basic.account_no)))
            self.sort_date_table.setItem(row, 1, QTableWidgetItem(basic.name))
            self.sort_date_table.setItem(row, 2, QTableWidgetItem(basic.id_card))
            self.sort_date_table.setItem(row, 3, QTableWidgetItem(basic.create_date))
            if balance:
                self.sort_date_table.setItem(row, 4, QTableWidgetItem(f'{balance.balance:.2f}元'))

    def delete_account(self):
        """清户"""
        try:
            account_no = int(self.delete_no.text().strip())
        except ValueError:
            QMessageBox.warning(self, '警告', '请输入有效的账号！')
            return

        for i, basic in enumerate(self.basics):
            if basic.account_no == account_no:
                balance = self.data_manager.get_account_balance_by_no(self.balances, account_no)
                current_balance = balance.balance if balance else 0

                reply = QMessageBox.question(
                    self, '确认删除',
                    f'账号: {account_no}\n姓名: {basic.name}\n当前余额: {current_balance:.2f}元\n\n确认删除该账户？',
                    QMessageBox.Yes | QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    basic.account_no = -1
                    if balance:
                        balance.account_no = -1
                    self.data_manager.save_account_basics(self.basics)
                    self.data_manager.save_account_balances(self.balances)
                    QMessageBox.information(self, '成功', '账户已删除（逻辑删除）！\n提示：请使用"文件紧缩"功能清除已删除账户。')

                self.delete_no.clear()
                return

        QMessageBox.warning(self, '警告', '未找到该账户！')

    def show_compact_info(self):
        """显示文件紧缩信息"""
        valid_accounts = [acc for acc in self.basics if acc.account_no != -1]
        deleted_count = len(self.basics) - len(valid_accounts)

        self.compact_table.setRowCount(2)
        self.compact_table.setColumnCount(2)
        self.compact_table.setHorizontalHeaderLabels(['项目', '数量'])

        self.compact_table.setItem(0, 0, QTableWidgetItem('当前账户数'))
        self.compact_table.setItem(0, 1, QTableWidgetItem(str(len(valid_accounts))))
        self.compact_table.setItem(1, 0, QTableWidgetItem('待删除账户数'))
        self.compact_table.setItem(1, 1, QTableWidgetItem(str(deleted_count)))

    def compact_files(self):
        """文件紧缩"""
        original_count = len(self.basics)

        valid_basics = [acc for acc in self.basics if acc.account_no != -1]
        valid_balances = [acc for acc in self.balances if acc.account_no != -1]

        self.basics = valid_basics
        self.balances = valid_balances

        self.data_manager.save_account_basics(self.basics)
        self.data_manager.save_account_balances(self.balances)

        QMessageBox.information(self, '成功', f'文件紧缩完成！\n原账户数: {original_count}\n现账户数: {len(self.basics)}\n删除账户数: {original_count - len(self.basics)}')

        self.show_compact_info()

    def show_statistics(self):
        """显示统计信息"""
        borrow_count = sum(1 for acc in self.basics if acc.account_no != -1)
        for i, basic in enumerate(self.basics):
            if basic.account_no == -1:
                continue
            balance = self.data_manager.get_account_balance_by_no(self.balances, basic.account_no)
            if balance and balance.balance < 0:
                pass

        borrow_accounts = []
        deposit_accounts = []
        total_borrow = 0.0
        total_deposit = 0.0

        for basic in self.basics:
            if basic.account_no == -1:
                continue
            balance = self.data_manager.get_account_balance_by_no(self.balances, basic.account_no)
            if balance:
                if balance.balance < 0:
                    borrow_accounts.append(basic)
                    total_borrow += -balance.balance
                elif balance.balance > 0:
                    deposit_accounts.append(basic)
                    total_deposit += balance.balance

        self.statistics_table.setRowCount(6)
        self.statistics_table.setColumnCount(2)
        self.statistics_table.setHorizontalHeaderLabels(['项目', '数值'])

        self.statistics_table.setItem(0, 0, QTableWidgetItem('当前账户个数'))
        self.statistics_table.setItem(0, 1, QTableWidgetItem(str(len([acc for acc in self.basics if acc.account_no != -1]))))
        self.statistics_table.setItem(1, 0, QTableWidgetItem('借款账户数'))
        self.statistics_table.setItem(1, 1, QTableWidgetItem(str(len(borrow_accounts))))
        self.statistics_table.setItem(2, 0, QTableWidgetItem('存款账户数'))
        self.statistics_table.setItem(2, 1, QTableWidgetItem(str(len(deposit_accounts))))
        self.statistics_table.setItem(3, 0, QTableWidgetItem('当前借款总额'))
        self.statistics_table.setItem(3, 1, QTableWidgetItem(f'{total_borrow:.2f}元'))
        self.statistics_table.setItem(4, 0, QTableWidgetItem('当前存款总额'))
        self.statistics_table.setItem(4, 1, QTableWidgetItem(f'{total_deposit:.2f}元'))
        self.statistics_table.setItem(5, 0, QTableWidgetItem('差额'))
        self.statistics_table.setItem(5, 1, QTableWidgetItem(f'{total_deposit - total_borrow:.2f}元'))
