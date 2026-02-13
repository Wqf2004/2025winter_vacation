# ./ui/main_window.py
"""
俄罗斯方块游戏 - PyQt5桌面版
集成AI引擎和深度学习评估
"""
import sys
import random
import io
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
                             QPushButton, QLabel, QFrame, QMessageBox, QApplication,
                             QComboBox, QDialog, QTextEdit, QProgressBar, QGroupBox)
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QKeyEvent
from ai_engine import TetrisAI, GameState, Solution


class TrainingDialog(QDialog):
    """训练进度和状态显示对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('AI训练状态')
        self.setGeometry(200, 200, 600, 700)
        self.init_ui()

    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()

        # 训练统计信息
        stats_group = QGroupBox("训练统计")
        stats_layout = QVBoxLayout()

        self.stage_label = QLabel("训练阶段: 静态")
        self.progress_label = QLabel("训练进度: 0%")
        self.samples_label = QLabel("训练样本数: 0")
        self.decisions_label = QLabel("人类决策总数: 0")
        self.rejection_label = QLabel("拒绝AI建议: 0 (0%)")

        stats_layout.addWidget(self.stage_label)
        stats_layout.addWidget(self.progress_label)
        stats_layout.addWidget(self.samples_label)
        stats_layout.addWidget(self.decisions_label)
        stats_layout.addWidget(self.rejection_label)
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        # 权重信息
        weights_group = QGroupBox("当前评分权重")
        weights_layout = QVBoxLayout()

        self.weight_info_label = QLabel("使用静态权重")
        weight_details = (
            "消除行数: +300\n"
            "落点高度: +15/行 (正向奖励)\n"
            "空洞数量: -20/个 (强惩罚)\n"
            "最高点: -3/行\n"
            "总高度: -1/格\n"
            "不平整度: -1/差\n"
            "接近完成: +50/行\n"
            "底层覆盖: +5/列\n"
            "下块友好: +10/位"
        )
        self.weight_details_label = QLabel(weight_details)
        self.weight_details_label.setStyleSheet("QLabel { font-family: monospace; }")

        weights_layout.addWidget(self.weight_info_label)
        weights_layout.addWidget(self.weight_details_label)
        weights_group.setLayout(weights_layout)
        layout.addWidget(weights_group)

        # 训练日志
        log_group = QGroupBox("训练日志")
        log_layout = QVBoxLayout()

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setPlainText("等待训练开始...")
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

        # 按钮
        button_layout = QHBoxLayout()

        self.train_button = QPushButton("开始训练")
        self.train_button.clicked.connect(self.start_training)
        button_layout.addWidget(self.train_button)

        self.save_button = QPushButton("保存模型")
        self.save_button.clicked.connect(self.save_model)
        button_layout.addWidget(self.save_button)

        self.load_button = QPushButton("加载模型")
        self.load_button.clicked.connect(self.load_model)
        button_layout.addWidget(self.load_button)

        self.save_data_button = QPushButton("保存数据")
        self.save_data_button.clicked.connect(self.save_training_data)
        button_layout.addWidget(self.save_data_button)

        self.load_data_button = QPushButton("加载数据")
        self.load_data_button.clicked.connect(self.load_training_data)
        button_layout.addWidget(self.load_data_button)

        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def set_ai(self, ai: TetrisAI):
        """设置AI对象"""
        self.ai = ai
        self.update_info()

    def update_info(self):
        """更新显示信息"""
        stats = self.ai.get_training_statistics()

        self.stage_label.setText(f"训练阶段: {stats['stage']}")
        self.progress_label.setText(f"训练进度: {stats['progress_ratio']:.1%}")
        self.samples_label.setText(f"训练样本数: {stats['training_samples']}")
        self.decisions_label.setText(f"人类决策总数: {stats['total_human_decisions']}")

        rejection_rate = stats['human_rejected_ai'] / max(stats['total_human_decisions'], 1) * 100
        self.rejection_label.setText(f"学习人类决策: {stats['human_rejected_ai']} ({rejection_rate:.1f}%)")

        if stats['stage'] == 'static':
            self.weight_info_label.setText("使用静态权重")
        elif stats['stage'] == 'hybrid':
            self.weight_info_label.setText(f"使用混合权重 (静态 {1-stats['progress_ratio']:.0%} + 学习 {stats['progress_ratio']:.0%})")
        else:
            self.weight_info_label.setText("使用学习权重")

    def start_training(self):
        """开始训练"""
        self.log_text.append("\n开始训练...")
        self.train_button.setEnabled(False)

        result = self.ai.train_model(epochs=20)

        self.update_info()

        if result['success']:
            self.log_text.append(f"训练完成!")
            self.log_text.append(f"使用样本: {result['samples_used']}")
            self.log_text.append(f"平均损失: {result['avg_loss']:.4f}")
            self.log_text.append(f"当前阶段: {result['stage']}")
            self.log_text.append(f"训练进度: {result['progress_ratio']:.1%}")
            if result['stage_changed']:
                self.log_text.append("✓ 阶段已升级!")
        else:
            self.log_text.append(f"训练失败: {result['message']}")

        self.train_button.setEnabled(True)

    def save_model(self):
        """保存模型"""
        import os
        model_dir = "models"
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        model_path = f"{model_dir}/tetris_ai_model.npy"
        self.ai.save_model(model_path)
        self.log_text.append(f"\n模型已保存到: {model_path}")

    def load_model(self):
        """加载模型"""
        import os
        model_dir = "models"
        model_path = f"{model_dir}/tetris_ai_model.npy"

        if os.path.exists(model_path):
            self.ai.load_model(model_path)
            self.update_info()
            self.log_text.append(f"\n模型已从 {model_path} 加载")
        else:
            self.log_text.append(f"\n模型文件不存在: {model_path}")

    def save_training_data(self):
        """保存训练数据"""
        import os
        data_dir = "training_data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        data_path = f"{data_dir}/tetris_training_data.json"
        self.ai.save_training_data(data_path)
        self.log_text.append(f"\n训练数据已保存到: {data_path}")

    def load_training_data(self):
        """加载训练数据"""
        import os
        data_dir = "training_data"
        data_path = f"{data_dir}/tetris_training_data.json"

        if os.path.exists(data_path):
            loaded_count = self.ai.load_training_data(data_path)
            self.update_info()
            self.log_text.append(f"\n已从 {data_path} 加载 {loaded_count} 个训练样本")
        else:
            self.log_text.append(f"\n训练数据文件不存在: {data_path}")




# 设置stdout为UTF-8编码以支持中文输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


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
            # J形 - 倒L（三横一竖，竖在右）
            [
                [[1, 1, 1], [0, 0, 1]],  # 横向，竖在右
                [[0, 1],
                 [0, 1],
                 [1, 1]],               # 竖向，竖在下（旋转90度）
                [[1, 0, 0], [1, 1, 1]],  # 横向，竖在左（旋转180度）
                [[1, 1],
                 [1, 0],
                 [1, 0]]                # 竖向，竖在上（旋转270度）
            ],
            # L形 - 三横一竖，竖在左
            [
                [[1, 1, 1], [1, 0, 0]],  # 横向，竖在左
                [[1, 1],
                 [0, 1],
                 [0, 1]],               # 竖向，竖在下（旋转90度）
                [[0, 0, 1], [1, 1, 1]],  # 横向，竖在右（旋转180度）
                [[1, 0],
                 [1, 0],
                 [1, 1]]                # 竖向，竖在上（旋转270度）
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
        self.piece_count = 0  # 方块计数（用于游戏轮次）

        # AI系统
        self.ai = TetrisAI()
        self.ai_enabled = False
        self.ai_mode = 'off'  # off, assist, auto
        self.last_human_move = None  # 记录最后一次人类移动
        self.ai_suggestion = None  # AI建议的解
        self.ai_suggestion_piece_index = -1  # AI建议对应的方块索引（防止重复计算）
        self.auto_game_timer = None  # AI自动游戏定时器
        self.show_human_drop = True  # 是否显示人类决策落点（黄色框）

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

        # AI控制
        info_layout.addSpacing(20)
        info_layout.addWidget(QLabel('AI模式:'))

        self.ai_mode_combo = QComboBox()
        self.ai_mode_combo.addItems(['关闭', '游戏辅助', '辅助学习', 'AI自动游戏'])
        self.ai_mode_combo.currentIndexChanged.connect(self.change_ai_mode)
        info_layout.addWidget(self.ai_mode_combo)

        # 显示人类落点选项
        self.show_human_drop_checkbox = QCheckBox('显示人类决策落点')
        self.show_human_drop_checkbox.setChecked(True)
        self.show_human_drop_checkbox.toggled.connect(self.toggle_human_drop_display)
        info_layout.addWidget(self.show_human_drop_checkbox)

        self.ai_stats_label = QLabel('AI统计: 暂无数据')
        self.ai_stats_label.setWordWrap(True)
        self.ai_stats_label.setStyleSheet('font-size: 10px;')
        info_layout.addWidget(self.ai_stats_label)

        # 训练按钮
        self.training_button = QPushButton('训练AI')
        self.training_button.clicked.connect(self.show_training_dialog)
        info_layout.addWidget(self.training_button)

        layout.addWidget(info_panel, 1)

        # 添加说明
        self.add_instructions()

    def toggle_human_drop_display(self, checked):
        """切换是否显示人类决策落点"""
        self.show_human_drop = checked
        if not checked:
            self.game_area.human_drop_info = None
        self.game_area.update()

    def add_instructions(self):
        """添加操作说明"""
        status_bar = self.statusBar()
        status_bar.showMessage('↑:旋转  ←:左移  →:右移  ↓:加速  空格:暂停  A:显示AI建议')

    def change_ai_mode(self, index):
        """切换AI模式"""
        modes = ['off', 'game_assist', 'learning_assist', 'auto']
        self.ai_mode = modes[index]
        self.ai_enabled = (self.ai_mode != 'off')

        # 停止自动游戏定时器
        if self.auto_game_timer:
            self.auto_game_timer.stop()
            self.auto_game_timer = None

        if self.ai_mode == 'game_assist':
            self.statusBar().showMessage('游戏辅助模式已启用 - 按A键查看AI建议')
            self.ai.disable_auto_game()
            # 设置只显示人类可到达的位置
            self.ai.set_reachable_only(True)
            # 重置游戏速度为正常
            self.timer.setInterval(1000 // self.level)
        elif self.ai_mode == 'learning_assist':
            self.statusBar().showMessage('辅助学习模式已启用 - 按A键查看AI建议（不加速，收集训练数据）')
            self.ai.disable_auto_game()
            # 显示所有位置（用于收集训练数据）
            self.ai.set_reachable_only(False)
            # 重置游戏速度为正常
            self.timer.setInterval(1000 // self.level)
        elif self.ai_mode == 'auto':
            self.statusBar().showMessage('AI自动游戏已启动 - AI将完全控制游戏')
            self.ai.enable_auto_game()
            # 启动自动游戏
            QTimer.singleShot(1000, self.auto_game_step)
        else:
            self.statusBar().showMessage('↑:旋转  ←:左移  →:右移  ↓:加速  空格:暂停  A:显示AI建议')
            self.ai.disable_auto_game()

    def get_ai_suggestion(self):
        """获取AI建议"""
        if not self.ai_enabled or self.game_over or self.paused:
            return

        # 记录上一次计算时的人类状态
        last_human_rotation = getattr(self, '_last_ai_human_rotation', None)
        last_human_position = getattr(self, '_last_ai_human_position', None)
        last_piece_index = getattr(self, '_last_ai_piece_index', None)

        # 检查是否需要重新计算：
        # 1. 从未计算过，或
        # 2. 新的方块出现了，或
        # 3. 人类调整了位置或旋转
        need_recalculate = (
            last_piece_index is None or
            last_piece_index != self.current_piece_index or
            last_human_rotation != self.current_rotation or
            last_human_position != self.current_x
        )

        if not need_recalculate:
            return  # 人类状态未改变，无需重新计算

        # 创建游戏状态
        game_state = GameState(
            self.board,
            self.current_piece_index,
            self.next_piece_index
        )

        # 获取AI最优解
        # 自动游戏模式：使用全面比较（random_order=True）
        # 辅助模式：基于人类状态的局部改进
        is_assist_mode = (self.ai_mode == 'game_assist' or self.ai_mode == 'learning_assist')
        best_solution = self.ai.get_best_solution(
            game_state,
            human_rotation=self.current_rotation if is_assist_mode else None,
            human_position=self.current_x if is_assist_mode else None,
            auto_play=(self.ai_mode == 'auto')
        )

        if best_solution:
            self.ai_suggestion = best_solution

            # 记录计算时的人类状态
            self._last_ai_piece_index = self.current_piece_index
            self._last_ai_human_rotation = self.current_rotation
            self._last_ai_human_position = self.current_x

            # 计算人类当前状态的评分（评估函数会自动计算落点Y）
            human_solution = Solution(self.current_rotation, self.current_x)
            human_score = self.ai.evaluator.evaluate(game_state, human_solution)
            # 获取人类实际落点的Y坐标
            human_drop_y = getattr(human_solution, '_drop_height', None)
            if human_drop_y is None:
                # 重新计算人类落点
                shapes = self.shapes[self.current_piece_index]
                human_shape = shapes[self.current_rotation]
                board_01 = [[1 if cell != 0 else 0 for cell in row] for row in self.board]
                human_drop_y = self.ai.evaluator._find_drop_y_with_board(
                    board_01, human_shape, self.current_x
                )

            # 判断是否是改进建议
            is_improvement = (best_solution.rotation != self.current_rotation or
                           best_solution.position != self.current_x)
            score_improvement = best_solution.score - human_score

            # 获取AI建议的落点Y
            ai_drop_y = getattr(best_solution, '_drop_height', 0)

            suggestion_text = (f'当前: 旋转{self.current_rotation}次, 位置{self.current_x}, 落点Y={human_drop_y}, 得分{human_score:.1f} | '
                          f'AI建议: 旋转{best_solution.rotation}次, 位置{best_solution.position}, 落点Y={ai_drop_y}, 得分{best_solution.score:.1f}')

            # 打印详细的特征得分分解（仅在辅助学习模式）
            if hasattr(best_solution, 'features') and self.ai_mode == 'learning_assist':
                print(f"\n=== AI建议特征分解 ===", flush=True)
                print(f"总分={best_solution.score:.1f}", flush=True)
                weights = self.ai.evaluator.weights
                for feature_name, feature_value in best_solution.features.items():
                    if feature_name in weights:
                        weight = weights[feature_name]
                        contribution = weight * feature_value
                        print(f"  {feature_name:20s}: {feature_value:6.1f} × {weight:7.1f} = {contribution:8.1f}", flush=True)

            if is_improvement:
                if score_improvement > 0:
                    suggestion_text += f' (提升{score_improvement:.1f})'
                else:
                    suggestion_text += ' (改进)'
            elif best_solution.score > 0:
                suggestion_text += ' (优)'
            elif best_solution.score < -100:
                suggestion_text += ' (差)'

            self.statusBar().showMessage(suggestion_text, 8000)
            self.game_area.set_ai_suggestion(best_solution)
            # 设置人类决策落点信息（用于显示黄色提示框）- 仅在启用时设置
            if self.show_human_drop:
                self.game_area.set_human_drop_info(human_drop_y, human_score)
            else:
                self.game_area.human_drop_info = None

    def show_training_dialog(self):
        """显示训练对话框"""
        dialog = TrainingDialog(self)
        dialog.set_ai(self.ai)
        dialog.exec_()

    def update_ai_stats(self):
        """更新AI统计信息"""
        stats = self.ai.get_training_statistics()

        # 超人类统计
        total = self.ai.solutions_found
        better = self.ai.better_than_human
        rate = better / max(total, 1) * 100

        # 训练统计
        rejection_rate = stats['human_rejected_ai'] / max(stats['total_human_decisions'], 1) * 100

        stats_text = (
            f"AI超人类: {better}/{total} ({rate:.1f}%)\n"
            f"学习人类决策: {stats['human_rejected_ai']}/{stats['total_human_decisions']} ({rejection_rate:.1f}%)\n"
            f"训练阶段: {stats['stage']}\n"
            f"训练进度: {stats['progress_ratio']:.1%}"
        )
        self.ai_stats_label.setText(stats_text)

    def auto_game_step(self):
        """AI自动游戏的一步 - 直接基于规则搜索最佳决策并移动"""
        if self.ai_mode != 'auto' or self.game_over or self.paused:
            return

        # 获取自动游戏代理
        agent = self.ai.get_auto_agent()
        if not agent:
            return

        # 获取当前游戏状态
        game_state = GameState(
            self.board,
            self.current_piece_index,
            self.next_piece_index
        )

        # 获取最优决策（直接使用auto_play=True获取全局最优解）
        rotation, position = agent.make_decision(game_state)

        # 直接设置方块到目标位置（基于规则搜索的最优解）
        self.current_rotation = rotation
        self.current_x = position

        # 计算落点位置
        shape = self.shapes[self.current_piece_index][self.current_rotation]
        board_01 = [[1 if cell != 0 else 0 for cell in row] for row in self.board]

        # 找到该形状在该位置的落点Y
        drop_y = self.ai.evaluator._find_drop_y_with_board(board_01, shape, self.current_x)
        if drop_y is not None:
            # drop_y是方块底部的y坐标，需要转换为顶部坐标
            # 例如：方块高度4，底部在y=19，则顶部应该在y=16
            self.current_y = drop_y - len(shape) + 1

        self.game_area.update()
        # 直接锁定方块
        self.lock_piece()
        # 继续下一个方块
        QTimer.singleShot(100, self.auto_game_step)

    def _natural_drop_step(self):
        """自然下落一步"""
        if self.ai_mode != 'auto' or self.game_over or self.paused:
            return

        old_y = self.current_y
        self.current_y += 1

        if self.check_collision(self.current_x, self.current_y, self.current_rotation):
            self.current_y = old_y
            self.lock_piece()
            # 固定后清理目标，准备下一个方块
            if hasattr(self, '_auto_target'):
                del self._auto_target
            # 继续下一个方块
            QTimer.singleShot(100, self.auto_game_step)
        else:
            self.game_area.update()
            # 继续下落
            QTimer.singleShot(100, self.auto_game_step)

    def show_ai_training_dialog(self):
        """显示AI训练对话框"""
        stats = self.ai.get_statistics()
        msg = f"AI训练统计:\n\n"
        msg += f"已收集游戏数据: {stats['total_comparisons']} 局\n"
        msg += f"AI超人类次数: {stats['better_than_human_count']}\n"
        msg += f"超人类比例: {stats['better_than_human_rate']:.1f}%\n\n"

        msg += "深度强化学习状态:\n"
        msg += "- 当前使用启发式评估\n"
        msg += "- 收集足够数据后可训练神经网络\n"
        msg += "- 目标：AI完全自动游戏\n\n"

        msg += "建议：\n"
        msg += "1. 在AI辅助模式下玩游戏\n"
        msg += "2. 按A键查看AI建议并学习\n"
        msg += "3. 收集更多数据后切换到AI自动游戏"

        QMessageBox.information(self, 'AI训练状态', msg)

    def update_ai_stats_display(self):
        """更新AI统计显示"""
        stats = self.ai.get_statistics()
        if stats['total_comparisons'] > 0:
            self.ai_stats_label.setText(
                f'AI统计:\n收集数据: {stats["total_comparisons"]}\n'
                f'超人类: {stats["better_than_human_count"]}/{stats["total_comparisons"]}\n'
                f'超人类率: {stats["better_than_human_rate"]:.1f}%'
            )

    def new_piece(self):
        """生成新方块"""
        self.current_piece_index = self.next_piece_index
        self.current_rotation = 0  # 新方块总是从初始旋转状态开始
        self.piece_count += 1  # 增加方块计数

        shape = self.shapes[self.current_piece_index][self.current_rotation]
        self.current_x = (self.board_width - len(shape[0])) // 2
        self.current_y = 0

        # 生成下一个方块
        self.next_piece_index = random.randint(0, len(self.shapes) - 1)
        self.next_rotation = 0

        # 新方块出现：重置AI建议状态，允许下次按下A键时重新计算
        self.ai_suggestion = None
        self.ai_suggestion_piece_index = -1
        self._last_ai_piece_index = None
        self._last_ai_human_rotation = None
        self._last_ai_human_position = None

        # 检查游戏结束
        if self.check_collision(self.current_x, self.current_y, self.current_rotation):
            self.game_over = True
            self.timer.stop()

            # 自动保存训练数据（仅在辅助学习模式下）
            if self.ai_mode == 'learning_assist':
                import os
                data_dir = "training_data"
                if not os.path.exists(data_dir):
                    os.makedirs(data_dir)
                data_path = f"{data_dir}/tetris_training_data.json"
                self.ai.save_training_data(data_path)
                print(f"训练数据已自动保存到: {data_path}")

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

    def hard_drop(self):
        """直接掉落到最底部"""
        while not self.check_collision(self.current_x, self.current_y + 1, self.current_rotation):
            self.current_y += 1
        self.lock_piece()

    def lock_piece(self):
        """固定方块到游戏板"""
        # 保存AI训练所需的信息
        ai_training_data = None
        is_assist_mode = (self.ai_mode == 'game_assist' or self.ai_mode == 'learning_assist')
        if is_assist_mode and hasattr(self, '_last_ai_human_rotation'):
            ai_solution = getattr(self, 'ai_suggestion', None)
            if ai_solution:
                # 保存消除前的行数
                lines_before = self.lines_cleared
                # 创建游戏状态（在放置前）
                game_state = GameState(
                    self.board,
                    self.current_piece_index,
                    self.next_piece_index
                )
                # 计算人类实际落点（方块底部y坐标）
                human_shape = self.shapes[self.current_piece_index][self.current_rotation]
                # 方块占据的行是[current_y, current_y + len(shape) - 1]
                # 底部坐标是current_y + len(shape) - 1
                human_actual_drop_y = self.current_y + len(human_shape) - 1
                # 评估人类决策（传递实际落点）
                human_solution = Solution(self.current_rotation, self.current_x, actual_drop_y=human_actual_drop_y)
                human_score = self.ai.evaluator.evaluate(game_state, human_solution)
                # 判断人类决策是否值得学习
                # 当人类选择的位置与AI建议不同，且人类得分 >= AI得分时记录学习样本：
                # 1. 人类得分 > AI得分：人类学到了更优决策
                # 2. 人类得分 == AI得分：人类决策同样有效，可能具有AI当前权重未体现的优势（如更利于后续块、更美观等）
                # 人类决策总是被认为更优，让AI学习人类的选择
                position_differs = (
                    self.current_rotation != ai_solution.rotation or
                    self.current_x != ai_solution.position
                )
                human_decision_worth_learning = position_differs and (human_score >= ai_solution.score)
                # 保存训练数据
                ai_training_data = {
                    'game_state': game_state,
                    'human_solution': human_solution,
                    'ai_solution': ai_solution,
                    'human_decision_worth_learning': human_decision_worth_learning,
                    'lines_before': lines_before,
                    'human_score': human_score
                }

        shape = self.shapes[self.current_piece_index][self.current_rotation]
        color = self.colors[self.current_piece_index]

        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j]:
                    board_y = self.current_y + i
                    board_x = self.current_x + j
                    if board_y >= 0:
                        self.board[board_y][board_x] = color

        # 清除AI建议（新方块出现后允许重新计算）
        self.game_area.clear_ai_suggestion()
        self.ai_suggestion = None
        self.ai_suggestion_piece_index = -1
        self._last_ai_piece_index = None
        self._last_ai_human_rotation = None
        self._last_ai_human_position = None

        # 消除行并记录消除的行数
        lines_before_clear = self.lines_cleared
        self.clear_lines()
        lines_cleared_now = self.lines_cleared - lines_before_clear

        # 处理AI训练数据（仅在辅助学习模式下记录）
        if ai_training_data:
            # 只在辅助学习模式下记录决策
            if self.ai_mode == 'learning_assist':
                # 计算奖励
                final_reward = lines_cleared_now * 300  # 每行300分

                # 计算最高点
                highest_point = self._get_highest_point()

                # 更新AI的游戏上下文
                self.ai.update_game_context(
                    lines_cleared=self.lines_cleared,
                    highest_point=highest_point,
                    game_round=self.piece_count
                )

                # 记录人类决策（仅在辅助学习模式下）
                self.ai.record_human_decision(
                    game_state=ai_training_data['game_state'],
                    human_solution=ai_training_data['human_solution'],
                    ai_solution=ai_training_data['ai_solution'],
                    human_decision_worth_learning=ai_training_data['human_decision_worth_learning'],
                    lines_cleared=self.lines_cleared,
                    highest_point=highest_point,
                    game_round=self.piece_count,
                    final_reward=final_reward,
                    learning_assist_mode=True
                )

                # 打印人类初始决策特征分解（省略"落点Y="那行，保留"总分="和drop_height特征）
                if hasattr(ai_training_data['human_solution'], 'features'):
                    print(f"\n=== 人类决策特征分解 ===", flush=True)
                    print(f"总分={ai_training_data['human_score']:.1f}", flush=True)
                    weights = self.ai.evaluator.weights
                    for feature_name, feature_value in ai_training_data['human_solution'].features.items():
                        if feature_name in weights:
                            weight = weights[feature_name]
                            contribution = weight * feature_value
                            print(f"  {feature_name:20s}: {feature_value:6.1f} × {weight:7.1f} = {contribution:8.1f}", flush=True)

            # 更新AI统计显示（所有辅助模式都更新）
            self.update_ai_stats()

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

            # 辅助学习模式下不加速，保持正常速度
            if self.ai_mode == 'learning_assist':
                self.timer.setInterval(1000)  # 固定为1秒
            else:
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
        # 停止自动游戏定时器
        if self.auto_game_timer:
            self.auto_game_timer.stop()
            self.auto_game_timer = None

        # 重置游戏状态
        self.board = [[0] * self.board_width for _ in range(self.board_height)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False

        # 如果是AI自动游戏模式，切换到关闭模式
        if self.ai_mode == 'auto':
            self.ai_mode_combo.setCurrentIndex(0)  # 切换到"关闭"

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

        key_handled = False

        if event.key() == Qt.Key_Left:
            if not self.check_collision(self.current_x - 1, self.current_y, self.current_rotation):
                self.current_x -= 1
                self.game_area.update()
                key_handled = True

        elif event.key() == Qt.Key_Right:
            if not self.check_collision(self.current_x + 1, self.current_y, self.current_rotation):
                self.current_x += 1
                self.game_area.update()
                key_handled = True

        elif event.key() == Qt.Key_Down:
            if not self.check_collision(self.current_x, self.current_y + 1, self.current_rotation):
                self.current_y += 1
                self.game_area.update()
                key_handled = True

        elif event.key() == Qt.Key_Up:
            old_rotation = self.current_rotation
            self.rotate_piece()
            if self.current_rotation != old_rotation:
                key_handled = True

        elif event.key() == Qt.Key_Space:
            self.toggle_pause()

        elif event.key() == Qt.Key_A or event.key() == ord('a'):
            self.get_ai_suggestion()

        elif event.key() == Qt.Key_S or event.key() == ord('s'):
            self.toggle_pause()

        # 记录人类移动（辅助模式）
        if (self.ai_mode == 'game_assist' or self.ai_mode == 'learning_assist') and key_handled:
            self.last_human_move = {
                'rotation': self.current_rotation,
                'position': self.current_x
            }

        # 传递事件到父类，确保焦点处理
        super().keyPressEvent(event)

    def _count_lines(self):
        """计算当前满行数"""
        lines = 0
        for y in range(self.board_height):
            full = True
            for x in range(self.board_width):
                if not self.board[y][x]:
                    full = False
                    break
            if full:
                lines += 1
        return lines

    def _get_highest_point(self):
        """获取棋盘最高点"""
        for y in range(self.board_height):
            for x in range(self.board_width):
                if self.board[y][x]:
                    return self.board_height - y
        return 0

    def move_piece(self, dx: int):
        """移动方块

        Args:
            dx: 移动方向（-1左移，+1右移）
        """
        new_x = self.current_x + dx
        if not self.check_collision(new_x, self.current_y, self.current_rotation):
            self.current_x = new_x
            self.game_area.update()


class GameArea(QWidget):
    def __init__(self, game_window):
        super().__init__()
        self.game_window = game_window
        self.ai_suggestion = None
        self.human_drop_info = None  # 人类决策的落点信息
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFixedSize(
            game_window.board_width * game_window.block_size,
            game_window.board_height * game_window.block_size
        )

    def set_ai_suggestion(self, suggestion):
        """设置AI建议"""
        self.ai_suggestion = suggestion
        self.update()

    def set_human_drop_info(self, drop_y, score):
        """设置人类决策的落点信息"""
        self.human_drop_info = {'drop_y': drop_y, 'score': score}
        self.update()

    def clear_ai_suggestion(self):
        """清除AI建议和人类落点信息"""
        self.ai_suggestion = None
        self.human_drop_info = None
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.black)

        game = self.game_window

        # 绘制人类决策的落点（黄色虚线框）- 仅在启用时显示
        if self.human_drop_info and not game.game_over and not game.paused and game.show_human_drop:
            self._draw_human_drop(painter, game)

        # 绘制AI建议（绿色虚线框）
        if self.ai_suggestion and not game.game_over and not game.paused:
            self._draw_ai_suggestion(painter, game)

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

    def _draw_human_drop(self, painter, game):
        """绘制人类当前决策的落点（黄色虚线框）"""
        if not self.human_drop_info:
            return

        shape = game.shapes[game.current_piece_index][game.current_rotation]
        drop_y = self.human_drop_info['drop_y']

        # 绘制黄色虚线框
        pen = QPen(QColor(255, 255, 0), 2)  # 黄色
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j]:
                    block_x = game.current_x + j
                    # drop_y是方块底部坐标，顶部坐标是drop_y - len(shape) + 1
                    block_y = drop_y - len(shape) + 1 + i
                    size = game.block_size
                    painter.drawRect(block_x * size, block_y * size, size, size)

    def _draw_ai_suggestion(self, painter, game):
        """绘制AI建议的位置（虚线框）- 使用与AI engine完全一致的落点计算"""
        if not self.ai_suggestion:
            return

        # 计算建议的落点
        shapes = game.shapes[game.current_piece_index]
        shape = shapes[self.ai_suggestion.rotation]
        shape_height = len(shape)

        # 转换 board 为 0/1 值（与 GameState 一致）
        board_01 = [[1 if cell != 0 else 0 for cell in row] for row in game.board]

        # 找到建议位置的落点Y（与 AI engine 的 _find_drop_y_with_board 逻辑完全一致）
        drop_y = 0

        # 检查初始位置是否合法
        collision = False
        for i in range(shape_height):
            for j in range(len(shape[0])):
                if shape[i][j]:
                    new_x = self.ai_suggestion.position + j
                    new_y = i
                    if new_x < 0 or new_x >= 10 or new_y >= 20:
                        collision = True
                        break
                    if new_y >= 0 and board_01[new_y][new_x] == 1:
                        collision = True
                        break
            if collision:
                break

        if not collision:
            # 从底部向上找落点（与 _find_drop_y 完全一致）
            for y in range(20 - shape_height, -1, -1):
                collision = False
                for i in range(shape_height):
                    for j in range(len(shape[0])):
                        if shape[i][j]:
                            new_x = self.ai_suggestion.position + j
                            new_y = y + i
                            if new_x < 0 or new_x >= 10 or new_y >= 20:
                                collision = True
                                break
                            if new_y >= 0 and board_01[new_y][new_x] == 1:
                                collision = True
                                break
                    if collision:
                        break

                if not collision:
                    if y + shape_height >= 20:
                        drop_y = y
                        break
                    # 检查向下移动一格是否会碰撞
                    next_collision = False
                    for i in range(shape_height):
                        for j in range(len(shape[0])):
                            if shape[i][j]:
                                new_x = self.ai_suggestion.position + j
                                new_y = (y + 1) + i
                                if new_x < 0 or new_x >= 10 or new_y >= 20:
                                    next_collision = True
                                    break
                                if new_y >= 0 and board_01[new_y][new_x] == 1:
                                    next_collision = True
                                    break
                        if next_collision:
                            break
                    if next_collision:
                        drop_y = y
                        break

        # 绘制虚线框
        pen = QPen(QColor(0, 255, 0), 2)
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j]:
                    block_x = self.ai_suggestion.position + j
                    # drop_y是方块底部坐标，顶部坐标是drop_y - len(shape) + 1
                    block_y = drop_y - len(shape) + 1 + i
                    size = game.block_size
                    painter.drawRect(block_x * size, block_y * size, size, size)

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
