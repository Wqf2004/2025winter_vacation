import random
import time
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QGridLayout, QMessageBox, 
                             QComboBox, QDialog, QTableWidget, QTableWidgetItem,
                             QHeaderView, QFrame)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from .login_dialog import LoginDialog
from data_manager import DataManager

class MinesweeperWindow(QWidget):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.rows = 10
        self.cols = 10
        self.mines = 10
        self.map = []
        self.revealed = []
        self.flagged = []
        self.buttons = []
        self.game_over = False
        self.first_click = True
        self.start_time = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        
        self.init_ui()
        self.new_game()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 信息栏 - 紧凑布局
        info_layout = QHBoxLayout()
        info_layout.setSpacing(10)
        
        # 难度选择
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(['简单', '中等', '困难'])
        self.difficulty_combo.setMinimumWidth(80)
        self.difficulty_combo.currentIndexChanged.connect(self.change_difficulty)
        info_layout.addWidget(QLabel('难度:'))
        info_layout.addWidget(self.difficulty_combo)
        
        info_layout.addStretch()
        
        # 剩余雷数和时间 - 紧凑显示
        self.mines_label = QLabel('💣 10')
        self.mines_label.setStyleSheet('font-size: 16px; font-weight: bold; color: #333;')
        info_layout.addWidget(self.mines_label)
        
        self.time_label = QLabel('⏱️ 0秒')
        self.time_label.setStyleSheet('font-size: 16px; font-weight: bold; color: #333;')
        info_layout.addWidget(self.time_label)
        
        layout.addLayout(info_layout)
        
        # 游戏区域 - 居中
        game_container = QWidget()
        game_layout = QVBoxLayout(game_container)
        game_layout.setContentsMargins(0, 0, 0, 0)
        
        self.game_grid = QGridLayout()
        self.game_grid.setSpacing(1)
        self.game_grid.setContentsMargins(0, 0, 0, 0)
        game_layout.addLayout(self.game_grid)
        game_layout.addStretch()
        
        layout.addWidget(game_container, 1)
        
        # 按钮区域 - 紧凑
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(5)
        
        new_game_btn = QPushButton('🔄 新游戏')
        new_game_btn.setFixedHeight(35)
        new_game_btn.clicked.connect(self.new_game)
        btn_layout.addWidget(new_game_btn)
        
        back_btn = QPushButton('🏠 返回')
        back_btn.setFixedHeight(35)
        back_btn.clicked.connect(self.parent().show_main_menu)
        btn_layout.addWidget(back_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def change_difficulty(self, index):
        if index == 0:
            self.rows, self.cols, self.mines = 9, 9, 10
        elif index == 1:
            self.rows, self.cols, self.mines = 10, 10, 10
        else:
            self.rows, self.cols, self.mines = 16, 16, 40
        
        # 根据难度调整按钮大小
        btn_size = 35 if self.cols <= 10 else 28
        self.button_size = btn_size
        self.new_game()
    
    def new_game(self):
        self.game_over = False
        self.first_click = True
        self.start_time = None
        self.timer.stop()
        self.time_label.setText('⏱️ 0秒')
        
        # 根据难度设置按钮大小
        btn_size = 35 if self.cols <= 10 else 28
        self.button_size = btn_size
        
        # 初始化地图
        self.map = [[0] * self.cols for _ in range(self.rows)]
        self.revealed = [[False] * self.cols for _ in range(self.rows)]
        self.flagged = [[False] * self.cols for _ in range(self.rows)]
        
        # 创建按钮
        self.clear_buttons()
        for i in range(self.rows):
            for j in range(self.cols):
                btn = QPushButton('')
                btn.setFixedSize(btn_size, btn_size)
                btn.setStyleSheet('background-color: #e0e0e0; border: 1px solid #999; font-weight: bold; font-size: 12px;')
                btn.clicked.connect(lambda checked, r=i, c=j: self.on_click(r, c))
                # 重写鼠标事件以支持右键标记
                btn.mousePressEvent = lambda event, r=i, c=j: self.mouse_press_event(event, r, c)
                self.game_grid.addWidget(btn, i, j)
                self.buttons.append(btn)
        
        self.mines_remaining = self.mines
        self.mines_label.setText(f'💣 {self.mines_remaining}')
    
    def clear_buttons(self):
        for i in reversed(range(self.game_grid.count())):
            self.game_grid.itemAt(i).widget().deleteLater()
        self.buttons.clear()
    
    def mouse_press_event(self, event, row, col):
        """处理鼠标点击事件，支持左键和右键"""
        from PyQt5.QtCore import Qt
        if event.button() == Qt.RightButton:
            self.on_right_click(row, col)
        elif event.button() == Qt.LeftButton:
            self.on_click(row, col)
    
    def place_mines(self, first_row, first_col):
        # 随机放置地雷
        positions = [(i, j) for i in range(self.rows) for j in range(self.cols) 
                    if not (abs(i - first_row) <= 1 and abs(j - first_col) <= 1)]
        random.shuffle(positions)
        
        for i in range(self.mines):
            row, col = positions[i]
            self.map[row][col] = -1
        
        # 计算周围地雷数
        for i in range(self.rows):
            for j in range(self.cols):
                if self.map[i][j] != -1:
                    count = 0
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < self.rows and 0 <= nj < self.cols:
                                if self.map[ni][nj] == -1:
                                    count += 1
                    self.map[i][j] = count
    
    def on_click(self, row, col):
        if self.game_over or self.revealed[row][col]:
            return
        
        # 如果已标记，左键点击取消标记并翻开
        if self.flagged[row][col]:
            self.flagged[row][col] = False
            btn = self.buttons[row * self.cols + col]
            btn.setText('')
            btn.setStyleSheet('background-color: #e0e0e0; border: 1px solid #999; font-weight: bold; font-size: 12px;')
            self.mines_remaining += 1
            self.mines_label.setText(f'💣 {self.mines_remaining}')
            return
        
        if self.first_click:
            self.place_mines(row, col)
            self.first_click = False
            self.start_time = time.time()
            self.timer.start(1000)
        
        self.reveal_cell(row, col)
        self.check_win()
    
    def on_right_click(self, row, col, event=None):
        if self.game_over or self.revealed[row][col]:
            return
        
        self.flagged[row][col] = not self.flagged[row][col]
        btn = self.buttons[row * self.cols + col]
        
        if self.flagged[row][col]:
            btn.setText('🚩')
            btn.setStyleSheet('background-color: #ffcccc; border: 1px solid #999; font-size: 12px;')
            self.mines_remaining -= 1
        else:
            btn.setText('')
            btn.setStyleSheet('background-color: #e0e0e0; border: 1px solid #999; font-weight: bold; font-size: 12px;')
            self.mines_remaining += 1
        
        self.mines_label.setText(f'💣 {self.mines_remaining}')
    
    def reveal_cell(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            return
        if self.revealed[row][col] or self.flagged[row][col]:
            return
        
        self.revealed[row][col] = True
        btn = self.buttons[row * self.cols + col]
        
        if self.map[row][col] == -1:
            btn.setText('💣')
            btn.setStyleSheet('background-color: #ff6666; border: 1px solid #999; font-size: 12px;')
            self.game_over = True
            self.timer.stop()
            self.reveal_all_mines()
            QMessageBox.critical(self, '游戏结束', '你踩到了雷！')
            return
        
        if self.map[row][col] == 0:
            btn.setStyleSheet('background-color: #ffffff; border: 1px solid #999; font-weight: bold; font-size: 12px;')
            # 递归翻开周围的格子
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di != 0 or dj != 0:
                        self.reveal_cell(row + di, col + dj)
        else:
            btn.setText(str(self.map[row][col]))
            colors = ['', '#0000ff', '#008000', '#ff0000', '#000080', 
                     '#800000', '#008080', '#000000', '#808080']
            btn.setStyleSheet(f'background-color: #f5f5f5; border: 1px solid #999; color: {colors[self.map[row][col]]}; font-weight: bold; font-size: 14px;')
    
    def reveal_all_mines(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.map[i][j] == -1 and not self.flagged[i][j]:
                    btn = self.buttons[i * self.cols + j]
                    btn.setText('💣')
                    btn.setStyleSheet('background-color: #ff0000; font-size: 14px;')
                elif self.map[i][j] != -1 and self.flagged[i][j]:
                    btn = self.buttons[i * self.cols + j]
                    btn.setText('❌')
                    btn.setStyleSheet('background-color: #ffcccc; font-size: 14px;')
    
    def check_win(self):
        if self.game_over:
            return
        
        won = True
        for i in range(self.rows):
            for j in range(self.cols):
                if self.map[i][j] != -1 and not self.revealed[i][j]:
                    won = False
                    break
            if not won:
                break
        
        if won:
            self.game_over = True
            self.timer.stop()
            elapsed = int(time.time() - self.start_time)
            
            # 保存成绩
            DataManager.update_best_time(self.user['name'], elapsed)
            DataManager.save_score(self.user['name'], elapsed)
            
            QMessageBox.information(self, '恭喜', f'你赢了！\n用时: {elapsed}秒')
    
    def update_time(self):
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            self.time_label.setText(f'时间: {elapsed}秒')

class RankingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('排行榜')
        self.setFixedSize(500, 400)
        
        layout = QVBoxLayout()
        
        label = QLabel('排行榜 - 最佳成绩')
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet('font-size: 18px; font-weight: bold; margin: 10px;')
        layout.addWidget(label)
        
        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['排名', '用户名', '时间(秒)'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        # 加载数据
        self.load_data()
        
        # 关闭按钮
        close_btn = QPushButton('关闭')
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def load_data(self):
        users = DataManager.load_users()
        
        # 按最佳成绩排序
        valid_users = [u for u in users if u.get('best_time', -1) != -1]
        valid_users.sort(key=lambda x: x.get('best_time', float('inf')))
        
        self.table.setRowCount(len(valid_users))
        
        for i, user in enumerate(valid_users):
            self.table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.table.setItem(i, 1, QTableWidgetItem(user['name']))
            self.table.setItem(i, 2, QTableWidgetItem(str(user['best_time'])))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.current_widget = None
        self.init_ui()
        self.show_login()
    
    def init_ui(self):
        self.setWindowTitle('扫雷游戏 - PyQt5版本')
        self.setMinimumSize(600, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
    
    def show_login(self):
        dialog = LoginDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.current_user = dialog.current_user
            self.show_main_menu()
        else:
            QApplication.quit()
    
    def show_main_menu(self):
        if self.current_widget:
            self.main_layout.removeWidget(self.current_widget)
            self.current_widget.deleteLater()
        
        self.current_widget = QWidget()
        layout = QVBoxLayout()
        
        # 标题
        title = QLabel('扫雷游戏')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 32px; font-weight: bold; margin: 40px;')
        layout.addWidget(title)
        
        # 欢迎信息
        welcome = QLabel(f'欢迎, {self.current_user["name"]}!')
        welcome.setAlignment(Qt.AlignCenter)
        welcome.setStyleSheet('font-size: 18px; margin: 20px;')
        layout.addWidget(welcome)
        
        # 按钮
        btn_layout = QHBoxLayout()
        
        game_btn = QPushButton('开始游戏')
        game_btn.setFixedSize(150, 50)
        game_btn.setStyleSheet('font-size: 16px;')
        game_btn.clicked.connect(self.show_game)
        btn_layout.addWidget(game_btn)
        
        rank_btn = QPushButton('排行榜')
        rank_btn.setFixedSize(150, 50)
        rank_btn.setStyleSheet('font-size: 16px;')
        rank_btn.clicked.connect(self.show_ranking)
        btn_layout.addWidget(rank_btn)
        
        layout.addLayout(btn_layout)
        
        # 注销按钮
        logout_btn = QPushButton('退出登录')
        logout_btn.setFixedSize(150, 50)
        logout_btn.setStyleSheet('font-size: 16px; margin-top: 20px;')
        logout_btn.clicked.connect(self.show_login)
        layout.addWidget(logout_btn, 0, Qt.AlignCenter)
        
        layout.addStretch()
        
        self.current_widget.setLayout(layout)
        self.main_layout.addWidget(self.current_widget)
    
    def show_game(self):
        if self.current_widget:
            self.main_layout.removeWidget(self.current_widget)
            self.current_widget.deleteLater()
        
        self.current_widget = MinesweeperWindow(self.current_user, self)
        self.main_layout.addWidget(self.current_widget)
    
    def show_ranking(self):
        dialog = RankingDialog(self)
        dialog.exec_()
