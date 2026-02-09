"""
俄罗斯方块游戏 - PyQt5桌面版
"""
import sys
import random
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFrame, QMessageBox, QApplication)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QKeyEvent


class TetrisGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_game()

    def init_game(self):
        self.setWindowTitle('俄罗斯方块 - PyQt5版')
        self.setGeometry(100, 100, 500, 600)
        self.setFocusPolicy(Qt.StrongFocus)  # 强制获取焦点

        # 游戏配置
        self.board_width = 10
        self.board_height = 20
        self.block_size = 30

        # 初始化游戏板
        self.board = [[0] * self.board_width for _ in range(self.board_height)]

        # 方块形状定义（7种形状，每种4个旋转状态）
        self.shapes = [
            # I形
            [
                [[1, 1, 1, 1]],
                [[1], [1], [1], [1]],
                [[1, 1, 1, 1]],
                [[1], [1], [1], [1]]
            ],
            # J形 - 倒L（三横一竖，竖在右下）
            [
                [[1, 1, 1], [0, 0, 1]],  # 横向，竖在右
                [[0, 0, 1], [0, 0, 1], [0, 1, 1]],  
                [[1, 0, 0], [1, 1, 1]],  
                [[1, 1, 0], [1, 0, 0], [1, 0, 0]]  # 竖向，凸出在上
            ],
            # L形 - 三横一竖，竖在左下
            [
                [[1, 1, 1], [1, 0, 0]],  # 横向，竖在左
                [[0, 1, 1], [0, 0, 1], [0, 0, 1]],  
                [[0, 0, 1], [1, 1, 1]],  # 横向，竖在右
                [[1, 0, 0], [1, 0, 0], [1, 1, 0]]  # 竖向，凸出在中
            ],
            # O形
            [
                [[1, 1], [1, 1]],
                [[1, 1], [1, 1]],
                [[1, 1], [1, 1]],
                [[1, 1], [1, 1]]
            ],
            # S形
            [
                [[0, 1, 1], [1, 1, 0]],
                [[1, 0], [1, 1], [0, 1]],
                [[0, 1, 1], [1, 1, 0]],
                [[1, 0], [1, 1], [0, 1]]
            ],
            # T形
            [
                [[0, 1, 0], [1, 1, 1]],
                [[1, 0], [1, 1], [1, 0]],
                [[1, 1, 1], [0, 1, 0]],
                [[0, 1], [1, 1], [0, 1]]
            ],
            # Z形
            [
                [[1, 1, 0], [0, 1, 1]],
                [[0, 1], [1, 1], [1, 0]],
                [[1, 1, 0], [0, 1, 1]],
                [[0, 1], [1, 1], [1, 0]]
            ]
        ]
        self.colors = [
            QColor(0, 255, 255),    # 青 - I
            QColor(0, 0, 255),      # 蓝 - J
            QColor(255, 165, 0),    # 橙 - L
            QColor(255, 255, 0),    # 黄 - O
            QColor(0, 255, 0),      # 绿 - S
            QColor(128, 0, 128),    # 紫 - T
            QColor(255, 0, 0)       # 红 - Z
        ]

        # 游戏状态
        self.current_piece_index = 0
        self.current_rotation = 0
        self.current_x = 0
        self.current_y = 0
        self.next_piece_index = 0
        self.next_rotation = 0
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False

        # 创建UI
        self.create_ui()

        # 先生成下一个方块，再生成当前方块
        self.next_piece_index = random.randint(0, len(self.shapes) - 1)
        self.next_rotation = 0
        self.new_piece()

        # 设置定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.game_step)
        self.timer.start(1000 // self.level)

    def create_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)

        # 游戏区域
        self.game_area = GameArea(self)
        self.game_area.setFocusPolicy(Qt.StrongFocus)
        layout.addWidget(self.game_area, 2)

        # 信息面板
        info_panel = QWidget()
        info_layout = QVBoxLayout(info_panel)

        # 下一个方块
        info_layout.addWidget(QLabel('下一个方块:'))
        self.next_piece_area = NextPieceArea(self)
        info_layout.addWidget(self.next_piece_area)
        info_layout.addSpacing(20)

        # 分数
        info_layout.addWidget(QLabel('分数:'))
        self.score_label = QLabel('0')
        self.score_label.setStyleSheet('font-size: 24px; font-weight: bold;')
        info_layout.addWidget(self.score_label)
        info_layout.addSpacing(20)

        # 等级
        info_layout.addWidget(QLabel('等级:'))
        self.level_label = QLabel('1')
        self.level_label.setStyleSheet('font-size: 24px; font-weight: bold;')
        info_layout.addWidget(self.level_label)
        info_layout.addSpacing(20)

        # 行数
        info_layout.addWidget(QLabel('消除行数:'))
        self.lines_label = QLabel('0')
        self.lines_label.setStyleSheet('font-size: 24px; font-weight: bold;')
        info_layout.addWidget(self.lines_label)
        info_layout.addStretch()

        # 控制按钮
        self.pause_btn = QPushButton('暂停')
        self.pause_btn.clicked.connect(self.toggle_pause)
        info_layout.addWidget(self.pause_btn)

        self.restart_btn = QPushButton('重新开始')
        self.restart_btn.clicked.connect(self.restart_game)
        info_layout.addWidget(self.restart_btn)

        layout.addWidget(info_panel, 1)

        # 添加说明
        self.add_instructions()

    def add_instructions(self):
        """添加操作说明"""
        status_bar = self.statusBar()
        status_bar.showMessage('↑:旋转  ←:左移  →:右移  ↓:加速  空格:暂停')

    def new_piece(self):
        """生成新方块"""
        self.current_piece_index = self.next_piece_index
        self.current_rotation = 0  # 新方块总是从初始旋转状态开始

        shape = self.shapes[self.current_piece_index][self.current_rotation]
        self.current_x = (self.board_width - len(shape[0])) // 2
        self.current_y = 0

        # 生成下一个方块
        self.next_piece_index = random.randint(0, len(self.shapes) - 1)
        self.next_rotation = 0

        # 检查游戏结束
        if self.check_collision(self.current_x, self.current_y, self.current_rotation):
            self.game_over = True
            self.timer.stop()
            QMessageBox.information(self, '游戏结束', f'游戏结束！\n最终得分: {self.score}')
            self.next_piece_area.update_piece(self.next_piece_index, self.next_rotation)

        self.next_piece_area.update_piece(self.next_piece_index, self.next_rotation)

    def rotate_piece(self):
        """旋转方块"""
        if self.current_piece_index == 3:  # O形不需要旋转
            return

        new_rotation = (self.current_rotation + 1) % 4

        if not self.check_collision(self.current_x, self.current_y, new_rotation):
            self.current_rotation = new_rotation
            self.game_area.update()

    def check_collision(self, x, y, rotation):
        """检查碰撞"""
        shape = self.shapes[self.current_piece_index][rotation]

        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j]:
                    new_x = x + j
                    new_y = y + i

                    if (new_x < 0 or new_x >= self.board_width or
                        new_y >= self.board_height):
                        return True

                    if new_y >= 0 and self.board[new_y][new_x]:
                        return True
        return False

    def lock_piece(self):
        """固定方块到游戏板"""
        shape = self.shapes[self.current_piece_index][self.current_rotation]
        color = self.colors[self.current_piece_index]

        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j]:
                    board_y = self.current_y + i
                    board_x = self.current_x + j
                    if board_y >= 0:
                        self.board[board_y][board_x] = color

        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        """消除满行"""
        lines = 0

        for y in range(self.board_height - 1, -1, -1):
            full = True
            for x in range(self.board_width):
                if not self.board[y][x]:
                    full = False
                    break

            if full:
                lines += 1
                for yy in range(y, 0, -1):
                    self.board[yy] = self.board[yy - 1].copy()
                self.board[0] = [0] * self.board_width
                y += 1

        if lines > 0:
            self.lines_cleared += lines
            self.score += lines * lines * 100 * self.level
            self.level = self.lines_cleared // 10 + 1

            self.score_label.setText(str(self.score))
            self.level_label.setText(str(self.level))
            self.lines_label.setText(str(self.lines_cleared))

            self.timer.setInterval(1000 // self.level)

    def game_step(self):
        """游戏步骤"""
        if not self.paused and not self.game_over:
            old_y = self.current_y
            self.current_y += 1

            if self.check_collision(self.current_x, self.current_y, self.current_rotation):
                self.current_y = old_y
                self.lock_piece()

            self.game_area.update()

    def toggle_pause(self):
        """切换暂停状态"""
        self.paused = not self.paused
        self.pause_btn.setText('继续' if self.paused else '暂停')

    def restart_game(self):
        """重新开始游戏"""
        self.board = [[0] * self.board_width for _ in range(self.board_height)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False

        self.score_label.setText('0')
        self.level_label.setText('1')
        self.lines_label.setText('0')
        self.pause_btn.setText('暂停')

        self.new_piece()
        self.next_piece_index = random.randint(0, len(self.shapes) - 1)
        self.next_rotation = 0
        self.next_piece_area.update_piece(self.next_piece_index, self.next_rotation)

        self.timer.setInterval(1000 // self.level)
        self.timer.start()
        self.game_area.update()

    def keyPressEvent(self, event: QKeyEvent):
        """处理键盘事件"""
        if self.game_over:
            return

        if event.key() == Qt.Key_Left:
            if not self.check_collision(self.current_x - 1, self.current_y, self.current_rotation):
                self.current_x -= 1
                self.game_area.update()

        elif event.key() == Qt.Key_Right:
            if not self.check_collision(self.current_x + 1, self.current_y, self.current_rotation):
                self.current_x += 1
                self.game_area.update()

        elif event.key() == Qt.Key_Down:
            if not self.check_collision(self.current_x, self.current_y + 1, self.current_rotation):
                self.current_y += 1
                self.game_area.update()

        elif event.key() == Qt.Key_Up:
            self.rotate_piece()

        elif event.key() == Qt.Key_Space:
            self.toggle_pause()

        # 传递事件到父类，确保焦点处理
        super().keyPressEvent(event)


class GameArea(QWidget):
    def __init__(self, game_window):
        super().__init__()
        self.game_window = game_window
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFixedSize(
            game_window.board_width * game_window.block_size,
            game_window.board_height * game_window.block_size
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.black)

        game = self.game_window

        # 绘制已固定的方块
        for y in range(game.board_height):
            for x in range(game.board_width):
                if game.board[y][x]:
                    self.draw_block(painter, x, y, game.board[y][x])

        # 绘制当前方块
        if not game.game_over:
            shape = game.shapes[game.current_piece_index][game.current_rotation]
            color = game.colors[game.current_piece_index]
            for i in range(len(shape)):
                for j in range(len(shape[0])):
                    if shape[i][j]:
                        self.draw_block(painter, game.current_x + j, game.current_y + i, color)

    def draw_block(self, painter, x, y, color):
        """绘制单个方块"""
        size = self.game_window.block_size
        painter.fillRect(x * size, y * size, size, size, color)
        painter.setPen(QColor(255, 255, 255))
        painter.drawRect(x * size, y * size, size, size)


class NextPieceArea(QFrame):
    def __init__(self, game_window):
        super().__init__()
        self.game_window = game_window
        self.piece_index = None
        self.piece_rotation = 0
        self.setFixedSize(120, 120)
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet('border: 2px solid gray;')

    def update_piece(self, piece_index, rotation):
        """更新下一个方块"""
        self.piece_index = piece_index
        self.piece_rotation = rotation
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.black)

        if self.piece_index is not None:
            shape = self.game_window.shapes[self.piece_index][self.piece_rotation]
            color = self.game_window.colors[self.piece_index]
            block_size = 25

            rows = len(shape)
            cols = len(shape[0])
            start_x = (120 - cols * block_size) // 2
            start_y = (120 - rows * block_size) // 2

            for i in range(rows):
                for j in range(cols):
                    if shape[i][j]:
                        painter.fillRect(
                            start_x + j * block_size,
                            start_y + i * block_size,
                            block_size,
                            block_size,
                            color
                        )
                        painter.setPen(QColor(255, 255, 255))
                        painter.drawRect(
                            start_x + j * block_size,
                            start_y + i * block_size,
                            block_size,
                            block_size
                        )


def main():
    app = QApplication(sys.argv)
    game = TetrisGame()
    game.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
