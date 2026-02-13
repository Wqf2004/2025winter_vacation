/*
 * 俄罗斯方块 AI 助手 - 基于强化学习
 * 使用 Q-Learning 算法实现智能决策
 */

#ifndef TETRIS_AI_H
#define TETRIS_AI_H

// 游戏状态特征
typedef struct {
    int aggregate_height;    // 总高度
    int complete_lines;     // 消除的行数
    int holes;             // 空洞数量
    int bumpiness;         // 表面不平整度
    int highest_point;      // 最高点
    int bottom_line_coverage; // 底层覆盖率（0-10，表示底层有多少列被填充）
    int near_complete_lines; // 接近完成的行数（已填8-9格的行数）
    int deepest_line_gap;    // 最深的连续空缺（用于判断是否容易消除）
} GameStateFeatures;

// 基于特征的状态空间设计
// 将连续特征离散化为有限的类别
#define HEIGHT_LEVELS 5      // 高度等级：[0-3], [4-7], [8-11], [12-15], [16+]
#define HOLE_LEVELS 4       // 空洞等级：[0], [1-3], [4-6], [7+]
#define BUMPINESS_LEVELS 5  // 不平整度等级：[0-3], [4-7], [8-11], [12-15], [16+]

// 新的Q表大小：7(当前方块) * 7(下一个方块) * 5(高度) * 4(空洞) * 5(不平整度) * 40(动作) = 196000
#define Q_TABLE_SIZE (7 * 7 * HEIGHT_LEVELS * HOLE_LEVELS * BUMPINESS_LEVELS * 40)

// 旧Q表大小（向后兼容）
#define OLD_Q_TABLE_SIZE (7 * 7 * 4 * 10)  // 1960

typedef struct {
    double q_values[Q_TABLE_SIZE];
    int num_states;
    double learning_rate;      // 学习率
    double discount_factor;    // 折扣因子
    double exploration_rate;   // 探索率
} QLearningAgent;

// AI 决策结果
typedef struct {
    int rotation;      // 旋转次数 (0-3)
    int position;      // 落下位置 (0-WIDTH-1)
    double confidence; // 置信度
} AIDecision;

// 初始化 AI 代理
void init_ql_agent(QLearningAgent* agent);

// 基于启发式知识初始化Q表（注入先验知识）
void init_q_table_with_heuristics(QLearningAgent* agent);

// 从文件加载 Q 表
int load_q_table(QLearningAgent* agent, const char* filename);

// 保存 Q 表到文件
void save_q_table(QLearningAgent* agent, const char* filename);

// 获取状态索引（旧版本，仅基于方块类型）
int get_state_index(int shape, int rotation, int position);

// 计算基于特征的状态索引（新版本）
int get_feature_based_state_index(int current_shape, int next_shape,
                                   int height_level, int holes_level,
                                   int bumpiness_level);

// 提取游戏状态特征
void extract_game_features(int board[20][10], GameStateFeatures* features);

// 计算状态奖励
double calculate_reward(const GameStateFeatures* before, const GameStateFeatures* after, int lines_cleared);

// 计算底层覆盖率（返回0-10之间的数值）
int calculate_bottom_line_coverage(int board[20][10]);

// 将特征离散化为状态索引
int get_feature_based_state_index(int current_shape, int next_shape,
                                   int height_level, int holes_level,
                                   int bumpiness_level);

// 获取特征的离散化等级
void discretize_features(const GameStateFeatures* features,
                         int* height_level, int* holes_level,
                         int* bumpiness_level);

// AI 决策：选择最佳动作
AIDecision ai_make_decision(QLearningAgent* agent, int current_shape, int next_shape, int board[20][10]);

// 检查碰撞（需要在主程序中实现）
extern int check_collision(int shape, int rotation, int x, int y);

// 检查某个旋转和位置组合是否有效（边界检测）
int is_valid_action(int board[20][10], int shape, int rotation, int position);

// 获取方块的有效位置范围
void get_valid_positions(int shape, int rotation, int* min_pos, int* max_pos);

// 训练 AI：更新 Q 值
void ai_train(QLearningAgent* agent, int state_idx, int action, int next_state_idx, double reward);

// ε-贪心策略选择动作（考虑边界限制）
int select_action_with_validation(QLearningAgent* agent, int state_idx, int current_shape, int board[20][10]);

// ε-贪心策略选择动作（原始版本，不考虑边界）
int select_action_epsilon_greedy(QLearningAgent* agent, int state_idx);

// 简单启发式评估（用于快速决策）
AIDecision heuristic_make_decision(int board[20][10], int current_shape, int next_shape);

#endif // TETRIS_AI_H
