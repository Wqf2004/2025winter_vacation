import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QGridLayout, QMessageBox, 
                             QComboBox, QDialog, QTableWidget, QTableWidgetItem,
                             QHeaderView, QFrame, QButtonGroup, QRadioButton)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont
from data_manager import DataManager

# 棋子颜色
EMPTY = 0
BLACK = 1
WHITE = 2

# 方向数组
DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]

class GomokuBoard(QWidget):
    # 信号
    move_made = pyqtSignal(int, int, int)  # x, y, color
    game_over = pyqtSignal(int)  # winner
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.board_size = 15
        self.cell_size = 30
        self.margin = 20
        
        # 棋盘状态
        self.board = [[EMPTY for _ in range(self.board_size)] 
                      for _ in range(self.board_size)]
        self.moves = []
        self.game_mode = 0  # 0: 人-人, 1: 人-计, 2: 计-人
        self.current_player = BLACK
        self.game_over_flag = False
        self.ai_enabled = False
        
        # 鼠标位置
        self.mouse_pos = QPoint(-1, -1)
        
        self.setMinimumSize(self.board_size * self.cell_size + 2 * self.margin,
                           self.board_size * self.cell_size + 2 * self.margin)
        self.setMouseTracking(True)
    
    def reset_board(self, size=15):
        """重置棋盘"""
        self.board_size = size
        self.board = [[EMPTY for _ in range(self.board_size)] 
                      for _ in range(self.board_size)]
        self.moves = []
        self.current_player = BLACK
        self.game_over_flag = False
        self.mouse_pos = QPoint(-1, -1)
        self.setMinimumSize(self.board_size * self.cell_size + 2 * self.margin,
                           self.board_size * self.cell_size + 2 * self.margin)
        self.update()
    
    def set_game_mode(self, mode):
        """设置游戏模式"""
        self.game_mode = mode
        self.ai_enabled = mode in [1, 2]
        
        # 如果是计算机先手
        if mode == 2 and not self.moves:
            self.ai_move()
    
    def paintEvent(self, event):
        """绘制棋盘"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制背景
        painter.fillRect(self.rect(), QColor(220, 179, 92))
        
        # 绘制网格线
        pen = QPen(QColor(0, 0, 0), 1)
        painter.setPen(pen)
        
        for i in range(self.board_size):
            # 横线
            x1 = self.margin
            y1 = self.margin + i * self.cell_size
            x2 = self.margin + (self.board_size - 1) * self.cell_size
            y2 = y1
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
            
            # 竖线
            x1 = self.margin + i * self.cell_size
            y1 = self.margin
            x2 = x1
            y2 = self.margin + (self.board_size - 1) * self.cell_size
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
        
        # 绘制星位点
        if self.board_size == 15:
            stars = [(3, 3), (11, 3), (7, 7), (3, 11), (11, 11)]
            for x, y in stars:
                center_x = self.margin + x * self.cell_size
                center_y = self.margin + y * self.cell_size
                painter.setBrush(QBrush(QColor(0, 0, 0)))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QPoint(int(center_x), int(center_y)), 3, 3)
        
        # 绘制棋子
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[y][x] != EMPTY:
                    center_x = self.margin + x * self.cell_size
                    center_y = self.margin + y * self.cell_size
                    radius = self.cell_size * 0.4
                    
                    if self.board[y][x] == BLACK:
                        painter.setBrush(QBrush(QColor(0, 0, 0)))
                    else:
                        painter.setBrush(QBrush(QColor(255, 255, 255)))
                    
                    painter.setPen(QPen(QColor(100, 100, 100), 1))
                    painter.drawEllipse(QPoint(int(center_x), int(center_y)), 
                                       int(radius), int(radius))
                    
                    # 标记最后一步
                    if self.moves and self.moves[-1]['x'] == x and self.moves[-1]['y'] == y:
                        painter.setPen(QPen(QColor(255, 0, 0), 2))
                        painter.drawPoint(QPoint(int(center_x), int(center_y)))
        
        # 绘制鼠标预览
        if not self.game_over_flag and self.mouse_pos.x() >= 0:
            grid_x = round((self.mouse_pos.x() - self.margin) / self.cell_size)
            grid_y = round((self.mouse_pos.y() - self.margin) / self.cell_size)
            
            if 0 <= grid_x < self.board_size and 0 <= grid_y < self.board_size:
                if self.board[grid_y][grid_x] == EMPTY:
                    center_x = self.margin + grid_x * self.cell_size
                    center_y = self.margin + grid_y * self.cell_size
                    radius = self.cell_size * 0.4 * 0.5
                    
                    if self.current_player == BLACK:
                        painter.setBrush(QBrush(QColor(0, 0, 0, 100)))
                    else:
                        painter.setBrush(QBrush(QColor(255, 255, 255, 100)))
                    
                    painter.setPen(Qt.NoPen)
                    painter.drawEllipse(QPoint(int(center_x), int(center_y)), 
                                       int(radius), int(radius))
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        self.mouse_pos = event.pos()
        self.update()
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if self.game_over_flag:
            return
        
        # AI的回合不允许玩家下棋
        if self.ai_enabled and ((self.game_mode == 1 and self.current_player == WHITE) or 
                               (self.game_mode == 2 and self.current_player == BLACK)):
            return
        
        if event.button() == Qt.LeftButton:
            grid_x = round((event.x() - self.margin) / self.cell_size)
            grid_y = round((event.y() - self.margin) / self.cell_size)
            
            if 0 <= grid_x < self.board_size and 0 <= grid_y < self.board_size:
                if self.board[grid_y][grid_x] == EMPTY:
                    self.make_move(grid_x, grid_y, self.current_player)
    
    def make_move(self, x, y, color):
        """落子"""
        self.board[y][x] = color
        self.moves.append({'x': x, 'y': y, 'color': color})
        self.move_made.emit(x, y, color)
        
        # 检查胜负
        winner = self.check_winner(x, y, color)
        if winner:
            self.game_over_flag = True
            self.game_over.emit(winner)
        else:
            # 切换玩家
            self.current_player = WHITE if color == BLACK else BLACK
            self.update()
            
            # AI下棋
            if self.ai_enabled and not self.game_over_flag:
                if (self.game_mode == 1 and self.current_player == WHITE) or \
                   (self.game_mode == 2 and self.current_player == BLACK):
                    QTimer.singleShot(500, self.ai_move)
    
    def ai_move(self):
        """AI下棋"""
        if self.game_over_flag:
            return
        
        # 第一步下在中心
        if not self.moves:
            center = self.board_size // 2
            self.make_move(center, center, self.current_player)
            return
        
        # 计算最佳位置
        best_score = -1
        best_pos = None
        
        center = self.board_size // 2
        
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[y][x] == EMPTY:
                    score = self.calc_value(x, y, self.current_player)
                    
                    # 位置权重（靠近中心）
                    score += (center - abs(center - x)) * (center - abs(center - y))
                    
                    if score > best_score:
                        best_score = score
                        best_pos = (x, y)
        
        if best_pos:
            self.make_move(best_pos[0], best_pos[1], self.current_player)
    
    def calc_value(self, x, y, color):
        """计算位置价值"""
        opponent = WHITE if color == BLACK else BLACK
        values = [0, 100, 600, 6000, 40000]
        total_score = 0
        
        for dx, dy in DIRECTIONS:
            # 进攻
            count = 1
            blocked = 0
            
            for i in range(1, 5):
                nx, ny = x + i * dx, y + i * dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if self.board[ny][nx] == color:
                        count += 1
                    elif self.board[ny][nx] == EMPTY:
                        break
                    else:
                        blocked += 1
                        break
                else:
                    blocked += 1
                    break
            
            for i in range(1, 5):
                nx, ny = x - i * dx, y - i * dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if self.board[ny][nx] == color:
                        count += 1
                    elif self.board[ny][nx] == EMPTY:
                        break
                    else:
                        blocked += 1
                        break
                else:
                    blocked += 1
                    break
            
            if count >= 5:
                return 100000
            if count <= 4:
                total_score += values[count] * (2 - blocked)
            
            # 防守
            block_count = 1
            for i in range(1, 5):
                nx, ny = x + i * dx, y + i * dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if self.board[ny][nx] == opponent:
                        block_count += 1
                    else:
                        break
                else:
                    break
            
            for i in range(1, 5):
                nx, ny = x - i * dx, y - i * dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if self.board[ny][nx] == opponent:
                        block_count += 1
                    else:
                        break
                else:
                    break
            
            if block_count >= 3 and block_count < len(values):
                total_score += values[block_count] // 2
        
        return total_score
    
    def check_winner(self, x, y, color):
        """检查胜负"""
        for dx, dy in DIRECTIONS:
            count = 1
            
            # 正方向
            for i in range(1, 5):
                nx, ny = x + i * dx, y + i * dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if self.board[ny][nx] == color:
                        count += 1
                    else:
                        break
                else:
                    break
            
            # 反方向
            for i in range(1, 5):
                nx, ny = x - i * dx, y - i * dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if self.board[ny][nx] == color:
                        count += 1
                    else:
                        break
                else:
                    break
            
            if count >= 5:
                return color
        
        return None
    
    def undo_move(self):
        """悔棋"""
        if len(self.moves) >= 2:
            # 撤销两步（如果是对战模式）
            if self.game_mode == 0:
                for _ in range(2):
                    if self.moves:
                        move = self.moves.pop()
                        self.board[move['y']][move['x']] = EMPTY
                self.current_player = BLACK if len(self.moves) % 2 == 0 else WHITE
            else:
                # AI模式下撤销一步
                move = self.moves.pop()
                self.board[move['y']][move['x']] = EMPTY
                self.current_player = BLACK
        elif len(self.moves) == 1:
            move = self.moves.pop()
            self.board[move['y']][move['x']] = EMPTY
            self.current_player = BLACK
        
        self.game_over_flag = False
        self.update()
    
    def load_game(self, board_size, moves):
        """加载游戏"""
        self.reset_board(board_size)
        for move in moves:
            x, y, color = move['x'], move['y'], move['color']
            self.board[y][x] = color
            self.moves.append(move)
            self.current_player = WHITE if color == BLACK else BLACK
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('五子棋游戏 - PyQt5版本')
        self.setMinimumSize(800, 700)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        
        # 标题
        title = QLabel('五子棋游戏')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 24px; font-weight: bold; margin: 10px;')
        layout.addWidget(title)
        
        # 信息栏
        info_layout = QHBoxLayout()
        
        # 模式选择
        mode_group = QButtonGroup(self)
        self.mode_pvp = QRadioButton('人-人')
        self.mode_pva = QRadioButton('人-计')
        self.mode_avp = QRadioButton('计-人')
        self.mode_pvp.setChecked(True)
        mode_group.addButton(self.mode_pvp, 0)
        mode_group.addButton(self.mode_pva, 1)
        mode_group.addButton(self.mode_avp, 2)
        
        info_layout.addWidget(QLabel('模式:'))
        info_layout.addWidget(self.mode_pvp)
        info_layout.addWidget(self.mode_pva)
        info_layout.addWidget(self.mode_avp)
        
        info_layout.addStretch()
        
        # 当前玩家
        self.current_player_label = QLabel('当前: 黑方')
        self.current_player_label.setStyleSheet('font-size: 14px; font-weight: bold;')
        info_layout.addWidget(self.current_player_label)
        
        # 步数
        self.move_count_label = QLabel('步数: 0')
        self.move_count_label.setStyleSheet('font-size: 14px;')
        info_layout.addWidget(self.move_count_label)
        
        layout.addLayout(info_layout)
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        # 棋盘
        self.board = GomokuBoard()
        self.board.move_made.connect(self.on_move_made)
        self.board.game_over.connect(self.on_game_over)
        
        board_container = QWidget()
        board_layout = QHBoxLayout(board_container)
        board_layout.addStretch()
        board_layout.addWidget(self.board)
        board_layout.addStretch()
        layout.addWidget(board_container, 1)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        
        new_game_btn = QPushButton('新游戏')
        new_game_btn.clicked.connect(self.new_game)
        new_game_btn.setFixedSize(100, 35)
        btn_layout.addWidget(new_game_btn)
        
        undo_btn = QPushButton('悔棋')
        undo_btn.clicked.connect(self.undo_move)
        undo_btn.setFixedSize(100, 35)
        btn_layout.addWidget(undo_btn)
        
        save_btn = QPushButton('保存')
        save_btn.clicked.connect(self.save_game)
        save_btn.setFixedSize(100, 35)
        btn_layout.addWidget(save_btn)
        
        load_btn = QPushButton('读取')
        load_btn.clicked.connect(self.load_game)
        load_btn.setFixedSize(100, 35)
        btn_layout.addWidget(load_btn)
        
        layout.addLayout(btn_layout)
    
    def new_game(self):
        """新游戏"""
        mode = 0
        if self.mode_pva.isChecked():
            mode = 1
        elif self.mode_avp.isChecked():
            mode = 2
        
        self.board.reset_board()
        self.board.set_game_mode(mode)
        self.update_info()
    
    def undo_move(self):
        """悔棋"""
        self.board.undo_move()
        self.update_info()
    
    def save_game(self):
        """保存游戏"""
        DataManager.save_game(self.board.moves, self.board.board_size)
        QMessageBox.information(self, '成功', '游戏已保存！')
    
    def load_game(self):
        """读取游戏"""
        board_size, moves = DataManager.load_game()
        if moves:
            self.board.load_game(board_size, moves)
            # 设置为对战模式
            self.mode_pvp.setChecked(True)
            self.board.game_mode = 0
            self.board.ai_enabled = False
            self.update_info()
            QMessageBox.information(self, '成功', '游戏已读取！')
        else:
            QMessageBox.warning(self, '警告', '没有存档！')
    
    def on_move_made(self, x, y, color):
        """落子事件"""
        self.update_info()
    
    def on_game_over(self, winner):
        """游戏结束事件"""
        winner_name = '黑方' if winner == BLACK else '白方'
        QMessageBox.information(self, '游戏结束', f'{winner_name}获胜！\n是否保存对局？')
        
        # 询问是否保存
        reply = QMessageBox.question(self, '保存', '是否保存对局记录？',
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            DataManager.save_game(self.board.moves, self.board.board_size)
            QMessageBox.information(self, '成功', '游戏已保存！')
    
    def update_info(self):
        """更新信息"""
        player_name = '黑方' if self.board.current_player == BLACK else '白方'
        self.current_player_label.setText(f'当前: {player_name}')
        self.move_count_label.setText(f'步数: {len(self.board.moves)}')
