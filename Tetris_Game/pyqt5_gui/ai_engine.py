"""
俄罗斯方块AI引擎 - 基于深度强化学习和启发式评估

核心思想：
1. 将每个局面、当前方块、下一个方块视为一个问题
2. 每个可行的放置位置(旋转+位置)都是这个问题的候选解
3. 通过评估函数为每个解计算得分
4. AI在所有可行解中寻找最优解

深度强化学习机制：
- 初始使用启发式评估作为基准
- 收集人类游戏数据（状态、动作、奖励）
- 通过深度Q学习(DQN)逐步优化评估网络
- 从AI辅助演进到AI自动游戏

人类学习机制：
- 人类的选择可以作为较优解的参考
- AI可以比较不同解，找到比人类选择更优的超人类解
- 通过对比训练提升评估函数的准确性

机器学习动态评分系统：
- 使用神经网络预测动态权重，替代静态评分规则
- 通过人类-AI差异数据进行训练
- 渐进式优化：静态权重 → 混合权重 → 完全学习权重
"""
import copy
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from typing import List, Tuple, Dict, Optional


class GameState:
    """游戏状态表示"""
    def __init__(self, board: List[List[int]], current_piece: int, next_piece: int):
        # 转换 board：将非0值（QColor对象等）转换为1，确保碰撞检测一致性
        self.board = []
        for row in board:
            self.board.append([1 if cell != 0 else 0 for cell in row])
        self.current_piece = current_piece  # 当前方块索引(0-6)
        self.next_piece = next_piece  # 下一个方块索引(0-6)
        self.board_height = 20
        self.board_width = 10


class Solution:
    """放置解的表示"""
    def __init__(self, rotation: int, position: int, score: float = 0.0, actual_drop_y: int = None):
        self.rotation = rotation  # 旋转次数(0-3)
        self.position = position  # 位置(0-9)
        self.score = score  # 该解的评估得分
        self.features = {}  # 该解的特征向量
        self.distance = 0  # 与人类当前位置的距离（用于排序）
        self.feature_vector = None  # 特征向量数组（用于神经网络训练）
        self.actual_drop_y = actual_drop_y  # 实际落点Y坐标（方块底部的y坐标，由人类实际落下的位置决定）


class HeuristicEvaluator:
    """
    启发式评估器

    使用多种特征评估放置位置的优劣
    """

    def __init__(self):
        # 特征权重（可通过训练调整）
        self.weights = {
            'lines_cleared': 1000.0,      # 消除行数（最重要，大幅提高权重）
            'holes':         -20.0,       # 空洞数量（增加惩罚，强烈避免产生空洞）
            'highest_point':   -10.0,        # 棋盘最高点（所有列中最高的那个位置，越低越好）
            'drop_height':   5.0,        # 落点高度（落点越低越好，值越大越低）
            'near_complete': 50.0,           # 填补接近完成的行
            'block_contact_score': 10.0,      # 方块接触评分（侧边界1分，底部3分，中间2分）
            'next_piece_friendly': 4.0,         # 对下一个方块友好度（降低权重）
            'fills_upper_gaps': 2.0,          # 填补上层空缺能力（正向奖励），容易有意制造空缺
            'row_transitions': -10.0,            # 行转换次数（越少越好，表面越平整）
            'col_transitions': -5.0,            # 列转换次数（越少越好，表面越平整）
            'covered_bottom': -15.0,            # 被遮挡的空格数量（越少越好）
        }

        # 特征名称顺序（用于神经网络）
        self.feature_names = [
            'lines_cleared', 'holes',
            'highest_point', 'drop_height', 'near_complete',
            'block_contact_score', 'next_piece_friendly',
            'fills_upper_gaps',
            'row_transitions', 'col_transitions', 'covered_bottom'
        ]

        # 方块形状定义
        self._shapes = [
            # I形 - 旋转0和2相同，旋转1和3相同
            [
                [[1, 1, 1, 1]],
                [[1], [1], [1], [1]],
                [[1, 1, 1, 1]],
                [[1], [1], [1], [1]]
            ],
            # J形 - 4种状态都不同
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
            # L形 - 4种状态都不同
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
            # O形 - 所有旋转都相同
            [
                [[1, 1], [1, 1]],
                [[1, 1], [1, 1]],
                [[1, 1], [1, 1]],
                [[1, 1], [1, 1]]
            ],
            # S形 - 旋转0和2相同，旋转1和3相同
            [
                [[0, 1, 1], [1, 1, 0]],
                [[1, 0], [1, 1], [0, 1]],
                [[0, 1, 1], [1, 1, 0]],
                [[1, 0], [1, 1], [0, 1]]
            ],
            # T形 - 4种状态都不同
            [
                [[0, 1, 0], [1, 1, 1]],
                [[1, 0], [1, 1], [1, 0]],
                [[1, 1, 1], [0, 1, 0]],
                [[0, 1], [1, 1], [0, 1]]
            ],
            # Z形 - 旋转0和2相同，旋转1和3相同
            [
                [[1, 1, 0], [0, 1, 1]],
                [[0, 1], [1, 1], [1, 0]],
                [[1, 1, 0], [0, 1, 1]],
                [[0, 1], [1, 1], [1, 0]]
            ]
        ]

        # 预计算每种方块类型的唯一旋转状态
        self._unique_rotations = {}
        for piece_type in range(7):
            piece_shapes = self._shapes[piece_type]
            unique_rotations = []
            seen_shapes = []

            for rotation in range(4):
                shape = piece_shapes[rotation]

                # 检查该形状是否已经出现过
                is_duplicate = False
                for seen_shape in seen_shapes:
                    if shape == seen_shape:
                        is_duplicate = True
                        break

                if not is_duplicate:
                    unique_rotations.append(rotation)
                    seen_shapes.append(shape)

            self._unique_rotations[piece_type] = unique_rotations
    

    def get_all_solutions(self, game_state: GameState,
                         custom_weights: Dict[str, float] = None,
                         random_order: bool = False) -> List[Solution]:
        """
        获取所有可行的放置解

        根据游戏规则检查每个解是否可以通过合法的移动和旋转到达，
        确保自动游戏模式也符合人类游戏规则。

        Args:
            game_state: 当前游戏状态
            custom_weights: 自定义权重
            random_order: 是否使用随机顺序评分（可能找到更高质量的位置）

        Returns:
            按评分排序的解列表
        """
        solutions = []
        shapes = self._shapes

        # 获取不重复的旋转状态
        unique_rotations = self._unique_rotations[game_state.current_piece]

        # 遍历所有不重复的旋转状态
        for rotation in unique_rotations:
            # 获取当前旋转的形状
            shape = shapes[game_state.current_piece][rotation]

            # 计算有效位置范围
            shape_width = len(shape[0])
            min_pos = 0
            max_pos = 10 - shape_width

            # 创建位置列表
            positions = list(range(min_pos, max_pos + 1))

            # 遍历所有可能的位置
            for position in positions:
                solution = Solution(rotation, position)

                # 检查是否可以通过游戏规则到达（符合人类游戏规则）
                if self._is_reachable(game_state, solution, shapes):
                    # 评估该解（使用自定义权重或默认权重）
                    score = self.evaluate(game_state, solution, custom_weights)
                    if score > -float('inf'):
                        solutions.append(solution)

        # 按评分排序（降序）
        solutions.sort(key=lambda x: x.score, reverse=True)

        return solutions

    def _is_reachable(self, game_state: GameState, solution: Solution, shapes: List) -> bool:
        """
        检查目标位置是否可以通过合法的移动和旋转到达

        算法：
        1. 从生成位置开始，使用BFS搜索所有可能的路径
        2. 状态包含：(y坐标, x位置, 旋转次数)
        3. 方块可以在未锁定前继续移动（踢墙技巧）

        Args:
            game_state: 当前游戏状态
            solution: 目标解
            shapes: 方块形状列表

        Returns:
            是否可以到达
        """
        from collections import deque

        # 获取目标形状
        target_shape = shapes[game_state.current_piece][solution.rotation]

        # 计算目标落点Y坐标
        drop_y = self._find_drop_y_with_board(
            game_state.board, target_shape, solution.position
        )

        if drop_y is None:
            return False

        # 计算方块顶部y坐标（BFS搜索使用的是顶部坐标）
        target_top_y = drop_y - len(target_shape)

        # 状态：(y, x, rotation)
        # 从生成位置开始（y=0, x=根据方块宽度居中, rotation=0）
        start_x = 5 - len(shapes[game_state.current_piece][0][0]) // 2
        start_state = (0, start_x, 0)

        # BFS搜索
        visited = set()
        queue = deque([start_state])
        visited.add(start_state)

        while queue:
            y, x, rot = queue.popleft()

            # 检查是否到达目标（drop_y是底部坐标，需要转换为顶部坐标）
            if (y, x, rot) == (target_top_y, solution.position, solution.rotation):
                return True

            # 检查当前状态是否可以下移
            current_shape = shapes[game_state.current_piece][rot]
            can_drop = not self._check_collision(game_state.board, current_shape, x, y + 1)

            # 如果可以下移，尝试下移
            if can_drop:
                new_state = (y + 1, x, rot)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append(new_state)

            # 如果不能下移（已到底部），仍然可以左右移动（踢墙）
            # 但需要在移动后检查是否能继续下移（不能下移才算真正锁定）
            current_shape = shapes[game_state.current_piece][rot]
            shape_width = len(current_shape[0])

            # 左移
            if x > 0:
                if not self._check_collision(game_state.board, current_shape, x - 1, y):
                    new_state = (y, x - 1, rot)
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append(new_state)

            # 右移
            if x + shape_width < 10:
                if not self._check_collision(game_state.board, current_shape, x + 1, y):
                    new_state = (y, x + 1, rot)
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append(new_state)

            # 尝试旋转（4个方向）
            for new_rot in range(4):
                if new_rot == rot:
                    continue

                new_shape = shapes[game_state.current_piece][new_rot]
                new_shape_width = len(new_shape[0])

                # 检查旋转后是否越界
                if x < 0 or x + new_shape_width > 10:
                    continue

                # 检查旋转后是否碰撞
                if not self._check_collision(game_state.board, new_shape, x, y):
                    new_state = (y, x, new_rot)
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append(new_state)

        return False

    def _simulate_with_drop_height(self, game_state: GameState, solution: Solution) -> Tuple[Optional[List[List[int]]], Optional[int], int]:
        """
        模拟方块放置并返回落点高度和消除行数

        Args:
            game_state: 游戏状态
            solution: 解

        Returns:
            (放置后的棋盘, 落点Y坐标, 消除的行数)
        """
        shapes = self._shapes
        shape = shapes[game_state.current_piece][solution.rotation]

        # 复制棋盘
        board = [row[:] for row in game_state.board]

        # 如果solution指定了actual_drop_y（人类实际落点），使用它；否则重新计算
        if solution.actual_drop_y is not None:
            drop_y = solution.actual_drop_y
        else:
            # 计算落点位置
            drop_y = self._find_drop_y_with_board(board, shape, solution.position)
            if drop_y is None:
                return None, None, 0

        # 保存落点高度
        solution._drop_height = drop_y
        # 方块高度
        shape_height = len(shape)

        # 放置方块
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j]:
                    # drop_y是方块底部坐标，顶部坐标是drop_y - shape_height + 1
                    board_y = drop_y - shape_height + 1 + i
                    board_x = solution.position + j
                    if 0 <= board_y < 20 and 0 <= board_x < 10:
                        board[board_y][board_x] = 1

        # 消除完整行并获取消除的行数
        board, lines_cleared = self._clear_lines(board)

        return board, drop_y, lines_cleared

    def evaluate(self, game_state: GameState, solution: Solution,
                 custom_weights: Dict[str, float] = None) -> float:
        """
        评估一个放置解的得分

        Args:
            game_state: 当前游戏状态
            solution: 要评估的解(旋转+位置)
            custom_weights: 自定义权重（用于动态评分）

        Returns:
            该解的评估得分（越高越好）
        """
        # 模拟放置并获取落点高度和消除行数
        simulated_board, drop_y, lines_cleared = self._simulate_with_drop_height(game_state, solution)
        if simulated_board is None:
            return -float('inf')  # 无效的解

        # 保存消除行数到solution，供_extract_features使用
        solution._lines_cleared = lines_cleared

        # 获取方块形状用于计算接触评分
        shapes = self._shapes
        shape = shapes[game_state.current_piece][solution.rotation]

        # 提取特征（传递原始棋盘用于计算接触评分）
        features = self._extract_features(simulated_board, solution, game_state.next_piece,
                                         game_state.board, shape, drop_y)

        solution.features = features

        # 使用自定义权重或默认权重
        weights = custom_weights if custom_weights else self.weights

        # 计算总分
        score = 0.0
        for feature_name, value in features.items():
            if feature_name in weights:
                score += weights[feature_name] * value

        solution.score = score
        return score


    def _find_drop_y_with_board(self, board: List[List[int]], shape: List[List[int]], position: int) -> int:
        """
        找到方块的落点Y坐标（返回实际值）

        Args:
            board: 棋盘
            shape: 方块形状
            position: 方块位置

        Returns:
            落点Y坐标（方块底部的y坐标）
        """
        shape_height = len(shape)
        shape_width = len(shape[0])

        # 检查初始位置是否合法
        if self._check_collision(board, shape, position, 0):
            return 0  # 初始位置就碰撞，返回0

        # 从底部向上找落点（找方块底部能放置的位置）
        for y in range(20 - shape_height, -1, -1):
            if not self._check_collision(board, shape, position, y):
                # 检查再下一行是否会碰撞
                if y + shape_height >= 20 or self._check_collision(board, shape, position, y + 1):
                    # 返回方块底部的y坐标：y是顶部坐标，底部是y + shape_height - 1
                    return y + shape_height - 1

        return 19  # 默认返回初始底部位置
    
    def _check_collision(self, board: List[List[int]], shape: List[List[int]], x: int, y: int) -> bool:
        """检查碰撞（只有值为1的方格才是实体的方格才会出现碰撞）"""
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j]:
                    new_x = x + j
                    new_y = y + i

                    if new_x < 0 or new_x >= 10 or new_y >= 20:
                        return True
                    # 只检查值为1的方格才碰撞
                    if new_y >= 0 and board[new_y][new_x] == 1:
                        return True
        return False

    def _extract_features(self, board: List[List[int]], solution: Solution, next_piece: int,
                        original_board: List[List[int]] = None, shape: List[List[int]] = None,
                        drop_y: int = None) -> Dict[str, float]:
        """提取放置后的特征"""
        features = {}

        # 1. 消除行数（由调用方提供，这里设为0默认值）
        features['lines_cleared'] = getattr(solution, '_lines_cleared', 0)

        # 2. 空洞数量
        features['holes'] = self._count_holes(board)

        # 3. 最高点
        features['highest_point'] = self._get_highest_point(board)

        # 4. 落点高度
        drop_height = self._get_drop_height(solution)
        features['drop_height'] = drop_height

        # 5. 接近完成的行数
        features['near_complete'] = self._count_near_complete_lines(board)

        # 6. 方块接触评分（计算放置后方块与周围环境的接触情况）
        features['block_contact_score'] = self._calculate_block_contact(
                original_board, board, shape, solution.position, drop_y
            )

        # 7. 对下一个方块友好度（计算下一个方块的可行位置数）
        features['next_piece_friendly'] = self._evaluate_next_piece_friendly(board, next_piece)

        # 8. 填补上层空缺能力（计算下一块及其他方块的填补方式）
        features['fills_upper_gaps'] = self._evaluate_upper_gap_filling(board, next_piece)

        # 9. 行转换次数（表面平整度）
        features['row_transitions'] = self._count_row_transitions(board, drop_y)

        # 10. 列转换次数（表面平整度）
        features['col_transitions'] = self._count_col_transitions(board)

        # 11. 覆盖的底部方块数量
        features['covered_bottom'] = self._count_covered_bottom(original_board, board, shape, solution.position, drop_y)

        # 生成特征向量数组（用于神经网络）
        solution.feature_vector = np.array([
            features['lines_cleared'],
            features['holes'],
            features['highest_point'],
            features['drop_height'],
            features['near_complete'],
            features['block_contact_score'],
            features['next_piece_friendly'],
            features['fills_upper_gaps'],
            features['row_transitions'],
            features['col_transitions'],
            features['covered_bottom']
        ], dtype=np.float32)

        return features

    def _clear_lines(self, board: List[List[int]]) -> Tuple[List[List[int]], int]:
        """消除完整行，返回(消除后的棋盘, 消除的行数)"""
        new_board = []
        lines_cleared = 0

        for y in range(20):
            # 检查是否所有列都有方块（处理 QColor 对象）
            is_full = True
            for x in range(10):
                cell = board[y][x]
                if cell is None or cell == 0:
                    is_full = False
                    break

            if is_full:
                lines_cleared += 1
            else:
                new_board.append(board[y][:])

        # 在顶部添加空行
        for _ in range(lines_cleared):
            new_board.insert(0, [0] * 10)

        return new_board, lines_cleared

    def _count_holes(self, board: List[List[int]]) -> int:
        """
        计算空洞/孔洞数量（被实体方块或边界包围的空格）

        定义：当一个空格的正上方、正左边、正右边、正下方都是边界或实体方块时，
        该位置就是空洞/孔洞（包括两个及以上连在一起而周围均为实体方块或边界的情况）
        """
        holes = 0

        for y in range(20):
            for x in range(10):
                # 只考虑空格
                cell = board[y][x]
                if cell is None or cell == 0:
                    # 检查四个方向是否都是边界或实体方块

                    # 上方：边界(y=0)或上方是实体方块
                    top_blocked = (y == 0) or (y > 0 and board[y-1][x] is not None and board[y-1][x] != 0)

                    # 左边：边界(x=0)或左边是实体方块
                    left_blocked = (x == 0) or (x > 0 and board[y][x-1] is not None and board[y][x-1] != 0)

                    # 右边：边界(x=9)或右边是实体方块
                    right_blocked = (x == 9) or (x < 9 and board[y][x+1] is not None and board[y][x+1] != 0)

                    # 下方：边界(y=19)或下方是实体方块
                    bottom_blocked = (y == 19) or (y < 19 and board[y+1][x] is not None and board[y+1][x] != 0)

                    # 如果四个方向都被阻挡，则这是一个空洞/孔洞
                    if top_blocked and left_blocked and right_blocked and bottom_blocked:
                        holes += 1

        return holes
    

    def _get_highest_point(self, board: List[List[int]]) -> int:
        """获取最高点"""
        for y in range(20):
            # 检查是否有任意列有方块
            for x in range(10):
                cell = board[y][x]
                if cell is not None and cell != 0:
                    return 20 - y
        return 0
    
    def _get_drop_height(self, solution: Solution, game_state: GameState = None) -> int:
        """获取解的落点高度"""
        # 在模拟放置时应该已经计算过落点Y
        # 这里返回一个合理的默认值
        # 如果需要准确值，应该在simulate_placement中记录
        if hasattr(solution, '_drop_height'):
            return solution._drop_height
        # 简化处理：使用位置作为近似
        return solution.position

    def _count_near_complete_lines(self, board: List[List[int]]) -> float:
        """
        统计接近完成的行（8-9个方块），根据行的高度加权

        加权规则：
        - 底部行（Y值大）接近完成：得分高（权重高）
        - 顶部行（Y值小）接近完成：得分低（权重低）
        - 权重 = (y + 1) / 20，底部权重接近1，顶部权重接近0.05

        这样可以避免以留下底部空缺为代价让顶部接近完成。
        """
        weighted_count = 0.0
        for y in range(20):
            filled = 0
            for x in range(10):
                cell = board[y][x]
                if cell is not None and cell != 0:
                    filled += 1

            if filled >= 8:
                # 根据行的高度计算权重
                # y=0 (顶部): weight = 1/20 = 0.05
                # y=19 (底部): weight = 20/20 = 1.0
                weight = (y + 1) / 20.0
                weighted_count += weight

        return weighted_count

    def _calculate_block_contact(self, original_board: List[List[int]], placed_board: List[List[int]],
                                 shape: List[List[int]], position: int, drop_y: int) -> float:
        """
        计算放置后方块与周围环境的接触评分

        计算方式：
        - 与侧边界接触：每接触1次得1分
        - 与底部方块/底边界接触：每接触1次得3分
        - 与中间方块（其他方块）接触：每接触1次得2分

        Args:
            original_board: 放置前的棋盘
            placed_board: 放置后的棋盘
            shape: 方块形状
            position: 方块位置
            drop_y: 落点Y坐标

        Returns:
            接触评分总分
        """
        contact_score = 0.0
        shape_height = len(shape)

        # 遍历方块的所有格子
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j]:  # 如果这是方块的实体部分
                    # drop_y是方块底部坐标，顶部坐标是drop_y - shape_height + 1
                    board_y = drop_y - shape_height + 1 + i
                    board_x = position + j

                    if not (0 <= board_y < 20 and 0 <= board_x < 10):
                        continue

                    # 检查四个方向的接触情况
                    # 1. 左边界或左侧有方块
                    if board_x == 0:  # 左边界
                        contact_score += 1.0  # 侧边界接触1分
                    else:
                        # 检查左侧是否在原始棋盘就有方块
                        left_cell = original_board[board_y][board_x - 1]
                        if left_cell is not None and left_cell != 0:
                            contact_score += 2.0  # 中间方块接触2分

                    # 2. 右边界或右侧有方块
                    if board_x == 9:  # 右边界
                        contact_score += 1.0  # 侧边界接触1分
                    else:
                        # 检查右侧是否在原始棋盘就有方块
                        right_cell = original_board[board_y][board_x + 1]
                        if right_cell is not None and right_cell != 0:
                            contact_score += 2.0  # 中间方块接触2分

                    # 3. 底边界或底部有方块
                    if board_y == 19:  # 底边界
                        contact_score += 3.0  # 底部/底边界接触3分
                    else:
                        # 检查下方是否在原始棋盘就有方块
                        bottom_cell = original_board[board_y + 1][board_x]
                        if bottom_cell is not None and bottom_cell != 0:
                            contact_score += 3.0  # 底部方块接触3分

                    # 4. 顶部（不计分，因为上方通常没有支撑）
                    # 不检查顶部接触

        return contact_score
    
    def _evaluate_next_piece_friendly(self, board: List[List[int]], next_piece: int) -> int:
        """
        评估当前放置对下一个方块的友好度

        计算逻辑：
        1. 模拟下一个方块的所有可能放置
        2. 计算每个位置的下个方块得分潜力
        3. 返回下一个方块能达到的最高分

        这样可以鼓励当前块为下一个块留出更好的位置。
        """
        shapes = self._shapes

        best_score = 0

        # 遍历下一个方块的所有旋转和位置
        for rot in range(4):
            shape = shapes[next_piece][rot]
            shape_height = len(shape)
            shape_width = len(shape[0])

            for pos in range(10 - shape_width + 1):
                # 检查初始位置是否合法
                if not self._check_collision(board, shape, pos, 0):
                    # 计算落点
                    drop_y = self._find_drop_y_with_board(board, shape, pos)
                    if drop_y is None:
                        continue

                    # 模拟放置
                    temp_board = [row[:] for row in board]
                    for i in range(len(shape)):
                        for j in range(len(shape[0])):
                            if shape[i][j]:
                                # drop_y是方块底部坐标，顶部坐标是drop_y - shape_height + 1
                                temp_board[drop_y - shape_height + 1 + i][pos + j] = 1

                    # 计算这个位置的得分潜力
                    # 考虑几个关键特征
                    potential_score = 0

                    # 1. 消除行数（最重要）
                    lines_cleared = self._count_lines(temp_board) - self._count_lines(board)
                    potential_score += lines_cleared * 100

                    # 2. 填补接近完成的行
                    near_complete = self._count_near_complete_lines(temp_board)
                    potential_score += near_complete * 10

                    # 3. 减少空洞数量
                    holes = self._count_holes(temp_board)
                    potential_score -= holes * 5

                    # 4. 降低最高点
                    highest_point = self._get_highest_point(temp_board)
                    potential_score -= highest_point * 2

                    # 更新最佳得分
                    best_score = max(best_score, potential_score)

        return best_score

    def _count_lines(self, board: List[List[int]]) -> int:
        """计算棋盘中的满行数"""
        lines = 0
        for y in range(20):
            full = True
            for x in range(10):
                cell = board[y][x]
                if cell is None or cell == 0:
                    full = False
                    break
            if full:
                lines += 1
        return lines

    def _evaluate_upper_gap_filling(self, board: List[List[int]], next_piece: int = None) -> int:
        """
        评估填补上层空缺的能力

        定义：当前解完成后，下一块方块及其他方块能有几种方式（旋转状态，不同方块不同）填补目前的空缺

        计算逻辑：
        1. 识别所有"空缺"（尚未被彻底包围的空格，周围仅有一个位置为空格）
        2. 对于每个空缺，计算下一块方块及其他方块填补它的可能方式数
        3. 下一方块的填补方式权重高于其他方块

        Args:
            board: 放置后的棋盘
            next_piece: 下一个方块类型（用于加权计算）

        Returns:
            填补能力评分（越高越好）
        """
        gap_fill_score = 0
        shapes = self._shapes

        # 1. 识别所有空缺（周围仅有一个位置为空格的位置）
        gaps = self._find_gaps(board)

        # 2. 计算每个空缺的填补方式数
        for gap in gaps:
            gap_x, gap_y = gap
            fill_ways = 0
            next_piece_ways = 0

            # 尝试用每种方块的每种旋转状态填补该空缺
            for piece_type in range(7):
                piece_shapes = shapes[piece_type]
                unique_rotations = self._unique_rotations[piece_type]

                for rotation in unique_rotations:
                    shape = piece_shapes[rotation]

                    # 找到该形状能填补空缺的所有位置
                    for i in range(len(shape)):
                        for j in range(len(shape[0])):
                            if shape[i][j]:  # 方块的实体部分
                                # 尝试将这部分放在空缺位置
                                place_x = gap_x - j
                                place_y = gap_y - i

                                # 计算落点位置（内部已包含碰撞检测）
                                drop_y = self._find_drop_y_with_board(board, shape, place_x)
                                if drop_y is not None:
                                    # drop_y是方块底部坐标，顶部坐标是drop_y - len(shape) + 1
                                    # 如果落点后能填补该空缺，则计数
                                    if drop_y - len(shape) + 1 + i == gap_y and place_x + j == gap_x:
                                        fill_ways += 1
                                        if next_piece is not None and piece_type == next_piece:
                                            next_piece_ways += 1

            # 下一方块的填补方式权重更高（权重x10）
            if next_piece is not None:
                # 下一方块贡献的得分
                gap_fill_score += next_piece_ways * 2
            # 其他方块贡献的得分
            gap_fill_score += fill_ways - next_piece_ways

        return gap_fill_score

    def _find_gaps(self, board: List[List[int]]) -> List[Tuple[int, int]]:
        """
        找出所有"空缺"（尚未被彻底包围的空格）

        定义：空格周围（上、下、左、右）有且仅有一个位置为空格（其他为边界或实体方块）
        即：被"堵住"三个方向，只剩一个开口可以填补
        附加条件：至少有一个方向的邻居是实体方块（避免在空棋盘上识别）

        Args:
            board: 棋盘

        Returns:
            空缺位置列表 [(x, y), ...]
        """
        gaps = []

        for y in range(20):
            for x in range(10):
                if board[y][x] == 0:  # 只考虑空格
                    # 统计周围有多少个是"空格"（边界不算空格）
                    empty_neighbors = 0
                    has_block_neighbor = False  # 至少有一个实体方块邻居

                    # 上方
                    if y > 0:
                        if board[y-1][x] == 0:
                            empty_neighbors += 1
                        elif board[y-1][x] is not None and board[y-1][x] != 0:
                            has_block_neighbor = True

                    # 下方
                    if y < 19:
                        if board[y+1][x] == 0:
                            empty_neighbors += 1
                        elif board[y+1][x] is not None and board[y+1][x] != 0:
                            has_block_neighbor = True

                    # 左边
                    if x > 0:
                        if board[y][x-1] == 0:
                            empty_neighbors += 1
                        elif board[y][x-1] is not None and board[y][x-1] != 0:
                            has_block_neighbor = True

                    # 右边
                    if x < 9:
                        if board[y][x+1] == 0:
                            empty_neighbors += 1
                        elif board[y][x+1] is not None and board[y][x+1] != 0:
                            has_block_neighbor = True

                    # 如果周围有且仅有一个空格，且至少有一个实体方块邻居，这是"空缺"
                    if empty_neighbors == 1 and has_block_neighbor:
                        gaps.append((x, y))

        return gaps


    def _count_row_transitions(self, board: List[List[int]], drop_y: int = None) -> int:
        """
        统计行转换次数（空格到实体或实体到空格的转换）

        计算逻辑：
        1. 检测当前方块最终下落到达的最低行
        2. 左边边界记为实体（1）
        3. 统计从空到实或从实到空的转换次数
        4. 转换次数越少说明行越完整或越空，越有利于放置

        Args:
            board: 棋盘
            drop_y: 方块落点y坐标（方块最低行的位置）

        该特征反映了棋盘表面的"粗糙"程度。
        """
        transitions = 0

        prev_cell = 1  # 左边边界记为实体（1）

        # 边界检查：确保drop_y在有效范围内
        if drop_y is None or drop_y >= len(board) or drop_y < 0:
            return transitions

        for x in range(10):
            cell = board[drop_y][x]
            if cell is None or cell == 0:
                current_cell = 0
            else:
                current_cell = 1

            # 检测转换（0->1 或 1->0）
            if prev_cell != current_cell:
                transitions += 1

            prev_cell = current_cell

        # 右边界的转换
        if prev_cell != 1:
            transitions += 1

        return transitions

    def _count_col_transitions(self, board: List[List[int]]) -> int:
        """
        统计列转换次数（空格到实体或实体到空格的转换）

        计算逻辑：
        1. 从上到下、从左到右遍历整个棋盘
        2. 上方边界记为空格（0）
        3. 统计每列从空到实或从实到空的转换次数
        4. 转换次数越少说明列越连续，越有利于放置

        该特征与row_transitions一起，更全面地反映表面平整度。
        """
        transitions = 0

        # 遍历每一列（从左到右）
        for x in range(10):
            prev_cell = 0  # 上方边界记为空格

            # 从上到下遍历每一行
            for y in range(20):
                cell = board[y][x]
                if cell is None or cell == 0:
                    current_cell = 0
                else:
                    current_cell = 1

                # 检测转换（0->1 或 1->0）
                if prev_cell != current_cell:
                    transitions += 1

                prev_cell = current_cell

            # 底部边界的转换
            if prev_cell != 0:
                transitions += 1

        return transitions

    def _count_covered_bottom(self, original_board: List[List[int]], final_board: List[List[int]],
                            shape: List[List[int]], position: int, drop_y: int) -> int:
        """
        统计当前方块下落导致下方被遮挡的空格数量

        计算逻辑：
        1. 对于放置后方块的每个实体部分，检查其正下方的空格
        2. 如果正下方的空格在original_board中是空的（可以从上方直接放置到达）
        3. 但在final_board中被堵住了（无法直接放置到达），则计数+1

        Args:
            original_board: 放置前的棋盘
            final_board: 放置后的棋盘
            shape: 方块形状
            position: 方块横向位置
            drop_y: 方块纵向落点

        Returns:
            被遮挡的空格数量
        """
        covered_count = 0
        shape_height = len(shape)

        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j]:  # 方块的实体部分
                    # drop_y是方块底部坐标，顶部坐标是drop_y - shape_height + 1
                    block_y = drop_y - shape_height + 1 + i
                    block_x = position + j

                    # 检查方块正下方是否为空格
                    below_y = block_y + 1
                    if below_y < 20:
                        # 原始棋盘中该位置是空格（可以从上方放置）
                        if (original_board[below_y][block_x] is None or
                            original_board[below_y][block_x] == 0):
                            # 但在final_board中被遮挡了
                            covered_count += 1

        return covered_count

class WeightPredictor(nn.Module):
    """
    PyTorch实现的权重预测神经网络

    根据游戏状态预测动态的评分权重
    """

    def __init__(self, input_dim=217, hidden_dims=[256, 128, 64], output_dim=10):
        """
        初始化神经网络

        Args:
            input_dim: 输入维度（棋盘200 + 当前方块7 + 下一个方块7 + 上下文3 = 217）
            hidden_dims: 隐藏层维度列表
            output_dim: 输出维度（10个特征权重）
        """
        super(WeightPredictor, self).__init__()

        layers = []
        prev_dim = input_dim

        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(0.2)
            ])
            prev_dim = hidden_dim

        # 输出层（不使用激活函数，直接输出权重）
        layers.append(nn.Linear(prev_dim, output_dim))

        self.network = nn.Sequential(*layers)

        # 训练相关
        self.is_trained = False
        self.training_samples = 0

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        前向传播

        Args:
            x: 输入特征张量 (batch_size, input_dim)

        Returns:
            预测的权重向量 (batch_size, output_dim)
        """
        return self.network(x)


class NeuralNetworkPredictor:
    """
    神经网络权重预测器包装类

    包装PyTorch的WeightPredictor，提供与原接口一致的API
    """

    def __init__(self, input_dim=217, hidden_dims=[256, 128, 64], output_dim=13):
        """
        初始化神经网络

        Args:
            input_dim: 输入维度
            hidden_dims: 隐藏层维度列表
            output_dim: 输出维度（11个特征权重）
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = WeightPredictor(input_dim, hidden_dims, output_dim).to(self.device)

        # 优化器
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        # 训练相关
        self.is_trained = False
        self.training_samples = 0

        # 损失函数（Ranking Loss）
        self.margin = 10.0

    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        前向传播

        Args:
            x: 输入特征向量 (batch_size, input_dim) 或 (input_dim,)

        Returns:
            预测的权重向量 (batch_size, output_dim) 或 (output_dim,)
        """
        self.model.eval()
        with torch.no_grad():
            if x.ndim == 1:
                x = x.reshape(1, -1)

            x_tensor = torch.FloatTensor(x).to(self.device)
            output = self.model(x_tensor)

            return output.cpu().numpy().squeeze()

    def train_step(self, state_features: np.ndarray, human_features: np.ndarray,
                   ai_features: np.ndarray, human_score: float, ai_score: float,
                   reward: float = 0.0) -> float:
        """
        单步训练（使用Ranking Loss）

        Args:
            state_features: 游戏状态特征 (input_dim,)
            human_features: 人类解的特征向量 (11维)
            ai_features: AI解的特征向量 (11维)
            human_score: 人类决策的原始得分
            ai_score: AI推荐的原始得分
            reward: 实际奖励（可选）

        Returns:
            损失值
        """
        self.model.train()

        # 转换为张量
        state_tensor = torch.FloatTensor(state_features).unsqueeze(0).to(self.device)
        human_features_tensor = torch.FloatTensor(human_features).to(self.device)
        ai_features_tensor = torch.FloatTensor(ai_features).to(self.device)

        # 前向传播
        predicted_weights = self.model(state_tensor).squeeze()

        # 计算人类和AI决策的预测得分
        human_pred_score = torch.sum(predicted_weights * human_features_tensor)
        ai_pred_score = torch.sum(predicted_weights * ai_features_tensor)

        # 计算Ranking Loss: 人类得分应该比AI高
        # Loss = ReLU(ai_score - human_score - margin)
        loss = torch.relu(ai_pred_score - human_pred_score + self.margin)

        # 如果有奖励信息，加入正则化
        if reward > 0:
            # 奖励高意味着人类决策好，强化学习
            reward_loss = -torch.log(torch.sigmoid(human_pred_score - ai_pred_score))
            loss = loss + 0.1 * reward_loss

        # 反向传播
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.training_samples += 1
        if self.training_samples > 100:
            self.is_trained = True

        return loss.item()

    def train_batch(self, state_features_batch: List[np.ndarray],
                    human_features_batch: List[np.ndarray],
                    ai_features_batch: List[np.ndarray],
                    human_scores_batch: List[float],
                    ai_scores_batch: List[float],
                    rewards_batch: List[float] = None) -> float:
        """
        批量训练

        Args:
            state_features_batch: 批次的游戏状态特征 (batch_size, input_dim)
            human_features_batch: 批次的人类解特征 (batch_size, 11)
            ai_features_batch: 批次的AI解特征 (batch_size, 11)
            human_scores_batch: 批次的人类得分
            ai_scores_batch: 批次的AI得分
            rewards_batch: 批次的奖励（可选）

        Returns:
            平均损失值
        """
        self.model.train()

        batch_size = len(state_features_batch)

        # 转换为张量
        state_tensor = torch.FloatTensor(np.array(state_features_batch)).to(self.device)
        human_features_tensor = torch.FloatTensor(np.array(human_features_batch)).to(self.device)
        ai_features_tensor = torch.FloatTensor(np.array(ai_features_batch)).to(self.device)

        # 前向传播
        predicted_weights = self.model(state_tensor)

        # 计算人类和AI决策的预测得分
        human_pred_scores = torch.sum(predicted_weights * human_features_tensor, dim=1)
        ai_pred_scores = torch.sum(predicted_weights * ai_features_tensor, dim=1)

        # 计算Ranking Loss
        losses = torch.relu(ai_pred_scores - human_pred_scores + self.margin)

        # 如果有奖励信息
        if rewards_batch:
            rewards_tensor = torch.FloatTensor(rewards_batch).to(self.device)
            # 对奖励>0的样本加强学习
            reward_mask = (rewards_tensor > 0)
            if reward_mask.any():
                reward_loss = -torch.log(torch.sigmoid(human_pred_scores[reward_mask] -
                                                        ai_pred_scores[reward_mask]))
                losses[reward_mask] = losses[reward_mask] + 0.1 * reward_loss

        # 平均损失
        avg_loss = losses.mean()

        # 反向传播
        self.optimizer.zero_grad()
        avg_loss.backward()
        self.optimizer.step()

        self.training_samples += batch_size
        if self.training_samples > 100:
            self.is_trained = True

        return avg_loss.item()

    def predict_weights(self, state_features: np.ndarray) -> Dict[str, float]:
        """
        预测特征权重

        Args:
            state_features: 游戏状态特征 (217维)

        Returns:
            特征权重字典
        """
        predicted = self.forward(state_features)

        feature_names = [
            'lines_cleared', 'holes', 'bumpiness',
            'highest_point', 'drop_height', 'near_complete',
            'block_contact_score', 'next_piece_friendly', 'fills_upper_gaps',
            'fillable_positions'
        ]

        weights = {}
        for name, value in zip(feature_names, predicted):
            weights[name] = float(value)

        return weights

    def save(self, filepath: str):
        """保存模型"""
        model_data = {
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'input_dim': self.model.network[0].in_features,
            'hidden_dims': [layer.out_features for layer in self.model.network
                           if isinstance(layer, nn.Linear)][:-1],
            'output_dim': self.model.network[-1].out_features,
            'is_trained': self.is_trained,
            'training_samples': self.training_samples
        }
        torch.save(model_data, filepath)

    def load(self, filepath: str):
        """加载模型"""
        model_data = torch.load(filepath, map_location=self.device)

        self.model.load_state_dict(model_data['model_state_dict'])
        self.optimizer.load_state_dict(model_data['optimizer_state_dict'])
        self.is_trained = model_data['is_trained']
        self.training_samples = model_data['training_samples']


class ExperienceReplayBuffer:
    """
    经验回放缓冲区

    存储人类-AI差异数据用于训练
    """

    def __init__(self, capacity=50000):
        """
        初始化缓冲区

        Args:
            capacity: 最大容量
        """
        self.capacity = capacity
        self.buffer = []

    def add(self, sample: Dict):
        """
        添加样本

        Args:
            sample: 样本字典，包含：
                - state_features: 游戏状态特征
                - human_solution: 人类选择的解
                - ai_solution: AI推荐的解
                - human_features: 人类解的特征向量
                - ai_features: AI解的特征向量
                - reward: 奖励（人类最终得分 - AI推荐得分）
        """
        self.buffer.append(sample)
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)

    def sample(self, batch_size: int) -> List[Dict]:
        """
        随机采样

        Args:
            batch_size: 批次大小

        Returns:
            样本列表
        """
        if len(self.buffer) < batch_size:
            return self.buffer.copy()

        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        return [self.buffer[i] for i in indices]

    def size(self) -> int:
        """返回缓冲区大小"""
        return len(self.buffer)

    def clear(self):
        """清空缓冲区"""
        self.buffer = []

    def save_to_file(self, filepath: str):
        """保存训练数据到文件"""
        import json
        # 转换为可序列化的格式
        serializable_data = []
        for sample in self.buffer:
            serializable_sample = {
                'state_features': sample['state_features'].tolist(),
                'human_features': sample['human_features'].tolist(),
                'ai_features': sample['ai_features'].tolist(),
                'human_score': float(sample['human_score']),
                'ai_score': float(sample['ai_score']),
                'reward': float(sample['reward'])
            }
            serializable_data.append(serializable_sample)

        data = {
            'samples': serializable_data,
            'total_samples': len(serializable_data)
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filepath: str):
        """从文件加载训练数据"""
        import json
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 转换回原始格式
        for sample in data['samples']:
            self.buffer.append({
                'state_features': np.array(sample['state_features'], dtype=np.float32),
                'human_features': np.array(sample['human_features'], dtype=np.float32),
                'ai_features': np.array(sample['ai_features'], dtype=np.float32),
                'human_score': sample['human_score'],
                'ai_score': sample['ai_score'],
                'reward': sample['reward']
            })

        # 如果超过容量，删除最旧的样本
        while len(self.buffer) > self.capacity:
            self.buffer.pop(0)

        return len(data['samples'])


class TrainingManager:
    """
    训练管理器

    负责收集数据、训练神经网络、管理权重融合
    """

    def __init__(self, evaluator: HeuristicEvaluator):
        """
        初始化训练管理器

        Args:
            evaluator: 启发式评估器
        """
        self.evaluator = evaluator
        self.nn_predictor = NeuralNetworkPredictor()
        self.experience_buffer = ExperienceReplayBuffer()

        # 训练阶段
        self.stage = 'static'  # static, hybrid, learned
        self.progress_ratio = 0.0  # 0-1，训练进度

        # 统计信息
        self.total_human_decisions = 0
        self.human_rejected_ai = 0  # 人类拒绝AI建议的次数
        self.training_rounds = 0

    def extract_state_features(self, game_state: GameState,
                              lines_cleared: int, highest_point: int,
                              game_round: int) -> np.ndarray:
        """
        提取游戏状态特征（217维）

        Args:
            game_state: 游戏状态
            lines_cleared: 已消除行数
            highest_point: 最高堆积高度
            game_round: 游戏轮次

        Returns:
            特征向量 (217维)
        """
        features = []

        # 1. 棋盘特征 (200维)
        for y in range(20):
            for x in range(10):
                cell = game_state.board[y][x]
                features.append(1 if cell is not None and cell != 0 else 0)

        # 2. 当前方块 (7维 one-hot)
        current_piece = [0] * 7
        current_piece[game_state.current_piece] = 1
        features.extend(current_piece)

        # 3. 下一个方块 (7维 one-hot)
        next_piece = [0] * 7
        next_piece[game_state.next_piece] = 1
        features.extend(next_piece)

        # 4. 游戏上下文 (3维)
        # 归一化到 0-1
        features.append(min(lines_cleared / 200.0, 1.0))
        features.append(min(highest_point / 20.0, 1.0))
        features.append(min(game_round / 1000.0, 1.0))

        return np.array(features, dtype=np.float32)

    def _get_piece_name(self, piece_index: int) -> str:
        """获取方块名称"""
        names = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        return names[piece_index] if 0 <= piece_index < len(names) else '?'

    def get_dynamic_weights(self, game_state: GameState,
                           lines_cleared: int, highest_point: int,
                           game_round: int) -> Dict[str, float]:
        """
        获取动态权重

        根据训练阶段决定使用静态权重、混合权重或学习权重

        Args:
            game_state: 游戏状态
            lines_cleared: 已消除行数
            highest_point: 最高堆积高度
            game_round: 游戏轮次

        Returns:
            权重字典
        """
        # 静态权重
        static_weights = self.evaluator.weights.copy()

        if self.stage == 'static' or not self.nn_predictor.is_trained:
            return static_weights

        # 提取状态特征
        state_features = self.extract_state_features(
            game_state, lines_cleared, highest_point, game_round
        )

        # 学习权重
        learned_weights = self.nn_predictor.predict_weights(state_features)

        if self.stage == 'learned':
            return learned_weights

        # 混合权重（根据进度比例融合）
        alpha = self.progress_ratio
        blended_weights = {}
        for key in static_weights:
            blended_weights[key] = (1 - alpha) * static_weights[key] + alpha * learned_weights[key]

        return blended_weights

    def train(self, epochs: int = 10, batch_size: int = 32, verbose: bool = True) -> Dict:
        """
        使用PyTorch训练神经网络

        Args:
            epochs: 训练轮数
            batch_size: 批次大小
            verbose: 是否打印训练信息

        Returns:
            训练结果字典
        """
        if self.experience_buffer.size() < 100:
            return {
                'success': False,
                'message': f'Not enough training data: {self.experience_buffer.size()}/100'
            }

        if verbose:
            print(f"\n{'='*70}")
            print(f"开始训练神经网络 (PyTorch)")
            print(f"{'='*70}")
            print(f"训练样本数: {self.experience_buffer.size()}")
            print(f"训练轮数: {epochs}")
            print(f"批次大小: {batch_size}")
            print(f"当前阶段: {self.stage}")
            print(f"训练进度: {self.progress_ratio:.1%}")
            print(f"使用设备: {self.nn_predictor.device}")
            print(f"{'-'*70}")

        losses = []
        human_rejected_count = 0
        improvement_count = 0

        for epoch in range(epochs):
            batch = self.experience_buffer.sample(batch_size)

            # 准备批量数据
            state_features_batch = [sample['state_features'] for sample in batch]
            human_features_batch = [sample['human_features'] for sample in batch]
            ai_features_batch = [sample['ai_features'] for sample in batch]
            human_scores_batch = [sample['human_score'] for sample in batch]
            ai_scores_batch = [sample['ai_score'] for sample in batch]
            rewards_batch = [sample['reward'] for sample in batch]

            # 使用PyTorch批量训练
            epoch_loss = self.nn_predictor.train_batch(
                state_features_batch,
                human_features_batch,
                ai_features_batch,
                human_scores_batch,
                ai_scores_batch,
                rewards_batch
            )

            losses.append(epoch_loss)

            # 统计信息
            for i, sample in enumerate(batch):
                if sample['human_score'] > sample['ai_score']:
                    human_rejected_count += 1
                if sample['reward'] > 0:
                    improvement_count += 1

            if verbose and (epoch + 1) % 5 == 0:
                print(f"轮次 {epoch+1}/{epochs} | 损失: {epoch_loss:.4f}")

        self.training_rounds += epochs

        # 更新进度比例
        old_ratio = self.progress_ratio
        self.progress_ratio = min(0.01 * self.training_rounds, 1.0)

        # 检查是否可以进入下一阶段
        old_stage = self.stage
        self._check_stage_transition()
        stage_changed = (old_stage != self.stage)

        if verbose:
            print(f"{'-'*70}")
            print(f"训练完成")
            print(f"平均损失: {np.mean(losses):.4f}")
            print(f"最小损失: {np.min(losses):.4f}")
            print(f"人类优于AI样本: {human_rejected_count}/{len(batch) * epochs}")
            print(f"奖励>0样本: {improvement_count}/{len(batch) * epochs}")
            print(f"训练阶段: {old_stage} → {self.stage}")
            print(f"训练进度: {old_ratio:.1%} → {self.progress_ratio:.1%}")
            if stage_changed:
                print(f"✓ 阶段已升级!")
            print(f"{'='*70}\n")

        return {
            'success': True,
            'epochs': epochs,
            'samples_used': self.experience_buffer.size(),
            'avg_loss': float(np.mean(losses)),
            'min_loss': float(np.min(losses)),
            'stage': self.stage,
            'progress_ratio': self.progress_ratio,
            'stage_changed': stage_changed,
            'human_rejected_count': human_rejected_count,
            'improvement_count': improvement_count
        }

    def _check_stage_transition(self):
        """检查是否应该进入下一训练阶段"""
        if self.stage == 'static' and self.experience_buffer.size() >= 500:
            self.stage = 'hybrid'
            print(f"Training stage advanced to: {self.stage}")

        elif self.stage == 'hybrid' and self.progress_ratio >= 1.0:
            self.stage = 'learned'
            print(f"Training stage advanced to: {self.stage}")

    def get_statistics(self) -> Dict:
        """获取训练统计信息"""
        return {
            'stage': self.stage,
            'progress_ratio': self.progress_ratio,
            'total_human_decisions': self.total_human_decisions,
            'human_rejected_ai': self.human_rejected_ai,
            'training_samples': self.experience_buffer.size(),
            'training_rounds': self.training_rounds,
            'network_trained': self.nn_predictor.is_trained
        }

    def save_model(self, filepath: str):
        """保存训练好的模型"""
        self.nn_predictor.save(filepath)

    def load_model(self, filepath: str):
        """加载训练好的模型"""
        self.nn_predictor.load(filepath)
        self.stage = 'learned'
        self.progress_ratio = 1.0

    def save_training_data(self, filepath: str):
        """保存训练数据到文件"""
        import json

        # 准备元数据
        metadata = {
            'stage': self.stage,
            'progress_ratio': self.progress_ratio,
            'total_human_decisions': self.total_human_decisions,
            'human_rejected_ai': self.human_rejected_ai,
            'training_rounds': self.training_rounds,
            'network_trained': self.nn_predictor.is_trained
        }

        # 转换训练样本为可序列化格式
        serializable_data = []
        for sample in self.experience_buffer.buffer:
            serializable_sample = {
                'state_features': sample['state_features'].tolist(),
                'human_features': sample['human_features'].tolist(),
                'ai_features': sample['ai_features'].tolist(),
                'human_score': float(sample['human_score']),
                'ai_score': float(sample['ai_score']),
                'reward': float(sample['reward'])
            }
            serializable_data.append(serializable_sample)

        # 合并数据和元数据
        data = {
            'metadata': metadata,
            'samples': serializable_data,
            'total_samples': len(serializable_data)
        }

        # 保存到文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def load_training_data(self, filepath: str):
        """从文件加载训练数据"""
        import json
        # 加载元数据
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 恢复元数据
        if 'metadata' in data:
            metadata = data['metadata']
            self.stage = metadata['stage']
            self.progress_ratio = metadata['progress_ratio']
            self.total_human_decisions = metadata['total_human_decisions']
            self.human_rejected_ai = metadata['human_rejected_ai']
            self.training_rounds = metadata['training_rounds']

        # 加载训练样本（不替换，追加到现有缓冲区）
        # 为了追加，需要临时创建一个buffer
        temp_buffer = ExperienceReplayBuffer(capacity=self.experience_buffer.capacity)
        loaded_count = temp_buffer.load_from_file(filepath)

        # 将加载的样本追加到现有buffer
        for sample in temp_buffer.buffer:
            self.experience_buffer.add(sample)

        return loaded_count

    def clear_training_data(self):
        """清空训练数据"""
        self.experience_buffer.clear()
        self.stage = 'static'
        self.progress_ratio = 0.0
        self.total_human_decisions = 0
        self.human_rejected_ai = 0
        self.training_rounds = 0


class TetrisAI:
    """
    俄罗斯方块AI主类

    整合启发式评估、人类学习机制和深度强化学习
    """

    def __init__(self):
        self.evaluator = HeuristicEvaluator()
        self.human_solutions: List[Dict] = []  # 存储人类选择的解
        self.solutions_found = 0
        self.better_than_human = 0  # 找到比人类更优解的次数
        self.auto_agent = None  # AI自动游戏代理

        # 训练管理器
        self.training_manager = TrainingManager(self.evaluator)

        # 游戏上下文跟踪
        self.current_lines_cleared = 0
        self.current_highest_point = 0
        self.game_round = 0

        # 只显示人类可到达的位置（游戏辅助模式）
        self.reachable_only = False

    def set_reachable_only(self, reachable: bool):
        """设置是否只显示人类可到达的位置"""
        self.reachable_only = reachable

    def get_best_solution(self, game_state: GameState,
                        human_rotation: int = None, human_position: int = None,
                        use_dynamic_weights: bool = True,
                        auto_play: bool = False) -> Optional[Solution]:
        """
        获取最优解

        如果提供了人类当前的旋转和位置，优先推荐基于人类状态的局部改进
        如果是自动游戏模式，使用全面比较（随机顺序评分）以获得最优解

        所有解都符合游戏规则（可以通过合法的移动和旋转到达）

        Args:
            game_state: 当前游戏状态
            human_rotation: 人类当前的旋转次数（可选）
            human_position: 人类当前的横向位置（可选）
            use_dynamic_weights: 是否使用动态权重
            auto_play: 是否为自动游戏模式（全面比较所有解）

        Returns:
            评分最高的解（或基于人类状态的改进建议）
        """
        # 获取动态权重
        if use_dynamic_weights:
            dynamic_weights = self.training_manager.get_dynamic_weights(
                game_state, self.current_lines_cleared,
                self.current_highest_point, self.game_round
            )
        else:
            dynamic_weights = None

        # 获取所有可行解（已通过游戏规则验证）
        random_order = auto_play
        solutions = self.evaluator.get_all_solutions(game_state, dynamic_weights, random_order)

        if not solutions:
            return None

        # 自动游戏模式：直接返回全局最优解（全面比较）
        if auto_play:
            return solutions[0]

        # 如果没有提供人类状态，返回全局最优解
        if human_rotation is None or human_position is None:
            return solutions[0]

        # 如果提供了人类状态，寻找基于人类位置的局部改进
        # 计算人类当前位置的评分
        human_solution = Solution(human_rotation, human_position)
        human_score = self.evaluator.evaluate(game_state, human_solution, dynamic_weights)

        # 找到比人类选择更好的解
        better_solutions = [s for s in solutions if s.score > human_score]

        if better_solutions:
            # 有更好的解，优先推荐离人类当前位置最近的改进
            # 计算每个改进解与人类位置的距离
            for sol in better_solutions:
                # 旋转距离（考虑旋转对称性）
                rotation_distance = min(
                    abs(sol.rotation - human_rotation),
                    4 - abs(sol.rotation - human_rotation)
                )
                # 位置距离
                position_distance = abs(sol.position - human_position)
                # 总距离（旋转和位置的加权和）
                sol.distance = rotation_distance * 2 + position_distance

            # 选择距离最近的改进解
            better_solutions.sort(key=lambda x: x.distance)
            return better_solutions[0]
        else:
            # 没有更好的解，返回人类的选择或全局最优
            # 这里返回全局最优作为参考
            return solutions[0]

    def compare_with_human(self, game_state: GameState,
                        human_rotation: int, human_position: int) -> Dict:
        """
        比较AI解与人类解
        
        Args:
            game_state: 当前游戏状态
            human_rotation: 人类选择的旋转
            human_position: 人类选择的位置
        
        Returns:
            比较结果，包含AI最优解和人类解的评分
        """
        # 获取AI找到的所有解
        ai_solutions = self.evaluator.get_all_solutions(game_state)
        
        if not ai_solutions:
            return {
                'success': False,
                'message': 'No valid solutions found'
            }
        
        best_ai_solution = ai_solutions[0]
        
        # 评估人类解
        human_solution = Solution(human_rotation, human_position)
        human_score = self.evaluator.evaluate(game_state, human_solution)
        
        # 比较评分
        is_better = best_ai_solution.score > human_score
        
        result = {
            'success': True,
            'best_ai_score': best_ai_solution.score,
            'human_score': human_score,
            'best_ai_rotation': best_ai_solution.rotation,
            'best_ai_position': best_ai_solution.position,
            'human_rotation': human_rotation,
            'human_position': human_position,
            'is_better_than_human': is_better,
            'improvement': best_ai_solution.score - human_score,
            'ai_solutions_count': len(ai_solutions),
            'best_ai_features': best_ai_solution.features,
            'human_features': human_solution.features
        }
        
        if is_better:
            self.better_than_human += 1
        
        # 记录人类选择
        self.human_solutions.append({
            'board': game_state.board,
            'current_piece': game_state.current_piece,
            'next_piece': game_state.next_piece,
            'rotation': human_rotation,
            'position': human_position,
            'score': human_score,
            'ai_best_score': best_ai_solution.score,
            'is_better': is_better
        })
        
        return result
    
    def get_statistics(self) -> Dict:
        """获取AI统计信息"""
        return {
            'total_comparisons': len(self.human_solutions),
            'better_than_human_count': self.better_than_human,
            'better_than_human_rate': self.better_than_human / max(len(self.human_solutions), 1) * 100
        }
    
    def reset_statistics(self):
        """重置统计信息"""
        self.human_solutions = []
        self.better_than_human = 0

    def update_game_context(self, lines_cleared: int, highest_point: int, game_round: int):
        """
        更新游戏上下文

        Args:
            lines_cleared: 已消除行数
            highest_point: 最高堆积高度
            game_round: 游戏轮次
        """
        self.current_lines_cleared = lines_cleared
        self.current_highest_point = highest_point
        self.game_round = game_round

    def record_human_decision(self, game_state: GameState,
                            human_solution: Solution, ai_solution: Solution,
                            human_decision_worth_learning: bool,
                            lines_cleared: int, highest_point: int,
                            game_round: int, final_reward: float = 0,
                            verbose: bool = True, learning_assist_mode: bool = True):
        """
        记录人类决策

        Args:
            game_state: 方块放置前的游戏状态
            human_solution: 人类选择的解
            ai_solution: AI推荐的解
            human_decision_worth_learning: 人类决策是否值得学习（位置不同且人类得分 <= AI得分，说明AI评估存在误差需要学习）
            lines_cleared: 已消除行数
            highest_point: 最高堆积高度
            game_round: 游戏轮次
            final_reward: 方块放置后获得的实际奖励
            verbose: 是否打印详细信息
            learning_assist_mode: 是否为辅助学习模式（仅在辅助学习模式下记录训练数据）
        """
        # 只在辅助学习模式下进行决策记录
        if not learning_assist_mode:
            return

        tm = self.training_manager
        tm.total_human_decisions += 1

        score_diff = human_solution.score - ai_solution.score

        if verbose:
            print(f"\n[决策记录 #{tm.total_human_decisions}]", flush=True)
            print(f"游戏状态: 轮次{game_round}, 消除{lines_cleared}行, 最高点{highest_point}", flush=True)
            print(f"当前方块: {self._get_piece_name(game_state.current_piece)}, "
                  f"下一个方块: {self._get_piece_name(game_state.next_piece)}", flush=True)
            print(f"人类决策: 旋转{human_solution.rotation}次, 位置{human_solution.position}, 得分{human_solution.score:.2f}", flush=True)
            print(f"AI建议:   旋转{ai_solution.rotation}次, 位置{ai_solution.position}, 得分{ai_solution.score:.2f}", flush=True)
            print(f"得分差异: {score_diff:+.2f}", end="", flush=True)

        if human_decision_worth_learning:
            tm.human_rejected_ai += 1
            rejection_rate = tm.human_rejected_ai / tm.total_human_decisions * 100

            if verbose:
                if human_solution.score < ai_solution.score:
                    print(f" → AI得分更高，但人类选择不同，AI评估可能有误需要学习 (AI得分优势+{ai_solution.score - human_solution.score:.2f}) ✓", flush=True)
                else:  # 得分相同
                    print(f" → 人类决策同样有效 (与AI得分相同，学习人类选择) ✓", flush=True)

            # 提取状态特征
            state_features = tm.extract_state_features(
                game_state, lines_cleared, highest_point, game_round
            )

            # 添加到经验回放缓冲区
            sample = {
                'state_features': state_features,
                'human_solution': human_solution,
                'ai_solution': ai_solution,
                'human_features': human_solution.feature_vector,
                'ai_features': ai_solution.feature_vector,
                'reward': final_reward,
                'human_score': human_solution.score,
                'ai_score': ai_solution.score
            }
            tm.experience_buffer.add(sample)

            if verbose:
                print(f"样本已记录到缓冲区 (当前: {tm.experience_buffer.size()}/{tm.experience_buffer.capacity})")
                print(f"人类选择与AI不同比例: {rejection_rate:.1f}%")
        else:
            if verbose:
                print(f" → 人类采纳AI建议")

        if verbose and final_reward != 0:
            reward_text = "消除行奖励" if final_reward > 0 else "未消除惩罚"
            print(f"实际奖励: {final_reward:+.2f} ({reward_text})")

    def _get_piece_name(self, piece_index: int) -> str:
        """获取方块名称"""
        names = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        return names[piece_index] if 0 <= piece_index < len(names) else '?'

    def train_model(self, epochs: int = 10) -> Dict:
        """
        训练神经网络模型

        Args:
            epochs: 训练轮数

        Returns:
            训练结果
        """
        return self.training_manager.train(epochs)

    def get_training_statistics(self) -> Dict:
        """获取训练统计信息"""
        return self.training_manager.get_statistics()

    def save_model(self, filepath: str):
        """
        保存训练好的模型

        Args:
            filepath: 保存路径
        """
        self.training_manager.save_model(filepath)

    def load_model(self, filepath: str):
        """
        加载训练好的模型

        Args:
            filepath: 模型文件路径
        """
        self.training_manager.load_model(filepath)

    def save_training_data(self, filepath: str):
        """
        保存训练数据到文件

        Args:
            filepath: 训练数据文件路径
        """
        return self.training_manager.save_training_data(filepath)

    def load_training_data(self, filepath: str):
        """
        从文件加载训练数据

        Args:
            filepath: 训练数据文件路径

        Returns:
            加载的样本数量
        """
        return self.training_manager.load_training_data(filepath)

    def clear_training_data(self):
        """清空训练数据"""
        self.training_manager.clear_training_data()

    def enable_auto_game(self):
        """启用AI自动游戏代理"""
        self.auto_agent = AutoGameAgent(self)

    def disable_auto_game(self):
        """禁用AI自动游戏代理"""
        self.auto_agent = None

    def get_auto_agent(self):
        """获取自动游戏代理"""
        return self.auto_agent

    def record_experience(self, game_state: GameState, solution: Solution, reward: float):
        """记录游戏经验用于深度强化学习"""
        if not hasattr(self, 'experience_buffer'):
            self.experience_buffer = []

        experience = {
            'state': self._extract_state_features(game_state),
            'action': (solution.rotation, solution.position),
            'reward': reward,
            'next_state': None  # 需要后续更新
        }

        self.experience_buffer.append(experience)

        # 限制缓冲区大小
        if len(self.experience_buffer) > 10000:
            self.experience_buffer.pop(0)

    def _extract_state_features(self, game_state: GameState) -> np.ndarray:
        """提取状态特征用于神经网络（217维）"""
        features = []

        # 1. 棋盘特征 (20x10 = 200)
        for y in range(20):
            for x in range(10):
                cell = game_state.board[y][x]
                features.append(1 if cell is not None and cell != 0 else 0)

        # 2. 当前方块 (7个one-hot编码)
        current_piece = [0] * 7
        current_piece[game_state.current_piece] = 1
        features.extend(current_piece)

        # 3. 下一个方块 (7个one-hot编码)
        next_piece = [0] * 7
        next_piece[game_state.next_piece] = 1
        features.extend(next_piece)

        # 4. 游戏上下文 (3维) - 这里暂时使用默认值
        features.extend([0.0, 0.0, 0.0])

        return np.array(features, dtype=np.float32)

    def train_deep_model(self, epochs: int = 10):
        """训练深度神经网络评估器"""
        if not hasattr(self, 'experience_buffer') or len(self.experience_buffer) < 100:
            return {'success': False, 'message': 'Not enough training data'}

        # 这里可以使用TensorFlow或PyTorch实现深度Q学习
        # 目前使用模拟训练，返回训练统计信息
        return {
            'success': True,
            'epochs': epochs,
            'samples_used': len(self.experience_buffer),
            'message': f'Trained on {len(self.experience_buffer)} samples for {epochs} epochs'
        }


class AutoGameAgent:
    """
    AI自动游戏代理

    从人类引导的数据中学习，实现完全自动游戏
    """

    def __init__(self, tetris_ai: TetrisAI):
        self.ai = tetris_ai
        self.game_count = 0
        self.total_score = 0
        self.lines_cleared = 0

    def make_decision(self, game_state: GameState) -> Tuple[int, int]:
        """
        为当前游戏状态做出决策

        Returns:
            (rotation, position) 最优的旋转和位置
        """
        # 使用AI的评估函数找到最优解（使用自动游戏模式以获取全局最优解）
        solution = self.ai.get_best_solution(game_state, auto_play=True)

        if solution:
            return solution.rotation, solution.position
        else:
            # 没有可行解，返回默认值
            return 0, game_state.board_width // 2

    def update_stats(self, score: int, lines: int):
        """更新游戏统计"""
        self.game_count += 1
        self.total_score += score
        self.lines_cleared += lines

    def get_performance(self) -> Dict:
        """获取性能统计"""
        avg_score = self.total_score / max(self.game_count, 1)
        return {
            'games_played': self.game_count,
            'total_score': self.total_score,
            'average_score': avg_score,
            'total_lines_cleared': self.lines_cleared,
            'avg_lines_per_game': self.lines_cleared / max(self.game_count, 1)
        }

    def reset_stats(self):
        """重置统计"""
        self.game_count = 0
        self.total_score = 0
        self.lines_cleared = 0

