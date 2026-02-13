# AI引擎使用指南

特征	权重	说明
lines_cleared	+300	消除行数
holes	-20	空洞数量（强惩罚）
bumpiness	-1	不平整度
highest_point	-3	最高点
drop_height	+15	落点高度（正向奖励）
near_complete	+50	接近完成的行
block_contact_score	+1	方块接触评分（侧边界1分，底部3分，中间2分）
next_piece_friendly	+10	下一个方块友好度
fills_upper_gaps	+20	填补上层空缺能力
fillable_positions	+3	可填充位置数量

AI用于评分的落点、通过提示框实际展示的落点以及与人类对比的落点是不是一致的？

这里表述的三个落点都是AI的落点，只是我想知道它们到底是不是一致的。因为我发现提示框出现在了明显可以得分的位置旁边，这显然不对，当然也可能是不正确的碰撞检测导致的。已知提示框提示的位置就是AI的落地。
注意只有值为1的方格才是实体的方格才会出现碰撞。

如果都正确，那么说明评分体系存在问题，对消除空缺不敏感，反而有时候会创造出空缺，可以对比前后上下文（两个状态），搜索比人类当前的决策（人类按下A键前保持的状态）好的位置，预测下一个状态，如果能够填补上层结构，从上方向下扫描暴露出来的位置的空缺（未填满整行，但不一定是最上层/最高），则赋予更高的分数，如果创造了下一个方块无法填补的空缺则给予负向的奖励。当前的AI对人类决策能够消除一整行都还有向旁边有偏差，说明了AI不知道选择如何消除一整行，无法正确识别这样的位置，也就是无法对当前方块下落后的状态进行理解，应增强这样的理解。
让AI用于评分的落点就是提示框的落点，并对当前方块与提示框一起进行评分，从而获得这样的状态的评分和比较。

评分从某个随机位置开始，不要有顺序，这样可能搜索到更加高质量的位置。

AI自动游戏时应该对当前状态的可行解进行全面的比较，以获得最优解。同时存在问题是，人类操作也同时被响应了，不对。

已知定义，在4×4的方格中

对I形的两种状态是

| 1 | 1 | 1 | 1 |
| - | - | - | - |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |

| 1 | 0 | 0 | 0 |
| - | - | - | - |
| 1 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 |

对J形四种状态是

| 1 | 1 | 1 | 0 |
| - | - | - | - |
| 0 | 0 | 1 | 0 |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |

| 0 | 1 | 0 | 0 |
| - | - | - | - |
| 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 0 |
| 0 | 0 | 0 | 0 |

| 1 | 0 | 0 | 0 |
| - | - | - | - |
| 1 | 1 | 1 | 0 |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |

| 1 | 1 | 0 | 0 |
| - | - | - | - |
| 1 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |

对L形四种状态是

| 1 | 1 | 1 | 0 |
| - | - | - | - |
| 1 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |

| 1 | 1 | 0 | 0 |
| - | - | - | - |
| 0 | 1 | 0 | 0 |
| 0 | 1 | 0 | 0 |
| 0 | 0 | 0 | 0 |

| 0 | 0 | 1 | 0 |
| - | - | - | - |
| 1 | 1 | 1 | 0 |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |

| 1 | 0 | 0 | 0 |
| - | - | - | - |
| 1 | 0 | 0 | 0 |
| 1 | 1 | 0 | 0 |
| 0 | 0 | 0 | 0 |

对O形一种状态是

| 1 | 1 | 0 | 0 |
| - | - | - | - |
| 1 | 1 | 0 | 0 |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |

对S形四种状态是

| 0 | 1 | 1 | 0 |
| - | - | - | - |
| 1 | 1 | 0 | 0 |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |

| 1 | 0 | 0 | 0 |
| - | - | - | - |
| 1 | 1 | 0 | 0 |
| 0 | 1 | 0 | 0 |
| 0 | 0 | 0 | 0 |

对T形四种状态是

| 0 | 1 | 0 | 0 |
| - | - | - | - |
| 1 | 1 | 1 | 0 |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |

| 1 | 0 | 0 | 0 |
| - | - | - | - |
| 1 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |

| 1 | 1 | 1 | 0 |
| - | - | - | - |
| 0 | 1 | 0 | 0 |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |

| 0 | 1 | 0 | 0 |
| - | - | - | - |
| 1 | 1 | 0 | 0 |
| 0 | 1 | 0 | 0 |
| 0 | 0 | 0 | 0 |

对Z形四种状态是

| 1 | 1 | 0 | 0 |
| - | - | - | - |
| 0 | 1 | 1 | 0 |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |

| 0 | 1 | 0 | 0 |
| - | - | - | - |
| 1 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |


特征权重（可通过训练调整）

    self.weights = {
            'lines_cleared': 300.0,      # 消除行数（最重要）
            'holes': -20.0,               # 空洞数量（越少越好）
            'bumpiness': -1.0,            # 不平整度（越小越好）
            'highest_point': -3.0,          # 最高点（越低越好）
            'drop_height': 15.0,           # 落点高度（正向奖励，落点越低越好）
            'near_complete': 50.0,           # 填补接近完成的行
            'block_contact_score': 1.0,     # 方块接触评分（侧边界1分，底部3分，中间2分）
            'next_piece_friendly': 10.0,       # 对下一个方块友好度
        }
这个权重设计得合理吗？既然是权重，可以不用负号。


俄罗斯方块游戏的特点是：
单智能体（不是对弈）、离散状态（游戏状态是有限离散的）、离散动作（可行解的数量是有限的）、随着游戏轮数的推进游戏环境是时变的

我的思路是静态规则驱动：评分函数的权重（比如消除行数 + 300、空洞 - 8）是预先设定的，不会随着游戏过程 / 数据积累自动调整；如果遇到新的棋盘局面（比如非常规布局），评分规则可能不再适用，需要人工调整权重；
但是我就想在
在游戏评分机制中引入机器学习，通过人类引导游戏时AI辅助收集的游戏数据，逐步优化评分体系。利用更优的评分标准持续提升AI辅助能力，最终实现从AI辅助到AI自动游戏的演进。将原方案中的'AI对比'调整为'AI自动游戏'概念。（深度强化学习的核心目标是让系统自主习得一套最优决策规则）
更细分一点，可以这样：
第一，人类做了初始决策
第二，AI对人类的决策做了评分，并通过搜索找到了在当前评分下优于人类的决策，给出了AI辅助决策的评分
第三，人类坚持初始决策不采用AI决策，说明当前的评分需要做调整，调整到人类决策优于当前给出的AI辅助决策
第四，可以分游戏阶段以给出不同的评分依据，也就是建立规则之上的规则，也只需要建立这样的两套完善的规则即可
难点：需要细分规则
如何建立神经网络，以获得前馈输出和反馈调参呢？
你上面的额神经网络的构建思路相当于是，将当前的评分作为输入神经元，然后计算评分，也就是将这样的评分作为了函数的输入参数而不是直接相加。但是存在两个问题，第一不同的方块的输出层不同，是采用统一的扩大的方式，将不同方块的所有情况数作为输出神经元的数量；第二，人类初始决策、AI辅助决策和人类最终确定的决策如何输入到神经网络中调整网络的参数；第三，如果是这样的话，可以将游戏阶段，也就是当前消除行数、方块堆积的最高高度分别作为一个神经元参数，取消“分游戏阶段以给出不同的评分依据”的策略。

## 基于机器学习的动态评分系统

### 系统设计理念

俄罗斯方块游戏特点：

- **单智能体**：不是对弈游戏，是决策优化问题
- **离散状态**：游戏状态是有限离散的（棋盘20×10，方块7种）
- **离散动作**：可行解数量有限（9-34个）
- **时变环境**：随游戏轮数推进，棋盘状态动态变化

**核心思想**：将静态评分规则转变为基于机器学习的动态优化系统

### 系统演进阶段

#### 第一阶段：静态规则基础

保留现有静态评分规则作为基础评分函数：

```python
weights = {
    'lines_cleared': 300.0,      # 消除行数
    'drop_height': 15.0,         # 落点高度（正向奖励）
    'holes': -20.0,              # 空洞数量
    'highest_point': -3.0,       # 最高点
    'bumpiness': -1.0,           # 不平整度
    'near_complete': 50.0,       # 接近完成的行
    'block_contact_score': 1.0,  # 方块接触评分
    'next_piece_friendly': 10.0, # 下块友好度
}
```

**特点**：

- 权重固定，不随数据调整
- 可解释性强，便于调试
- 为神经网络提供初始指导

#### 第二阶段：数据收集

**人类决策数据收集流程**：

```
人类初始决策
    ↓
AI评估并生成辅助决策
    ↓
人类坚持初始决策（拒绝AI建议）
    ↓
记录差异样本用于训练
```

**数据样本结构**：

```python
# 训练样本格式
training_sample = {
    # 游戏状态特征（212维）
    'state_features': [
        # 棋盘特征 (200维)
        *board_cells,  # 20×10 = 200

        # 当前方块 one-hot (7维)
        *current_piece_encoded,  # 7

        # 下一个方块 one-hot (7维)
        *next_piece_encoded,  # 7

        # 游戏上下文特征 (3维)
        'lines_cleared': 50,      # 已消除行数
        'highest_point': 8,       # 最高堆积高度
        'game_round': 150,        # 游戏轮次
    ],

    # 人类选择的动作
    'human_action': {
        'rotation': 0,
        'position': 6,
        'score': 245.5  # 静态规则评分
    },

    # AI推荐的更优动作
    'ai_action': {
        'rotation': 1,
        'position': 3,
        'score': 285.8
    },

    # 奖励信号（人类坚持选择，说明人类决策优于AI）
    'reward': 40.3  # 人类最终得分 - AI推荐得分
}
```

**关键设计决策**：

1. **为什么用游戏上下文替代"分阶段规则"**？

   - 将 `lines_cleared`、`highest_point`、`game_round` 作为神经网络输入
   - 网络自动学习不同阶段的策略
   - 避免人工设定阶段阈值（如"前50行用策略A，后50行用策略B"）
2. **为什么用奖励差值而非二分类**？

   - 保持信息密度，使用连续值 `reward = human_score - ai_score`
   - 网络学习人类决策相对AI的优势程度
   - 支持梯度下降，便于反向传播

#### 第三阶段：神经网络设计

**核心问题：训练结果究竟是什么？**

训练的结果是**动态权重函数**，而不是直接的动作评分：

```
输入：217维游戏状态特征
  ├─ 棋盘：200维 (20×10)
  ├─ 当前方块：7维 (one-hot)
  ├─ 下一个方块：7维 (one-hot)
  └─ 游戏上下文：3维
      ├─ lines_cleared（已消除行数）
      ├─ highest_point（最高点）
      └─ game_round（游戏轮次）

输出：9个动态权重
  ├─ lines_cleared权重

  ├─ holes权重
  ├─ bumpiness权重
  ├─ highest_point权重
  ├─ drop_height权重
  ├─ near_complete权重
  ├─ block_contact_score权重
  └─ next_piece_friendly权重

评分计算：
score = Σ(权重_i × 特征_i)
```

**不是"状态-动作对"，而是"状态→权重"的映射**

这意味着：
- 同样是"消除1行"，在不同游戏阶段（开局vs残局），消除行的权重可能不同
- 同样是"产生空洞"，在不同棋盘结构下，空洞的惩罚程度可能不同
- 网络学习的是：**在不同状态下，哪些特征更重要**

**与传统Q值网络的区别**：

| 传统Q值网络 | 当前权重网络 |
|-----------|-------------|
| 输入：状态 | 输入：状态 |
| 输出：每个动作的Q值 | 输出：特征权重 |
| 直接选最大Q值动作 | 用权重计算特征得分后再选最优 |
| 不需要特征提取 | 保留13个特征的可解释性 |

**为什么选择权重预测而非直接Q值预测？**

1. **可解释性强**：仍基于13个清晰的特征（消除行、空洞、高度等）
2. **泛化能力强**：学习的是特征重要性，而非特定动作
3. **训练稳定**：Ranking Loss比时序差分更稳定
4. **渐进式进化**：可以从静态权重平滑过渡到学习权重

**改进方案1：动态掩码输出层**

```python
# 输出层固定为最大可行解数（34）
# 使用掩码将无效位置的输出设为 -∞

class TetrisMLP(nn.Module):
    def __init__(self):
        self.network = nn.Sequential(
            nn.Linear(212, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 34)  # 输出34个Q值（最大可行解数）
        )

    def forward(self, state_features, piece_type):
        q_values = self.network(state_features)

        # 根据方块类型应用掩码
        mask = self._get_mask(piece_type)  # 例如T形: [1]*34
        q_values = q_values * mask

        return q_values

    def _get_mask(self, piece_type):
        # 返回有效位置掩码
        piece_info = {
            'I': (2, [7, 10]),  # 2种旋转，对应7和10个位置
            'O': (1, [9]),      # 1种旋转，9个位置
            'S': (2, [8, 8]),   # 2种旋转，每种8个位置
            'Z': (2, [8, 8]),
            'T': (4, [8, 9, 8, 9]),  # 4种旋转，交替8/9个位置
            'J': (4, [8, 8, 8, 8]),
            'L': (4, [8, 8, 8, 8])
        }

        rotations, positions_per_rotation = piece_info[piece_type]
        total_solutions = sum(positions_per_rotation)
        mask = torch.zeros(34)
        mask[:total_solutions] = 1
        return mask
```

**推荐方案：权重预测网络（已实现）**

```python
import torch
import torch.nn as nn
import torch.optim as optim

class WeightPredictor(nn.Module):
    """
    权重预测神经网络

    输入：217维游戏状态特征
    输出：9个动态特征权重
    """
    def __init__(self, input_dim=217, hidden_dims=[256, 128, 64], output_dim=9):
        super(WeightPredictor, self).__init__()

        # 构建网络
        layers = []
        prev_dim = input_dim

        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(0.2)
            ])
            prev_dim = hidden_dim

        # 输出层（直接输出权重值）
        layers.append(nn.Linear(prev_dim, output_dim))

        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)
```

**训练方法：Ranking Loss**

```python
def train_weight_predictor(weight_predictor, human_samples, optimizer, epochs=100):
    """
    训练权重预测网络

    人类坚持初始决策 → 人类决策 > AI推荐
    → 调整权重使得人类决策的动态评分 > AI推荐的评分
    """
    for epoch in range(epochs):
        optimizer.zero_grad()

        # 前向传播：预测动态权重
        weights = weight_predictor(human_samples['state_features'])

        # 计算人类决策和AI决策的得分
        # 关键：使用同一套预测权重分别计算
        human_scores = torch.sum(weights * human_samples['human_features'], dim=1)
        ai_scores = torch.sum(weights * human_samples['ai_features'], dim=1)

        # 创建目标：人类得分应该高于AI得分
        target = torch.ones_like(human_scores)

        # 计算Ranking Loss
        criterion = nn.MarginRankingLoss(margin=10.0)
        loss = criterion(human_scores, ai_scores, target)

        # 反向传播
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

    return weight_predictor
```

**使用训练后的网络进行评估**：

```python
def evaluate_with_learned_weights(game_state, solution, weight_predictor):
    """
    使用学习到的动态权重评估解

    Args:
        game_state: 游戏状态
        solution: 待评估的解(旋转+位置)
        weight_predictor: 训练好的权重预测网络

    Returns:
        动态评分
    """
    # 1. 提取游戏状态特征（217维）
    state_features = extract_state_features(game_state)

    # 2. 神经网络预测动态权重（9维）
    with torch.no_grad():
        state_tensor = torch.FloatTensor(state_features).unsqueeze(0)
        predicted_weights = weight_predictor(state_tensor).squeeze()

    # 3. 提取解的特征（13维）
    features = extract_features(game_state, solution)

    # 4. 计算动态评分
    score = torch.sum(predicted_weights * torch.FloatTensor(features))

    return score.item()
```

**训练结果解释**：

```python
# 训练前（静态权重）
static_weights = {'lines_cleared': 300.0, 'holes': -8.0, ...}
score = Σ(static_weights[i] × features[i])

# 训练后（动态权重）
# 对于每个不同状态，网络输出不同的权重
def get_weights_for_state(game_state):
    state_features = extract_state_features(game_state)  # 217维
    weights = weight_network(state_features)  # 9维，随状态变化
    return weights

# 示例：同一特征在不同状态下的权重变化
state_early_game = extract_state_features(early_game_state)
state_late_game = extract_state_features(late_game_state)

weights_early = weight_network(state_early_game)
weights_late = weight_network(state_late_game)

# 可能结果：
# 开局时：lines_cleared权重250，next_piece_friendly权重20
# 残局时：lines_cleared权重350，next_piece_friendly权重5
```

#### 第四阶段：渐进式优化

**权重融合策略**：

```python
def evaluate_with_blended_weights(game_state, solution, progress_ratio):
    """
    progress_ratio: 0-1，表示训练进度
    0 = 完全使用静态权重
    1 = 完全使用学习权重
    """
    # 静态权重
    static_weights = {
        'lines_cleared': 300.0,
        'holes': -8.0,
        # ...
    }

    # 学习权重
    state_features = extract_state_features(game_state)
    learned_weights = weight_network(state_features)

    # 融合权重
    blended_weights = {}
    for key in static_weights:
        alpha = progress_ratio  # 随着训练增加，逐渐依赖学习权重
        blended_weights[key] = (
            (1 - alpha) * static_weights[key] +
            alpha * learned_weights[key].item()
        )

    # 计算得分
    features = extract_features(game_state, solution)
    score = sum(blended_weights[k] * features[k] for k in blended_weights)

    return score
```

**训练触发条件**：

```
1. 数据量阈值：收集至少100个人类-AI差异样本
2. 游戏轮次：每50轮触发一次训练
3. 性能下降：如果AI超人类率连续下降，触发训练
4. 手动触发：用户主动点击"训练AI"按钮
```

#### 第五阶段：完全自主学习

目标：实现从静态规则到完全自主学习的过渡

```python
class SelfTrainingAI:
    def __init__(self):
        self.stage = 'static'  # static → hybrid → learned
        self.weight_network = WeightPredictor()
        self.experience_replay = ExperienceReplay(capacity=50000)

    def get_best_solution(self, game_state):
        if self.stage == 'static':
            return self._static_best_solution(game_state)
        elif self.stage == 'hybrid':
            return self._hybrid_best_solution(game_state)
        else:
            return self._learned_best_solution(game_state)

    def train_with_human_feedback(self):
        """从人类反馈中学习"""
        samples = self._collect_human_feedback_samples()
        self._train_network(samples)

        # 检查是否可以进入下一阶段
        if self._check_stage_transition():
            self._advance_stage()

    def _check_stage_transition(self):
        """检查是否应该进入下一阶段"""
        stats = self.get_statistics()
        human_data_count = len(self.experience_replay.human_samples)
        ai_performance = stats['ai_better_than_human_rate']

        if self.stage == 'static' and human_data_count > 500:
            return True  # 进入混合模式
        elif self.stage == 'hybrid' and ai_performance > 70:
            return True  # 进入完全学习模式
        return False
```

### 训练机制详解

#### 损失函数设计

```python
def compute_loss(network, batch_samples):
    """
    批量计算损失

    batch_samples: 包含多个人类-AI差异样本
    """
    total_loss = 0

    for sample in batch_samples:
        # 1. 提取特征
        state = sample['state_features']
        human_features = sample['human_action']['features']
        ai_features = sample['ai_action']['features']

        # 2. 预测权重
        weights = network(state)

        # 3. 计算得分
        human_score = compute_weighted_score(weights, human_features)
        ai_score = compute_weighted_score(weights, ai_features)

        # 4. 对比损失（Ranking Loss）
        # 人类决策应优于AI决策
        margin = 20  # 最小得分差
        loss = F.relu(ai_score - human_score + margin)

        total_loss += loss

    return total_loss / len(batch_samples)
```

#### 数据增强策略

为了提高泛化能力，对每个样本进行数据增强：

```python
def augment_sample(original_sample):
    """数据增强：在保持决策差异的前提下生成新样本"""

    augmentations = []

    # 1. 棋盘水平翻转（对称性）
    flipped_board = flip_horizontally(original_sample['board'])
    augmentations.append({
        'state_features': extract_features(flipped_board, ...),
        'human_action': {
            'position': 9 - original_sample['human_action']['position'],  # 对称位置
            'rotation': original_sample['human_action']['rotation'],
            ...
        },
        'ai_action': {
            'position': 9 - original_sample['ai_action']['position'],
            'rotation': original_sample['ai_action']['rotation'],
            ...
        }
    })

    # 2. 噪声注入（小幅扰动棋盘）
    for _ in range(3):
        noisy_board = add_noise(original_sample['board'], noise_level=0.05)
        augmentations.append({
            'state_features': extract_features(noisy_board, ...),
            'human_action': original_sample['human_action'],
            'ai_action': original_sample['ai_action']
        })

    return augmentations
```

#### 在线学习机制

```python
def online_learning_step(game_state, human_solution, ai_solution, human_final_score):
    """
    在线学习：每一步都可能更新网络

    参数：
    - game_state: 方块放置前的游戏状态
    - human_solution: 人类选择的解（旋转+位置）
    - ai_solution: AI推荐的解
    - human_final_score: 方块放置后获得的实际奖励（消除行数等）
    """

    # 1. 提取特征
    state_features = extract_state_features(game_state)
    human_features = extract_features(game_state, human_solution)
    ai_features = extract_features(game_state, ai_solution)

    # 2. 计算损失
    weights = weight_network(state_features)
    human_pred = compute_weighted_score(weights, human_features)
    ai_pred = compute_weighted_score(weights, ai_features)

    # 如果人类最终得分高，说明人类决策更优
    if human_final_score > 0:  # 消除了行
        target_diff = human_final_score  # 正奖励
    else:
        target_diff = -10  # 未消除行，轻微惩罚

    loss = F.relu(ai_pred - human_pred - target_diff)

    # 3. 反向传播
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

    # 4. 保存到经验回放
    experience_replay.add({
        'state': state_features,
        'human_features': human_features,
        'ai_features': ai_features,
        'reward': target_diff
    })
```

### 系统可解释性

为了保持系统可解释性，设计特征重要性分析：

```python
def analyze_feature_importance(network, sample_state):
    """分析在特定状态下各特征的重要性"""

    # 计算梯度
    state_features = extract_state_features(sample_state)
    state_tensor = torch.tensor(state_features, requires_grad=True)

    weights = network(state_tensor)
    total_score = weights.sum()

    # 反向传播获取梯度
    total_score.backward()
    gradients = state_tensor.grad

    # 特征重要性排序
    feature_names = [
        # 棋盘特征（200个）
        *[f'board_{y}_{x}' for y in range(20) for x in range(10)],
        # 当前方块
        'current_I', 'current_O', 'current_S', 'current_Z',
        'current_T', 'current_J', 'current_L',
        # 下一个方块
        'next_I', 'next_O', 'next_S', 'next_Z',
        'next_T', 'next_J', 'next_L',
        # 上下文
        'lines_cleared', 'highest_point', 'game_round'
    ]

    importance = sorted(
        zip(feature_names, gradients.abs().tolist()),
        key=lambda x: x[1],
        reverse=True
    )

    return importance[:10]  # 返回最重要的10个特征
```

### 实施路线图

**阶段1（已实现）**：

- ✅ 静态评分规则
- ✅ AI辅助模式（A键触发）
- ✅ AI自动游戏模式
- ✅ 经验记录机制

**阶段2（待实现）**：

- ⏳ 神经网络架构搭建
- ⏳ 人类-AI差异数据收集
- ⏳ 训练管道实现

**阶段3（待实现）**：

- ⏳ 混合权重评估
- ⏳ 在线学习机制
- ⏳ 自动阶段转换

**阶段4（待实现）**：

- ⏳ 完全自主学习
- ⏳ 自我对弈优化
- ⏳ 性能监控和调优

## 深度强化学习与AI演进

### AI能力演进路线

```
人类辅助 → 数据收集 → 模型训练 → AI自动游戏
```

**第一阶段：人类辅助**

- 使用启发式评估函数提供游戏建议
- 人类玩家按A键获取AI建议
- 基于人类当前位置推荐局部改进
- 记录人类游戏数据用于训练

**第二阶段：数据收集**

- 记录游戏状态、人类决策、奖励信号
- 建立经验回放缓冲区
- 分析AI超人类决策的比例
- 识别AI优势领域和待改进区域

**第三阶段：模型训练**

- 使用深度Q学习(DQN)训练神经网络
- 从人类数据中学习最优决策模式
- 持续优化评估函数权重
- 实现从启发式到深度学习的过渡

**第四阶段：AI自动游戏**

- AI完全控制游戏决策
- 实时选择最优放置位置
- 持续学习和自我改进
- 目标：超越人类游戏水平

### 深度强化学习核心概念

**Q学习框架**：

```
Q(state, action) = 预期累积奖励

状态(State): 棋盘 + 当前方块 + 下一个方块
动作(Action): (旋转, 位置) 的组合
奖励(Reward): 消除行数 - 惩罚(空洞、高度等)
```

**神经网络架构**：

- 输入层：214维特征向量（棋盘200 + 方块14）
- 隐藏层：2-3层全连接层，使用ReLU激活
- 输出层：动作价值Q值
- 损失函数：时序差分(TD)误差

**训练流程**：

1. 收集人类游戏经验
2. 随机采样构建训练批次
3. 计算目标Q值：`r + γ * max Q(s', a')`
4. 更新网络参数最小化TD误差
5. 定期更新目标网络保证稳定

## 核心原理：可行解生成与评分机制

### 问题建模视角

俄罗斯方块的每个决策都可以建模为一个优化问题：

```
问题状态 = 当前棋盘状态 + 当前方块 + 下一个方块
可行解空间 = 所有合法的(旋转次数, 横向位置)组合
最优解 = 评估得分最高的可行解
```

### 可行解的生成方法

**可行解定义**：一个可行解是指当前方块在棋盘上的所有合法放置方式，每个解由两个参数唯一确定：

- **旋转次数** (rotation)：0、1、2、3（分别代表4种旋转状态）
- **横向位置** (position)：方块左侧所在的列索引（0-9）

**可行解生成算法**：

1. **枚举唯一旋转状态**

   - 对于当前方块，遍历不重复的旋转状态
   - 不同方块的有效旋转状态数量不同：
     - **I形（长条）**：2种状态（横向、竖向）
     - **O形（正方形）**：1种状态（所有旋转都相同）
     - **J形、L形、T形**：4种状态（每种旋转都不同）
     - **S形、Z形**：2种状态（两种镜像对称状态）
   - 获取每种旋转状态下的方块形状矩阵
2. **确定有效位置范围**

   - 根据方块的宽度计算可放置的列范围
   - 例如：I形方块（宽4格）的有效位置是 0-6
   - O形方块（宽2格）的有效位置是 0-8
3. **深度落点机制（重要）**

   - 可行解的位置不是方块的初始Y坐标，而是**落到底部后的最终位置**
   - 算法模拟方块从顶部（Y=0）开始，**自然下落**直到碰到底部或已有方块
   - 这个过程中不限制中间路径，只检查最终落点是否合法

   **关于"下移后旋转平移"的说明**：

   - 理论上，"下移→旋转→再下移"可能产生额外解
   - 但实际上，这样的操作最终落点等同于直接在某个位置旋转后下落
   - 例如：在位置0下移5格→旋转→再下移到位置3，等同于直接在位置3旋转后下移
   - 因此，当前算法通过枚举所有(旋转, 位置)组合已经覆盖了所有可能的最终落点
   - AI评估的是方块的最终放置位置，而不关心到达该位置的路径
4. **合法性验证**

   - 落点后的方块不超出棋盘边界（0-9列，0-19行）
   - 落点后的方块不与现有方块重叠
   - 通过验证的组合构成可行解集合

**示例**：

```
当前方块：I形（长条）
棋盘状态：第5行有部分方块

可行解枚举（去重后）：
- 旋转0（横向）：位置0、1、2、3、4、5、6 → 7个解
- 旋转1（竖向）：位置0、1、2、3、4、5、6、7、8、9 → 10个解

总计：17个可行解（去重前为34个，实际只有17个唯一解）

每个可行解的落点位置通过模拟计算：
例如：旋转0，位置3
  1. 方块从Y=0、X=3开始
  2. 模拟下落，检查每一步是否碰撞
  3. 假设在Y=15处碰到第5行的方块
  4. 该可行解的最终落点：(X=3, Y=15)
```

**各方块类型可行解数量**：

| 方块类型 | 唯一旋转数 | 有效位置范围  | 可行解数量 |
| -------- | ---------- | ------------- | ---------- |
| I形      | 2          | 7个或10个位置 | 17         |
| J形      | 4          | 8个位置       | 32         |
| L形      | 4          | 8个位置       | 32         |
| O形      | 1          | 9个位置       | 9          |
| S形      | 2          | 8个位置       | 16         |
| T形      | 4          | 8个或9个位置  | 34         |
| Z形      | 2          | 8个位置       | 16         |

### 评分机制与最优解选择

**多特征评分函数**：

每个可行解通过评估函数计算得分，得分越高表示该位置越优。评估函数综合考虑9个特征：

1. **消除行数** (权重: +300)

   - 放置后可以消除的完整行数
   - 消除4行得分最高（+1200）
   - 这是得分的主要来源
2. **落点高度** (权重: -15/行)

   - 方块最终落点的Y坐标
   - 落点越低，未来空间越大
   - 优先选择能落到底部或低位置的解
3. **空洞数量** (权重: -8/个)

   - 方块内部被上方方块遮挡的空格
   - 空洞极难填补，应严厉避免
   - 好的解不会产生空洞
4. **最高点** (权重: -6/行)

   - 棋盘最上方方块的高度
   - 最高点接近顶部会增加游戏失败风险
5. **总高度** (权重: -2/格)

   - 所有列高度的总和
   - 反映整体棋盘的拥挤程度
6. **不平整度** (权重: -2/差)

   - 相邻列之间高度差的绝对值之和
   - 表面越平整，后续放置越容易
7. **接近完成的行数** (权重: +50/加权行)

   - 已经有8-9个方块的行
   - 填补这些行为后续消除做准备
   - **关键**：底部行接近完成得分高，顶部行接近完成得分低
   - 权重计算：(y + 1) / 20，底部权重接近1，顶部权重接近0.05
   - 避免以留下底部空缺为代价让顶部接近完成
8. **方块接触评分** (权重: +1/分)

   - 计算放置后方块与周围环境的接触情况
   - 与侧边界接触：每接触1次得1分
   - 与底部方块/底边界接触：每接触1次得3分
   - 与中间方块（其他方块）接触：每接触1次得2分
   - 鼓励方块与其他方块或边界有更多接触，提高结构稳定性
9. **对下一个方块友好度** (权重: +10/分)

   - 计算下一个方块的得分潜力（最佳位置得分）
   - 鼓励当前块为下一个块留出更好的位置
   - 考虑消除行数、接近完成的行、空洞数量、最高点等
   - 超前考虑，避免当前块占据对下个方块更有利的位置

**评分计算示例**：

```
可行解A：旋转0，位置3
- 消除行数：2行 → 2 × 300 = +600
- 落点高度：第5行 → 5 × (-15) = -75
- 空洞数量：0个 → 0 × (-8) = 0
- 最高点：第8行 → 8 × (-6) = -48
- 对下一个方块友好度：15个位置 → 15 × 10 = +150
- 其他特征总和：+20

总分 = 600 - 75 + 0 - 48 + 150 + 20 = 647

可行解B：旋转1，位置5
- 消除行数：0行 → 0 × 300 = 0
- 落点高度：第12行 → 12 × (-15) = -180
- 空洞数量：1个 → 1 × (-8) = -8
- 最高点：第15行 → 15 × (-6) = -90
- 对下一个方块友好度：8个位置 → 8 × 10 = +80
- 其他特征总和：-30

总分 = 0 - 180 - 8 - 90 + 80 - 30 = -228

结论：可行解A（647分）优于可行解B（-228分），选择A作为最优解
```

### 下一个方块的作用

虽然可行解主要由当前局面和当前方块确定，但**下一个方块在评分中起关键作用**：

1. **直接影响**：通过"对下一个方块友好度"特征，为当前解加分或减分

   - AI会模拟下一个方块的放置，统计其可行位置数量
   - 当前放置如果限制了下一个方块的选择，会降低评分
2. **间接影响**：下一个方块的类型影响评分策略

   - 如果下一个是I形，当前应预留长条空间
   - 如果下一个是L形，当前应避免产生深坑
3. **策略多样性**：不同下一个方块导致不同最优解

   - 同一局面+当前方块+下一个I形 → 可能选择横向放置
   - 同一局面+当前方块+下一个T形 → 可能选择竖向放置

### AI寻找超人类较优解的时机

**触发条件**：

- 用户按下 **A键** 时
- 游戏处于非暂停、非结束状态
- AI辅助模式已启用

**工作流程**：

```
1. 方块出现
   ↓
2. 用户可以先旋转和移动方块到想要的位置
   ↓
3. 用户按下A键（可以在任意时刻多次按下）
   ↓
4. AI开始寻找基于人类当前状态的改进建议
   - 生成所有可行解（9-32个，取决于方块类型）
   - 计算人类当前选择的得分
   - 找出比人类选择更好的所有解
   - 在改进解中选择距离最近的解推荐
   ↓
5. 显示AI建议框（绿色虚线框+状态栏文字）
   - 提示框持续显示直到方块锁定
   - 如果用户调整位置后再次按A键，会重新计算
   ↓
6. 方块锁定，新方块出现
   ↓
7. AI建议自动清除，等待下一次A键触发
```

**重要特性**：

- 显示提示框后，如果用户调整了方块位置（旋转或移动），**再次按下A键会重新计算**
- AI会根据人类新的当前位置重新推荐改进建议
- 这样可以多次交互，逐步找到最优位置
- 确保用户看到的是稳定的建议

**对比模式下的时机**：

- 用户无需按键
- 每次方块锁定后自动触发对比
- 显示人类选择vs AI最优的对比窗口

### AI评估函数的深度学习潜力

当前使用**启发式评估**（手工特征+固定权重），为深度学习奠定基础：

**未来改进方向**：

1. 用神经网络替代手工特征提取

   - 输入：棋盘状态、当前方块、下一个方块
   - 输出：每个可行解的评分
   - 训练数据：人类游戏记录+AI对比结果
2. 端到端学习

   - 不需要手工设计特征
   - 网络自动学习什么位置好、什么位置差
   - 可能发现人类未注意的策略
3. 强化学习

   - AI自我对弈
   - 通过游戏结果（消除行数、存活时间）优化评估函数
   - 无需人类标签

当前启发式评估的优点：

- 计算快速（10-50ms）
- 可解释性强（每个特征的贡献清晰）
- 稳定可靠（不会产生离谱建议）
- 便于调试和调整

## 快速开始

### 1. 安装依赖

```bash
cd pyqt5_gui
pip install -r requirements.txt
```

### 2. 启动游戏

```bash
# Windows
.\run.bat

# Linux/Mac
bash run.sh
```

### 3. 启用AI模式

- 在游戏界面右侧的下拉菜单选择AI模式
- 推荐先使用"AI辅助"模式体验
- 熟悉后可切换到"AI对比"模式进行深度分析

## AI核心概念

### 问题建模

将每次方块决策视为一个优化问题：

```
输入: 棋盘状态 + 当前方块 + 下一个方块
解空间: 所有有效的(旋转, 位置)组合
目标: 找到评分最高的解
```

### 可行解枚举

对于不同方块，可行解数量不同：

**I形方块**（2种旋转状态）：

- 旋转0（横向）：位置0-6（共7个解）
- 旋转1（竖向）：位置0-9（共10个解）
- 总计：17个可行解

**O形方块**（1种旋转状态）：

- 旋转0：位置0-8（共9个解）
- 总计：9个可行解

**J/L/T形方块**（4种旋转状态）：

- 每种旋转：位置0-7（共8个解）
- 总计：32个可行解

**S/Z形方块**（2种旋转状态）：

- 每种旋转：位置0-7（共8个解）
- 总计：16个可行解

AI会评估所有可行解后选择最优的。

### 评估特征详解

#### 1. 消除行数 (Lines Cleared)

- **含义**：放置后消除的完整行数
- **权重**：+300（最重要）
- **原理**：消除行是得分的主要来源

示例：

```
消除4行: 评分 +1200
消除1行: 评分 +300
消除0行: 评分 +0
```

#### 2. 落点高度 (Drop Height)

- **含义**：方块最终落点的Y坐标
- **权重**：-15/行
- **原理**：低位置留出更多空间

示例：

```
落在第5行: 评分 -75
落在第2行: 评分 -30
```

#### 3. 空洞数量 (Holes)

- **含义**：方块内部无法填满的空格
- **权重**：-8/个
- **原理**：空洞极难填补，应避免

示例：

```
产生0个空洞: 评分 +0
产生2个空洞: 评分 -16
```

#### 4. 最高点 (Highest Point)

- **含义**：棋盘最上方方块的高度
- **权重**：-6/行
- **原理**：最高点接近顶部会结束游戏

示例：

```
最高点10行: 评分 -60
最高点18行: 评分 -108
```

#### 5. 其他特征

| 特特征         | 权重   | 说明                                     |
| -------------- | ------ | ---------------------------------------- |
| 总高度         | -2/格  | 所有列高度之和                           |
| 不平整度       | -2/差  | 列间高度差的绝对值                       |
| 填补缺口       | +50/行 | 填补8-9格的行                            |
| 方块接触评分   | +1/分  | 侧边界1分，底部3分，中间2分              |
| 下块友好度     | +10/位 | 下一个方块的可行位置数                   |

## AI模式详解

### AI辅助模式

#### 使用场景

- 学习俄罗斯方块策略
- 了解什么位置更优
- 提升游戏水平
- 寻找基于当前放置的改进建议

#### 核心特性：基于人类状态的智能推荐

AI不是简单地给出全局最优解，而是**基于人类当前的旋转和位置**推荐改进：

```
人类的当前状态 → AI寻找更优解 → 推荐局部改进
```

**工作原理**：

1. AI评估所有可行解（9-32个）
2. 计算人类当前选择的得分
3. 找出比人类选择更好的所有解
4. 在这些改进解中，选择**距离人类当前位置最近**的解
   - 考虑旋转距离（需要旋转几次）
   - 考虑位置距离（需要移动几格）
   - 优先推荐最接近人类当前状态的改进

**示例**：

```
人类当前：旋转0次，位置7，得分50

AI评估后发现更好的解：
- 旋转1次，位置3，得分600（改进大，但距离远）
- 旋转0次，位置6，得分200（改进中等，距离近）
- 旋转0次，位置8，得分150（改进小，距离最近）

AI推荐：旋转0次，位置6，得分200 (改进)
原因：这是离人类当前位置最近的明显改进
```

#### 操作流程

1. 方块出现，你可以先旋转和移动到你想要的位置
2. 在你认为合适的时候，按 **A键** 请求AI建议
3. AI基于你当前的旋转和位置，分析所有可行解
4. 界面显示：
   - 状态栏：`AI建议: 旋转0次, 位置3, 得分245.5 (改进)`
     - 如果建议与你的位置不同，会显示"(改进)"
     - 如果已经是你的位置且得分高，会显示"(优)"
   - 游戏区：绿色虚线框显示建议落点
5. 你可以选择：
   - **跟随建议**：按AI建议的旋转和位置调整
   - **自主决策**：按自己的想法继续调整或放置

#### 示例对话

```
[游戏状态]
当前方块: I(长条)
棋盘状态: 第5行开始有堆积
你的当前: 旋转0次(横向)，位置7

[你按A键]

[AI分析]
正在评估17个可行解...
找到比当前选择更好的解:
  人类得分: 50.0
  改进解:
    - 旋转0次，位置6，得分200 (距离近)
    - 旋转0次，位置3，得分285.5 (距离远)
  推荐: 旋转0次，位置6，得分200
  原因: 离你的当前位置最近的明显改进

[你看到]
- 状态栏显示: `AI建议: 旋转0次, 位置6, 得分200.0 (改进)`
- 游戏区位置6处有绿色虚线框

[你决定]
选择跟随AI建议，按←移动到位置6
或
选择自己的想法，继续调整或直接放置

[如果你调整位置后再次按A键]
你的新位置: 旋转0次，位置5
AI基于新位置重新评估...
```

### AI对比模式

#### 使用场景

- 深度分析自己的策略
- 发现可改进之处
- 收集AI超人类的统计数据

#### 操作流程

1. 选择"AI对比"模式
2. 正常游玩
3. 每次方块锁定，自动弹出对比窗口
4. 对比窗口显示：
   - 你的选择：旋转、位置、评分
   - AI最优：旋转、位置、评分
   - 是否超人类：是/否
   - 可行解总数：AI评估了多少个候选解
   - 统计数据

#### 示例对比分析

```
[你玩的局面]
当前方块: T(丁字形)
下一个方块: L
棋盘: 第8行有较多空洞

[你的选择]
旋转: 1次
位置: 5
评分: -35.2 (产生1个空洞，落点较高)

[AI分析]
评估了32个可行解
最优解:
  旋转: 0次
  位置: 6
  评分: 125.8

[对比结果]
✓ AI找到更优解!
  人类得分: -35.2
  AI得分: 125.8
  提升: 161.0 分
  原因: AI选择落点更低，填补了缺口，对下一个方块更友好

[统计更新]
超人类: 23 / 45 (51.1%)
```

#### 对话窗口说明

```
┌────────────────────────────────┐
│  AI对比分析                │
├────────────────────────────────┤
│ 人类解: 旋转1, 位置5, 得分-35.2 │
│ AI最优: 旋转0, 位置6, 得分125.8 │
│                             │
│ ✓ AI找到更优解! 提升了 161.0 分 │
│                             │
│ 统计: AI超人类 23 次 / 总 45 次 │
│                             │
│      [      确定      ]       │
└────────────────────────────────┘
```

## 进阶技巧

### 1. 理解评分构成

当AI给出一个建议时，分析其评分构成：

```
得分285.5 = 消除2行×300 + 落点2行×(-15) + 无空洞×(-8) + ...
         = 600 - 30 + 0 + ...
         = 285.5
```

这帮助你理解AI为什么选择这个位置。

### 2. 持续改进

使用对比模式观察：

1. AI经常超人类的局面类型
2. AI很少超人类的局面类型
3. 针对性地练习这些局面

### 3. 权重调整

如果想改变AI风格，可以修改 `ai_engine.py` 中的权重：

```python
self.weights = {
    'lines_cleared': 300.0,      # 增加权重 → 更激进地消除
    'drop_height': -15.0,          # 增加负权重 → 更保守地保持低高度
    'holes': -8.0,                # 增加负权重 → 更严格地避免空洞
    # ... 其他权重
}
```

### 4. 训练AI评估函数

要真正训练一个深度学习模型：

```python
# 伪代码
from tensorflow import keras

# 1. 收集数据集
dataset = []
for game_state, human_solution in human_games:
    best_solution = ai.get_best_solution(game_state)
    features = extract_features(game_state, best_solution)
    label = 1 if best_solution.score > human_solution.score else 0
    dataset.append((features, label))

# 2. 训练模型
model = keras.Sequential([...])
model.fit(X, y, epochs=100)

# 3. 用模型预测
predicted_score = model.predict(features)
```

## 常见问题

### Q: 训练结果究竟是什么？是状态-动作对，还是不同情况下的评分机制？

A: **训练结果是动态权重函数，不是状态-动作对**

```
输入：217维游戏状态
输出：9个动态特征权重

score = Σ(weight_i × feature_i)
```

例如：
- 同样是"消除1行"，在开局时权重可能为250，残局时可能为350
- 同样是"产生空洞"，在稳定结构下惩罚-5，在不稳定结构下惩罚-15
- 网络学习的是：**在不同状态下，哪些特征更重要**

这与传统Q值网络的区别：
- Q值网络：直接输出每个动作的Q值
- 权重网络：输出特征权重，再用权重计算评分

好处：
- 保持特征的可解释性
- 训练更稳定（Ranking Loss）
- 可以从静态权重平滑过渡

### Q: 如何在现有模型基础上训练？

A: 当前系统已具备完整训练能力，步骤如下：

**1. 收集训练数据**：
- 选择"AI辅助"模式
- 正常玩游戏
- 每次人类拒绝AI建议时，自动收集样本
- 目标：收集≥100个样本

**2. 触发训练**：
- 点击"AI训练"按钮（或菜单项）
- 设置训练参数（轮数、批次大小）
- 点击"开始训练"

**3. 查看结果**：
```python
# 查看训练状态
stats = ai.get_training_statistics()
print(f"训练阶段: {stats['stage']}")  # static → hybrid → learned
print(f"训练进度: {stats['progress_ratio']:.1%}")
```

**4. 保存模型**：
```python
ai.save_model('models/weight_model.pth')
```

**当前状态**（基于 `training_data/tetris_training_data.json`）：
- 阶段：`static`（静态权重）
- 已收集：52个决策（45次人类拒绝AI）
- 训练轮数：0
- 下一步：继续收集数据至≥100个样本

### Q: AI建议总是同一个位置，怎么办？

A: 可能是评估函数过于偏向某些特征。尝试：

1. 调整 `HeuristicEvaluator` 中的权重
2. 增加 `lines_cleared` 以外特征的权重
3. 降低 `drop_height` 的权重

### Q: AI对比模式显示"人类选择更优"？

A: 这正常！AI并非总能超人类：

- AI基于启发式规则
- 人类有前瞻和直觉
- 某些复杂局面人类可能更优
- 这是收集超人类数据的最佳时机

### Q: 如何提高AI超人类率？

A: 多练习，对比模式提供反馈：

1. 注意AI超人类的局面特征
2. 学习这些局面的最优策略
3. 在类似局面尝试模仿AI
4. 统计会显示你的进步

### Q: AI辅助模式影响游戏性能吗？

A: 影响很小：

- AI分析约10-50ms（取决于解空间大小）
- 只在按A键时计算
- 不影响正常游戏流程

## 未来扩展

### 计划中的功能

1. **深度神经网络评估器**

   - 用神经网络替代手工特征
   - 从人类对弈数据中学习
2. **蒙特卡洛树搜索(MCTS)**

   - 前瞻多步，考虑未来方块的放置
   - 模拟多次随机落子，选择最优分支
3. **强化学习训练**

   - AI自我对弈训练
   - 持续改进策略
   - 无需人类标签
4. **在线学习**

   - 实时从你的选择中学习
   - 逐步个性化AI评估函数
   - 越玩越适合你的风格
5. **性能分析工具**

   - 回放游戏对局
   - 逐步分析每个决策
   - 生成改进报告

## 技术架构

```
TetrisAI (主控制器)
    ├── HeuristicEvaluator (评估器)
    │   ├── evaluate() - 评估单个解
    │   ├── _simulate_placement() - 模拟放置
    │   ├── _extract_features() - 提取特征
    │   └── weights - 特征权重
    ├── get_all_solutions() - 枚举所有可行解
    ├── get_best_solution() - 返回最优解
    ├── compare_with_human() - 对比人类选择
    └── human_solutions[] - 存储人类选择历史

GameState (状态表示)
    ├── board[20][10] - 棋盘
    ├── current_piece - 当前方块
    └── next_piece - 下一个方块

Solution (解表示)
    ├── rotation - 旋转次数
    ├── position - 横向位置
    ├── score - 评估得分
    └── features - 特征字典
```

## 贡献和反馈

如果你有改进建议或发现bug，请：

1. 记录具体的局面和AI行为
2. 分析评估特征是否合理
3. 尝试调整权重参数
4. 提供反馈或代码改进
