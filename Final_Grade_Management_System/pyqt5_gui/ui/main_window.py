"""
主窗口
"""
import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QPushButton, QLabel
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QComboBox, QDialog
from PyQt5.QtCore import Qt
from data_manager import DataManager
from ui.login_dialog import LoginDialog


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        # 获取项目根目录
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.data_manager = DataManager(base_dir)
        self.basics = []
        self.grades = []
        self.init_ui()
        self.load_data()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('期末成绩管理系统')
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

        title_label = QLabel('期末成绩管理系统')
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

        self.btn_input = QPushButton('录入成绩')
        self.btn_input.setStyleSheet(btn_style)
        self.btn_input.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        sidebar_layout.addWidget(self.btn_input)

        self.btn_query_basic = QPushButton('查询基本情况')
        self.btn_query_basic.setStyleSheet(btn_style)
        self.btn_query_basic.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        sidebar_layout.addWidget(self.btn_query_basic)

        self.btn_query_grade = QPushButton('查询成绩')
        self.btn_query_grade.setStyleSheet(btn_style)
        self.btn_query_grade.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        sidebar_layout.addWidget(self.btn_query_grade)

        self.btn_show_all = QPushButton('成绩一览表')
        self.btn_show_all.setStyleSheet(btn_style)
        self.btn_show_all.clicked.connect(lambda: [self.stack.setCurrentIndex(3), self.show_all_grades()])
        sidebar_layout.addWidget(self.btn_show_all)

        self.btn_show_award = QPushButton('受奖情况')
        self.btn_show_award.setStyleSheet(btn_style)
        self.btn_show_award.clicked.connect(lambda: [self.stack.setCurrentIndex(4), self.show_awards()])
        sidebar_layout.addWidget(self.btn_show_award)

        self.btn_sort = QPushButton('成绩排序')
        self.btn_sort.setStyleSheet(btn_style)
        self.btn_sort.clicked.connect(lambda: [self.stack.setCurrentIndex(5), self.sort_by_average()])
        sidebar_layout.addWidget(self.btn_sort)

        self.btn_statistics = QPushButton('统计功能')
        self.btn_statistics.setStyleSheet(btn_style)
        self.btn_statistics.clicked.connect(lambda: self.stack.setCurrentIndex(6))
        sidebar_layout.addWidget(self.btn_statistics)

        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar)

        # 内容区域
        self.stack = QStackedWidget()

        # 录入成绩页面
        input_page = QWidget()
        input_layout = QVBoxLayout(input_page)

        label = QLabel('录入学生成绩')
        label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        input_layout.addWidget(label)

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText('学号')
        self.input_id.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 5px;')
        input_layout.addWidget(self.input_id)

        self.input_computer = QLineEdit()
        self.input_computer.setPlaceholderText('计算机成绩')
        self.input_computer.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 5px;')
        input_layout.addWidget(self.input_computer)

        self.input_math = QLineEdit()
        self.input_math.setPlaceholderText('高等数学成绩')
        self.input_math.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 5px;')
        input_layout.addWidget(self.input_math)

        self.input_english = QLineEdit()
        self.input_english.setPlaceholderText('外语成绩')
        self.input_english.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 5px;')
        input_layout.addWidget(self.input_english)

        self.input_pe = QLineEdit()
        self.input_pe.setPlaceholderText('体育成绩')
        self.input_pe.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 10px;')
        input_layout.addWidget(self.input_pe)

        submit_btn = QPushButton('提交')
        submit_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        ''')
        submit_btn.clicked.connect(self.input_grade)
        input_layout.addWidget(submit_btn)

        input_layout.addStretch()
        self.stack.addWidget(input_page)

        # 查询基本情况页面
        query_basic_page = QWidget()
        query_basic_layout = QVBoxLayout(query_basic_page)

        label2 = QLabel('查询学生基本情况')
        label2.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        query_basic_layout.addWidget(label2)

        self.query_id_edit = QLineEdit()
        self.query_id_edit.setPlaceholderText('请输入学号')
        self.query_id_edit.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 10px;')
        query_basic_layout.addWidget(self.query_id_edit)

        query_btn = QPushButton('查询')
        query_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
        ''')
        query_btn.clicked.connect(self.query_student_basic)
        query_basic_layout.addWidget(query_btn)

        self.basic_table = QTableWidget()
        self.basic_table.setStyleSheet('QTableWidget {gridline-color: #ccc; alternate-background-color: #f5f5f5; }')
        query_basic_layout.addWidget(self.basic_table)

        self.stack.addWidget(query_basic_page)

        # 查询成绩页面
        query_grade_page = QWidget()
        query_grade_layout = QVBoxLayout(query_grade_page)

        label3 = QLabel('查询学生成绩')
        label3.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        query_grade_layout.addWidget(label3)

        self.query_grade_id_edit = QLineEdit()
        self.query_grade_id_edit.setPlaceholderText('请输入学号')
        self.query_grade_id_edit.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 10px;')
        query_grade_layout.addWidget(self.query_grade_id_edit)

        query_grade_btn = QPushButton('查询')
        query_grade_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
        ''')
        query_grade_btn.clicked.connect(self.query_student_grade)
        query_grade_layout.addWidget(query_grade_btn)

        self.grade_table = QTableWidget()
        self.grade_table.setStyleSheet('QTableWidget {gridline-color: #ccc; alternate-background-color: #f5f5f5; }')
        query_grade_layout.addWidget(self.grade_table)

        self.stack.addWidget(query_grade_page)

        # 成绩一览表页面
        all_grade_page = QWidget()
        all_grade_layout = QVBoxLayout(all_grade_page)

        label4 = QLabel('期末成绩一览表')
        label4.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        all_grade_layout.addWidget(label4)

        self.all_grade_table = QTableWidget()
        self.all_grade_table.setStyleSheet('QTableWidget {gridline-color: #ccc; alternate-background-color: #f5f5f5; }')
        all_grade_layout.addWidget(self.all_grade_table)

        self.stack.addWidget(all_grade_page)

        # 受奖情况页面
        award_page = QWidget()
        award_layout = QVBoxLayout(award_page)

        label5 = QLabel('受奖情况')
        label5.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        award_layout.addWidget(label5)

        self.award_table = QTableWidget()
        self.award_table.setStyleSheet('QTableWidget {gridline-color: #ccc; alternate-background-color: #f5f5f5; }')
        award_layout.addWidget(self.award_table)

        self.stack.addWidget(award_page)

        # 排序页面
        sort_page = QWidget()
        sort_layout = QVBoxLayout(sort_page)

        label6 = QLabel('按平均成绩从高到低排序')
        label6.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        sort_layout.addWidget(label6)

        self.sort_table = QTableWidget()
        self.sort_table.setStyleSheet('QTableWidget {gridline-color: #ccc; alternate-background-color: #f5f5f5; }')
        sort_layout.addWidget(self.sort_table)

        self.stack.addWidget(sort_page)

        # 统计功能页面
        statistics_page = QWidget()
        statistics_layout = QVBoxLayout(statistics_page)

        label7 = QLabel('统计功能')
        label7.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        statistics_layout.addWidget(label7)

        self.statistics_combo = QComboBox()
        self.statistics_combo.addItems([
            '各科平均分',
            '各科最高最低分',
            '各科各级别人数',
            '留级退学统计',
            '补考留级判断'
        ])
        self.statistics_combo.setStyleSheet('padding: 8px; font-size: 12px; margin-bottom: 10px;')
        statistics_layout.addWidget(self.statistics_combo)

        stat_btn = QPushButton('查看统计')
        stat_btn.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
            }
        ''')
        stat_btn.clicked.connect(self.show_statistics)
        statistics_layout.addWidget(stat_btn)

        self.statistics_table = QTableWidget()
        self.statistics_table.setStyleSheet('QTableWidget {gridline-color: #ccc; alternate-background-color: #f5f5f5; }')
        statistics_layout.addWidget(self.statistics_table)

        self.stack.addWidget(statistics_page)

        main_layout.addWidget(self.stack)

        # 初始化显示
        self.show_all_grades()

    def load_data(self):
        """加载数据"""
        self.basics = self.data_manager.read_student_basics()
        self.grades = self.data_manager.read_student_grades()

    def input_grade(self):
        """录入学生成绩"""
        student_id = self.input_id.text().strip()

        if not student_id:
            QMessageBox.warning(self, '警告', '请输入学号！')
            return

        # 检查学生是否存在
        basic = self.data_manager.get_student_basic_by_id(self.basics, student_id)
        if not basic:
            QMessageBox.warning(self, '警告', '该学生不存在！')
            return

        try:
            computer = float(self.input_computer.text().strip())
            math = float(self.input_math.text().strip())
            english = float(self.input_english.text().strip())
            pe = float(self.input_pe.text().strip())
        except ValueError:
            QMessageBox.warning(self, '警告', '成绩必须为数字！')
            return

        average = (computer + math + english + pe) / 4

        # 查找并更新或添加成绩
        grade = self.data_manager.get_student_grade_by_id(self.grades, student_id)
        if grade:
            grade.computer_score = computer
            grade.math_score = math
            grade.english_score = english
            grade.pe_score = pe
            grade.average_score = average
            QMessageBox.information(self, '提示', '成绩已更新！')
        else:
            new_grade = StudentGrade(student_id, computer, math, english, pe, average)
            self.grades.append(new_grade)
            QMessageBox.information(self, '提示', '成绩已录入！')

        # 保存到文件
        self.data_manager.save_student_grades(self.grades)

        # 清空输入
        self.input_id.clear()
        self.input_computer.clear()
        self.input_math.clear()
        self.input_english.clear()
        self.input_pe.clear()

        # 刷新表格
        self.show_all_grades()

    def query_student_basic(self):
        """查询学生基本情况"""
        student_id = self.query_id_edit.text().strip()

        if not student_id:
            QMessageBox.warning(self, '警告', '请输入学号！')
            return

        basic = self.data_manager.get_student_basic_by_id(self.basics, student_id)
        if basic:
            self.basic_table.setRowCount(1)
            self.basic_table.setColumnCount(8)
            self.basic_table.setHorizontalHeaderLabels([
                '学号', '姓名', '性别', '出生日期', '入学日期', '受奖次数', '补考次数', '留级次数'
            ])

            self.basic_table.setItem(0, 0, QTableWidgetItem(basic.id))
            self.basic_table.setItem(0, 1, QTableWidgetItem(basic.name))
            self.basic_table.setItem(0, 2, QTableWidgetItem(basic.sex))
            self.basic_table.setItem(0, 3, QTableWidgetItem(basic.birth_date))
            self.basic_table.setItem(0, 4, QTableWidgetItem(basic.enroll_date))
            self.basic_table.setItem(0, 5, QTableWidgetItem(str(basic.award_count)))
            self.basic_table.setItem(0, 6, QTableWidgetItem(str(basic.makeup_count)))
            self.basic_table.setItem(0, 7, QTableWidgetItem(str(basic.retain_count)))
        else:
            QMessageBox.warning(self, '提示', '未找到该学生！')

    def query_student_grade(self):
        """查询学生成绩"""
        student_id = self.query_grade_id_edit.text().strip()

        if not student_id:
            QMessageBox.warning(self, '警告', '请输入学号！')
            return

        grade = self.data_manager.get_student_grade_by_id(self.grades, student_id)
        if grade:
            basic = self.data_manager.get_student_basic_by_id(self.basics, student_id)
            self.grade_table.setRowCount(1)
            self.grade_table.setColumnCount(6)
            self.grade_table.setHorizontalHeaderLabels([
                '学号', '姓名', '计算机', '高等数学', '外语', '体育', '平均分'
            ])

            self.grade_table.setItem(0, 0, QTableWidgetItem(grade.id))
            if basic:
                self.grade_table.setItem(0, 1, QTableWidgetItem(basic.name))
            self.grade_table.setItem(0, 2, QTableWidgetItem(f'{grade.computer_score:.2f}'))
            self.grade_table.setItem(0, 3, QTableWidgetItem(f'{grade.math_score:.2f}'))
            self.grade_table.setItem(0, 4, QTableWidgetItem(f'{grade.english_score:.2f}'))
            self.grade_table.setItem(0, 5, QTableWidgetItem(f'{grade.pe_score:.2f}'))
            self.grade_table.setItem(0, 6, QTableWidgetItem(f'{grade.average_score:.2f}'))
        else:
            QMessageBox.warning(self, '提示', '未找到该学生！')

    def show_all_grades(self):
        """显示所有成绩"""
        self.all_grade_table.setRowCount(len(self.grades))
        self.all_grade_table.setColumnCount(7)
        self.all_grade_table.setHorizontalHeaderLabels([
            '学号', '姓名', '计算机', '高等数学', '外语', '体育', '平均分'
        ])

        for row, grade in enumerate(self.grades):
            basic = self.data_manager.get_student_basic_by_id(self.basics, grade.id)
            self.all_grade_table.setItem(row, 0, QTableWidgetItem(grade.id))
            if basic:
                self.all_grade_table.setItem(row, 1, QTableWidgetItem(basic.name))
            self.all_grade_table.setItem(row, 2, QTableWidgetItem(f'{grade.computer_score:.2f}'))
            self.all_grade_table.setItem(row, 3, QTableWidgetItem(f'{grade.math_score:.2f}'))
            self.all_grade_table.setItem(row, 4, QTableWidgetItem(f'{grade.english_score:.2f}'))
            self.all_grade_table.setItem(row, 5, QTableWidgetItem(f'{grade.pe_score:.2f}'))
            self.all_grade_table.setItem(row, 6, QTableWidgetItem(f'{grade.average_score:.2f}'))

    def show_awards(self):
        """显示受奖情况"""
        results = []
        for grade in self.grades:
            award = self.data_manager.calculate_award(grade.average_score)
            if award > 0:
                basic = self.data_manager.get_student_basic_by_id(self.basics, grade.id)
                if basic:
                    results.append((grade, basic, award))

        self.award_table.setRowCount(len(results))
        self.award_table.setColumnCount(8)
        self.award_table.setHorizontalHeaderLabels([
            '学号', '姓名', '计算机', '高等数学', '外语', '体育', '平均分', '奖励金额'
        ])

        for row, (grade, basic, award) in enumerate(results):
            self.award_table.setItem(row, 0, QTableWidgetItem(grade.id))
            self.award_table.setItem(row, 1, QTableWidgetItem(basic.name))
            self.award_table.setItem(row, 2, QTableWidgetItem(f'{grade.computer_score:.2f}'))
            self.award_table.setItem(row, 3, QTableWidgetItem(f'{grade.math_score:.2f}'))
            self.award_table.setItem(row, 4, QTableWidgetItem(f'{grade.english_score:.2f}'))
            self.award_table.setItem(row, 5, QTableWidgetItem(f'{grade.pe_score:.2f}'))
            self.award_table.setItem(row, 6, QTableWidgetItem(f'{grade.average_score:.2f}'))
            self.award_table.setItem(row, 7, QTableWidgetItem(f'{award}元'))

    def sort_by_average(self):
        """按平均成绩排序"""
        sorted_grades = sorted(self.grades, key=lambda g: g.average_score, reverse=True)

        self.sort_table.setRowCount(len(sorted_grades))
        self.sort_table.setColumnCount(7)
        self.sort_table.setHorizontalHeaderLabels([
            '学号', '姓名', '计算机', '高等数学', '外语', '体育', '平均分'
        ])

        for row, grade in enumerate(sorted_grades):
            basic = self.data_manager.get_student_basic_by_id(self.basics, grade.id)
            self.sort_table.setItem(row, 0, QTableWidgetItem(grade.id))
            if basic:
                self.sort_table.setItem(row, 1, QTableWidgetItem(basic.name))
            self.sort_table.setItem(row, 2, QTableWidgetItem(f'{grade.computer_score:.2f}'))
            self.sort_table.setItem(row, 3, QTableWidgetItem(f'{grade.math_score:.2f}'))
            self.sort_table.setItem(row, 4, QTableWidgetItem(f'{grade.english_score:.2f}'))
            self.sort_table.setItem(row, 5, QTableWidgetItem(f'{grade.pe_score:.2f}'))
            self.sort_table.setItem(row, 6, QTableWidgetItem(f'{grade.average_score:.2f}'))

    def show_statistics(self):
        """显示统计"""
        stat_type = self.statistics_combo.currentText()

        if stat_type == '各科平均分':
            self.show_average_stats()
        elif stat_type == '各科最高最低分':
            self.show_max_min_stats()
        elif stat_type == '各科各级别人数':
            self.show_grade_levels()
        elif stat_type == '留级退学统计':
            self.show_retain_drop_stats()
        elif stat_type == '补考留级判断':
            self.check_failures()

    def show_average_stats(self):
        """显示平均分统计"""
        if not self.grades:
            return

        sum_computer = sum(g.computer_score for g in self.grades)
        sum_math = sum(g.math_score for g in self.grades)
        sum_english = sum(g.english_score for g in self.grades)
        sum_pe = sum(g.pe_score for g in self.grades)
        count = len(self.grades)

        self.statistics_table.setRowCount(4)
        self.statistics_table.setColumnCount(2)
        self.statistics_table.setHorizontalHeaderLabels(['科目', '平均分'])

        self.statistics_table.setItem(0, 0, QTableWidgetItem('计算机'))
        self.statistics_table.setItem(0, 1, QTableWidgetItem(f'{sum_computer/count:.2f}'))
        self.statistics_table.setItem(1, 0, QTableWidgetItem('高等数学'))
        self.statistics_table.setItem(1, 1, QTableWidgetItem(f'{sum_math/count:.2f}'))
        self.statistics_table.setItem(2, 0, QTableWidgetItem('外语'))
        self.statistics_table.setItem(2, 1, QTableWidgetItem(f'{sum_english/count:.2f}'))
        self.statistics_table.setItem(3, 0, QTableWidgetItem('体育'))
        self.statistics_table.setItem(3, 1, QTableWidgetItem(f'{sum_pe/count:.2f}'))

    def show_max_min_stats(self):
        """显示最高最低分统计"""
        if not self.grades:
            return

        max_computer = max(g.computer_score for g in self.grades)
        min_computer = min(g.computer_score for g in self.grades)
        max_math = max(g.math_score for g in self.grades)
        min_math = min(g.math_score for g in self.grades)
        max_english = max(g.english_score for g in self.grades)
        min_english = min(g.english_score for g in self.grades)
        max_pe = max(g.pe_score for g in self.grades)
        min_pe = min(g.pe_score for g in self.grades)

        self.statistics_table.setRowCount(4)
        self.statistics_table.setColumnCount(3)
        self.statistics_table.setHorizontalHeaderLabels(['科目', '最高分', '最低分'])

        self.statistics_table.setItem(0, 0, QTableWidgetItem('计算机'))
        self.statistics_table.setItem(0, 1, QTableWidgetItem(f'{max_computer:.2f}'))
        self.statistics_table.setItem(0, 2, QTableWidgetItem(f'{min_computer:.2f}'))
        self.statistics_table.setItem(1, 0, QTableWidgetItem('高等数学'))
        self.statistics_table.setItem(1, 1, QTableWidgetItem(f'{max_math:.2f}'))
        self.statistics_table.setItem(1, 2, QTableWidgetItem(f'{min_math:.2f}'))
        self.statistics_table.setItem(2, 0, QTableWidgetItem('外语'))
        self.statistics_table.setItem(2, 1, QTableWidgetItem(f'{max_english:.2f}'))
        self.statistics_table.setItem(2, 2, QTableWidgetItem(f'{min_english:.2f}'))
        self.statistics_table.setItem(3, 0, QTableWidgetItem('体育'))
        self.statistics_table.setItem(3, 1, QTableWidgetItem(f'{max_pe:.2f}'))
        self.statistics_table.setItem(3, 2, QTableWidgetItem(f'{min_pe:.2f}'))

    def show_grade_levels(self):
        """显示各级别人数"""
        levels = ['优(90+)', '良(80-89)', '中(70-79)', '及格(60-69)', '不及格(<60)']
        computer_counts = [0] * 5
        math_counts = [0] * 5
        english_counts = [0] * 5
        pe_counts = [0] * 5

        for grade in self.grades:
            for i, (score, counts) in enumerate([
                (grade.computer_score, computer_counts),
                (grade.math_score, math_counts),
                (grade.english_score, english_counts),
                (grade.pe_score, pe_counts)
            ]):
                if score >= 90:
                    counts[0] += 1
                elif score >= 80:
                    counts[1] += 1
                elif score >= 70:
                    counts[2] += 1
                elif score >= 60:
                    counts[3] += 1
                else:
                    counts[4] += 1

        self.statistics_table.setRowCount(5)
        self.statistics_table.setColumnCount(5)
        self.statistics_table.setHorizontalHeaderLabels(['等级', '计算机', '高等数学', '外语', '体育'])

        for i, level in enumerate(levels):
            self.statistics_table.setItem(i, 0, QTableWidgetItem(level))
            self.statistics_table.setItem(i, 1, QTableWidgetItem(str(computer_counts[i])))
            self.statistics_table.setItem(i, 2, QTableWidgetItem(str(math_counts[i])))
            self.statistics_table.setItem(i, 3, QTableWidgetItem(str(english_counts[i])))
            self.statistics_table.setItem(i, 4, QTableWidgetItem(str(pe_counts[i])))

    def show_retain_drop_stats(self):
        """显示留级退学统计"""
        retain_count = sum(1 for b in self.basics if b.retain_count > 0)
        makeup_count = sum(1 for b in self.basics if b.makeup_count > 0)
        drop_count = sum(1 for b in self.basics if b.retain_count >= 2 or b.makeup_count >= 8)

        self.statistics_table.setRowCount(3)
        self.statistics_table.setColumnCount(2)
        self.statistics_table.setHorizontalHeaderLabels(['项目', '人数'])

        self.statistics_table.setItem(0, 0, QTableWidgetItem('留级人数'))
        self.statistics_table.setItem(0, 1, QTableWidgetItem(str(retain_count)))
        self.statistics_table.setItem(1, 0, QTableWidgetItem('补考人数'))
        self.statistics_table.setItem(1, 1, QTableWidgetItem(str(makeup_count)))
        self.statistics_table.setItem(2, 0, QTableWidgetItem('退学人数'))
        self.statistics_table.setItem(2, 1, QTableWidgetItem(str(drop_count)))

    def check_failures(self):
        """判断补考与留级"""
        results = []
        for grade in self.grades:
            basic = self.data_manager.get_student_basic_by_id(self.basics, grade.id)
            if basic:
                fail_computer = grade.computer_score < 60
                fail_math = grade.math_score < 60
                fail_english = grade.english_score < 60
                fail_pe = grade.pe_score < 60

                fail_subjects = []
                if fail_computer:
                    fail_subjects.append('计算机')
                if fail_math:
                    fail_subjects.append('高等数学')
                if fail_english:
                    fail_subjects.append('外语')
                if fail_pe:
                    fail_subjects.append('体育')

                status = '全科及格'
                if fail_subjects:
                    status = f'需补考：{", ".join(fail_subjects)}'
                    if fail_computer and fail_math and fail_english:
                        status += '，需留级'

                if basic.retain_count >= 2:
                    status += '，需退学（留级）'
                elif basic.makeup_count >= 8:
                    status += '，需退学（补考）'

                results.append((grade, basic, status))

        self.statistics_table.setRowCount(len(results))
        self.statistics_table.setColumnCount(3)
        self.statistics_table.setHorizontalHeaderLabels(['学号', '姓名', '状态'])

        for row, (grade, basic, status) in enumerate(results):
            self.statistics_table.setItem(row, 0, QTableWidgetItem(grade.id))
            self.statistics_table.setItem(row, 1, QTableWidgetItem(basic.name))
            self.statistics_table.setItem(row, 2, QTableWidgetItem(status))


def run():
    """运行应用"""
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWidgets import QDialog

    app = QApplication(sys.argv)

    # 获取项目根目录（Final_Grade_Management_System）
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_manager = DataManager(base_dir)

    login_dialog = LoginDialog(data_manager)
    if login_dialog.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)
