"""
主窗口
"""
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QTableWidget, QTableWidgetItem,
                             QMessageBox, QStackedWidget)
from PyQt5.QtCore import Qt
from data_manager import DataManager
from ui.login_dialog import LoginDialog


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        # 获取项目根目录（Attendance_Management_System）
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.data_manager = DataManager(base_dir)
        self.employees = []
        self.attendances = []
        self.punch_records = []
        self.init_ui()
        self.load_data()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('出勤管理系统')
        self.setGeometry(100, 100, 900, 600)

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

        title_label = QLabel('功能菜单')
        title_label.setStyleSheet('font-size: 16px; font-weight: bold; padding: 20px;')
        title_label.setAlignment(Qt.AlignCenter)
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

        self.btn_process = QPushButton('读取打卡记录')
        self.btn_process.setStyleSheet(btn_style)
        self.btn_process.clicked.connect(self.process_punch_records)
        sidebar_layout.addWidget(self.btn_process)

        self.btn_query = QPushButton('查询功能')
        self.btn_query.setStyleSheet(btn_style)
        self.btn_query.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        sidebar_layout.addWidget(self.btn_query)

        self.btn_leave = QPushButton('请假管理')
        self.btn_leave.setStyleSheet(btn_style)
        self.btn_leave.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        sidebar_layout.addWidget(self.btn_leave)

        self.btn_statistics = QPushButton('统计功能')
        self.btn_statistics.setStyleSheet(btn_style)
        self.btn_statistics.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        sidebar_layout.addWidget(self.btn_statistics)

        self.btn_sort = QPushButton('排序功能')
        self.btn_sort.setStyleSheet(btn_style)
        self.btn_sort.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        sidebar_layout.addWidget(self.btn_sort)

        sidebar_layout.addStretch()

        sidebar_layout.addWidget(sidebar)

        # 内容区域
        self.stack = QStackedWidget()

        # 查询页面
        self.query_widget = QWidget()
        self.init_query_page()
        self.stack.addWidget(self.query_widget)

        # 请假页面
        self.leave_widget = QWidget()
        self.init_leave_page()
        self.stack.addWidget(self.leave_widget)

        # 统计页面
        self.statistics_widget = QWidget()
        self.init_statistics_page()
        self.stack.addWidget(self.statistics_widget)

        # 排序页面
        self.sort_widget = QWidget()
        self.init_sort_page()
        self.stack.addWidget(self.sort_widget)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

    def init_query_page(self):
        """初始化查询页面"""
        layout = QVBoxLayout(self.query_widget)

        # 查询按钮
        btn_layout = QHBoxLayout()

        btn_style = '''
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 8px 16px;
                font-size: 13px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        '''

        query_by_id_btn = QPushButton('按编号查询')
        query_by_id_btn.setStyleSheet(btn_style)
        query_by_id_btn.clicked.connect(self.query_by_id)
        btn_layout.addWidget(query_by_id_btn)

        perfect_btn = QPushButton('全勤职工')
        perfect_btn.setStyleSheet(btn_style)
        perfect_btn.clicked.connect(self.query_perfect_attendance)
        btn_layout.addWidget(perfect_btn)

        leave_btn = QPushButton('请假超标')
        leave_btn.setStyleSheet(btn_style)
        leave_btn.clicked.connect(self.query_excessive_leave)
        btn_layout.addWidget(leave_btn)

        absent_btn = QPushButton('旷工职工')
        absent_btn.setStyleSheet(btn_style)
        absent_btn.clicked.connect(self.query_absent_employees)
        btn_layout.addWidget(absent_btn)

        layout.addLayout(btn_layout)

        # 结果表格
        self.query_table = QTableWidget()
        self.query_table.setStyleSheet('''
            QTableWidget {
                gridline-color: #BDC3C7;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #ECF0F1;
                padding: 8px;
                font-weight: bold;
                border: 1px solid #BDC3C7;
            }
        ''')
        layout.addWidget(self.query_table)

    def init_leave_page(self):
        """初始化请假页面"""
        layout = QVBoxLayout(self.leave_widget)

        info_label = QLabel('请输入职工编号进行请假登记')
        info_label.setStyleSheet('font-size: 14px; padding: 10px;')
        layout.addWidget(info_label)

        self.leave_id_edit = QLabel('职工编号：')
        layout.addWidget(self.leave_id_edit)

        from PyQt5.QtWidgets import QLineEdit
        self.leave_id_input = QLineEdit()
        self.leave_id_input.setStyleSheet('padding: 8px; font-size: 12px;')
        layout.addWidget(self.leave_id_input)

        submit_btn = QPushButton('提交请假')
        submit_btn.setStyleSheet('''
            QPushButton {
                background-color: #E67E22;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #D35400;
            }
        ''')
        submit_btn.clicked.connect(self.submit_leave)
        layout.addWidget(submit_btn)

        # 请假结果表格
        self.leave_table = QTableWidget()
        self.leave_table.setStyleSheet('''
            QTableWidget {
                gridline-color: #BDC3C7;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #ECF0F1;
                padding: 8px;
                font-weight: bold;
            }
        ''')
        layout.addWidget(self.leave_table)

        refresh_btn = QPushButton('刷新数据')
        refresh_btn.setStyleSheet('''
            QPushButton {
                background-color: #27AE60;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        ''')
        refresh_btn.clicked.connect(self.load_data)
        layout.addWidget(refresh_btn)

    def init_statistics_page(self):
        """初始化统计页面"""
        layout = QVBoxLayout(self.statistics_widget)

        from PyQt5.QtWidgets import QTextEdit
        self.statistics_text = QTextEdit()
        self.statistics_text.setStyleSheet('''
            QTextEdit {
                font-family: "Microsoft YaHei";
                font-size: 13px;
                padding: 10px;
                background-color: #FFFFFF;
                border: 1px solid #BDC3C7;
            }
        ''')
        self.statistics_text.setReadOnly(True)
        layout.addWidget(self.statistics_text)

        show_btn = QPushButton('显示统计信息')
        show_btn.setStyleSheet('''
            QPushButton {
                background-color: #9B59B6;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #8E44AD;
            }
        ''')
        show_btn.clicked.connect(self.show_statistics)
        layout.addWidget(show_btn)

    def init_sort_page(self):
        """初始化排序页面"""
        layout = QVBoxLayout(self.sort_widget)

        btn_layout = QHBoxLayout()

        btn_style = '''
            QPushButton {
                background-color: #1ABC9C;
                color: white;
                padding: 10px 20px;
                font-size: 13px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
        '''

        earliest_btn = QPushButton('最早到厂')
        earliest_btn.setStyleSheet(btn_style)
        earliest_btn.clicked.connect(self.sort_earliest)
        btn_layout.addWidget(earliest_btn)

        asc_btn = QPushButton('出生日期升序')
        asc_btn.setStyleSheet(btn_style)
        asc_btn.clicked.connect(lambda: self.sort_by_birth_date(True))
        btn_layout.addWidget(asc_btn)

        desc_btn = QPushButton('女职工降序')
        desc_btn.setStyleSheet(btn_style)
        desc_btn.clicked.connect(lambda: self.sort_by_birth_date(False))
        btn_layout.addWidget(desc_btn)

        layout.addLayout(btn_layout)

        # 排序结果表格
        self.sort_table = QTableWidget()
        self.sort_table.setStyleSheet('''
            QTableWidget {
                gridline-color: #BDC3C7;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #ECF0F1;
                padding: 8px;
                font-weight: bold;
            }
        ''')
        layout.addWidget(self.sort_table)

    def load_data(self):
        """加载数据"""
        self.employees = self.data_manager.read_employees()
        self.attendances = self.data_manager.read_attendance()
        self.punch_records = self.data_manager.read_punch_records()

    def process_punch_records(self):
        """处理打卡记录"""
        self.attendances = self.data_manager.process_punch_records(
            self.employees, self.attendances, self.punch_records
        )
        self.data_manager.save_attendance(self.attendances)
        self.data_manager.append_month_records(self.punch_records)

        QMessageBox.information(self, '成功', '打卡记录处理完成！\n已更新月出勤情况文件。')

    def query_by_id(self):
        """按编号查询"""
        from PyQt5.QtWidgets import QInputDialog
        emp_id, ok = QInputDialog.getText(self, '查询职工', '请输入职工编号：')

        if ok and emp_id:
            emp = self.data_manager.get_employee_by_id(self.employees, emp_id)
            att = self.data_manager.get_attendance_by_id(self.attendances, emp_id)
            record = self.data_manager.get_punch_record_by_id(self.punch_records, emp_id)

            if emp:
                self.query_table.setRowCount(1)
                self.query_table.setColumnCount(6)
                self.query_table.setHorizontalHeaderLabels(
                    ['编号', '姓名', '性别', '出生日期', '职务级别', '所在部门']
                )

                self.query_table.setItem(0, 0, QTableWidgetItem(emp.id))
                self.query_table.setItem(0, 1, QTableWidgetItem(emp.name))
                self.query_table.setItem(0, 2, QTableWidgetItem(emp.sex))
                self.query_table.setItem(0, 3, QTableWidgetItem(emp.birth_date))
                self.query_table.setItem(0, 4, QTableWidgetItem(emp.level))
                self.query_table.setItem(0, 5, QTableWidgetItem(emp.department))

                if record:
                    arrival_time = f'{record.hour:02d}:{record.minute:02d}:{record.second:02d}'
                    QMessageBox.information(self, '当日到厂时间', f'到厂时间：{arrival_time}')
                else:
                    QMessageBox.information(self, '当日到厂时间', '当日未打卡')

                if att:
                    msg = f'迟到次数：{att.late_count}\n请假天数：{att.leave_days}\n旷工天数：{att.absent_days}'
                    QMessageBox.information(self, '当月出勤情况', msg)
            else:
                QMessageBox.warning(self, '提示', '未找到该职工！')

    def query_perfect_attendance(self):
        """查询全勤职工"""
        results = []
        for emp in self.employees:
            att = self.data_manager.get_attendance_by_id(self.attendances, emp.id)
            if att and att.late_count == 0 and att.leave_days == 0 and att.absent_days == 0:
                results.append(emp)

        self.query_table.setRowCount(len(results))
        self.query_table.setColumnCount(4)
        self.query_table.setHorizontalHeaderLabels(['编号', '姓名', '性别', '出生日期'])

        for row, emp in enumerate(results):
            self.query_table.setItem(row, 0, QTableWidgetItem(emp.id))
            self.query_table.setItem(row, 1, QTableWidgetItem(emp.name))
            self.query_table.setItem(row, 2, QTableWidgetItem(emp.sex))
            self.query_table.setItem(row, 3, QTableWidgetItem(emp.birth_date))

    def query_excessive_leave(self):
        """查询请假天数超过5天的职工"""
        results = []
        for emp in self.employees:
            att = self.data_manager.get_attendance_by_id(self.attendances, emp.id)
            if att:
                allowed = self.data_manager.get_allowed_leave_days(emp)
                exceeded = att.leave_days - allowed
                if att.leave_days > 5:
                    results.append((emp, allowed, att.leave_days, exceeded))

        self.query_table.setRowCount(len(results))
        self.query_table.setColumnCount(7)
        self.query_table.setHorizontalHeaderLabels(
            ['编号', '姓名', '性别', '出生日期', '允许天数', '实际天数', '超出天数']
        )

        for row, (emp, allowed, actual, exceeded) in enumerate(results):
            self.query_table.setItem(row, 0, QTableWidgetItem(emp.id))
            self.query_table.setItem(row, 1, QTableWidgetItem(emp.name))
            self.query_table.setItem(row, 2, QTableWidgetItem(emp.sex))
            self.query_table.setItem(row, 3, QTableWidgetItem(emp.birth_date))
            self.query_table.setItem(row, 4, QTableWidgetItem(str(allowed)))
            self.query_table.setItem(row, 5, QTableWidgetItem(str(actual)))
            self.query_table.setItem(row, 6, QTableWidgetItem(str(exceeded)))

    def query_absent_employees(self):
        """查询旷工职工"""
        results = []
        for emp in self.employees:
            att = self.data_manager.get_attendance_by_id(self.attendances, emp.id)
            if att and att.absent_days > 0:
                results.append((emp, att))

        self.query_table.setRowCount(len(results))
        self.query_table.setColumnCount(7)
        self.query_table.setHorizontalHeaderLabels(
            ['编号', '姓名', '性别', '出生日期', '迟到次数', '请假天数', '旷工天数']
        )

        for row, (emp, att) in enumerate(results):
            self.query_table.setItem(row, 0, QTableWidgetItem(emp.id))
            self.query_table.setItem(row, 1, QTableWidgetItem(emp.name))
            self.query_table.setItem(row, 2, QTableWidgetItem(emp.sex))
            self.query_table.setItem(row, 3, QTableWidgetItem(emp.birth_date))
            self.query_table.setItem(row, 4, QTableWidgetItem(str(att.late_count)))
            self.query_table.setItem(row, 5, QTableWidgetItem(str(att.leave_days)))
            self.query_table.setItem(row, 6, QTableWidgetItem(str(att.absent_days)))

    def submit_leave(self):
        """提交请假"""
        emp_id = self.leave_id_input.text().strip()

        if not emp_id:
            QMessageBox.warning(self, '提示', '请输入职工编号！')
            return

        emp = self.data_manager.get_employee_by_id(self.employees, emp_id)
        if not emp:
            QMessageBox.warning(self, '提示', '未找到该职工！')
            return

        att = self.data_manager.get_attendance_by_id(self.attendances, emp_id)
        if att:
            att.leave_days += 1
            if att.absent_days > 0:
                att.absent_days -= 1

            self.data_manager.save_attendance(self.attendances)

            msg = f'职工：{emp.name}\n请假天数：{att.leave_days}\n旷工天数：{att.absent_days}'
            QMessageBox.information(self, '请假成功', msg)
            self.leave_id_input.clear()
        else:
            QMessageBox.warning(self, '提示', '未找到该职工的出勤记录！')

    def show_statistics(self):
        """显示统计信息"""
        total_emp = len(self.employees)
        perfect_count = 0
        max_late_minutes = 0
        max_leave_days = 0
        max_late_count = 0
        max_absent_days = 0
        late_today_count = 0

        for emp in self.employees:
            att = self.data_manager.get_attendance_by_id(self.attendances, emp.id)
            if att:
                if att.late_count == 0 and att.leave_days == 0 and att.absent_days == 0:
                    perfect_count += 1
                if att.leave_days > max_leave_days:
                    max_leave_days = att.leave_days
                if att.late_count > max_late_count:
                    max_late_count = att.late_count
                if att.absent_days > max_absent_days:
                    max_absent_days = att.absent_days

        for record in self.punch_records:
            arrival_time = record.hour * 3600 + record.minute * 60 + record.second
            standard_time = 8 * 3600

            if arrival_time > standard_time:
                late_time = arrival_time - standard_time
                if late_time > max_late_minutes:
                    max_late_minutes = late_time
                late_today_count += 1

        perfect_rate = (perfect_count / total_emp * 100) if total_emp > 0 else 0
        late_today_rate = (late_today_count / total_emp * 100) if total_emp > 0 else 0

        stats_text = f'''
══════════════════════════════════════════
          统计信息
══════════════════════════════════════════

【基本统计】
  当前职工总数：{total_emp}
  当月全勤职工总数：{perfect_count}
  全勤率：{perfect_rate:.2f}%

【当日统计】
  当日最长迟到时间：{max_late_minutes // 60}分钟
  当日迟到职工总数：{late_today_count}
  当日迟到率：{late_today_rate:.2f}%

【当月统计】
  当月最大请假天数：{max_leave_days}天
  当月最大迟到次数：{max_late_count}次
  当月最大旷工天数：{max_absent_days}天

══════════════════════════════════════════
'''

        self.statistics_text.setPlainText(stats_text)

    def sort_earliest(self):
        """排序最早到厂的职工"""
        earliest_time = 24 * 3600
        earliest_record = None

        for record in self.punch_records:
            arrival_time = record.hour * 3600 + record.minute * 60 + record.second
            if arrival_time < earliest_time:
                earliest_time = arrival_time
                earliest_record = record

        if earliest_record:
            emp = self.data_manager.get_employee_by_id(self.employees, earliest_record.id)
            if emp:
                self.sort_table.setRowCount(1)
                self.sort_table.setColumnCount(3)
                self.sort_table.setHorizontalHeaderLabels(['编号', '姓名', '到厂时间'])

                arrival_time_str = f'{earliest_record.hour:02d}:{earliest_record.minute:02d}:{earliest_record.second:02d}'
                self.sort_table.setItem(0, 0, QTableWidgetItem(emp.id))
                self.sort_table.setItem(0, 1, QTableWidgetItem(emp.name))
                self.sort_table.setItem(0, 2, QTableWidgetItem(arrival_time_str))
        else:
            QMessageBox.information(self, '提示', '今日无打卡记录')

    def sort_by_birth_date(self, ascending=True):
        """按出生日期排序"""
        if ascending:
            sorted_emps = sorted(self.employees, key=lambda e: e.birth_date)
            title = '按出生日期升序输出全体职工'
        else:
            female_emps = [e for e in self.employees if e.sex == '女']
            sorted_emps = sorted(female_emps, key=lambda e: e.birth_date, reverse=True)
            title = '按出生日期降序列出全体女职工'

        self.sort_table.setRowCount(len(sorted_emps))
        self.sort_table.setColumnCount(6)
        self.sort_table.setHorizontalHeaderLabels(['编号', '姓名', '性别', '出生日期', '职务级别', '所在部门'])

        for row, emp in enumerate(sorted_emps):
            self.sort_table.setItem(row, 0, QTableWidgetItem(emp.id))
            self.sort_table.setItem(row, 1, QTableWidgetItem(emp.name))
            self.sort_table.setItem(row, 2, QTableWidgetItem(emp.sex))
            self.sort_table.setItem(row, 3, QTableWidgetItem(emp.birth_date))
            self.sort_table.setItem(row, 4, QTableWidgetItem(emp.level))
            self.sort_table.setItem(row, 5, QTableWidgetItem(emp.department))


def run():
    """运行应用"""
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWidgets import QDialog

    app = QApplication(sys.argv)

    # 获取项目根目录（Attendance_Management_System）
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_manager = DataManager(base_dir)

    login_dialog = LoginDialog(data_manager)
    if login_dialog.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)
