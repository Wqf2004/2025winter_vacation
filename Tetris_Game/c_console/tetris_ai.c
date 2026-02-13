/*
 * 俄罗斯方块 AI 助手实现 - Q-Learning 算法
 */

#include "tetris_ai.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>

#define WIDTH 10
#define HEIGHT 20

// 外部定义的形状数组（与main.c一致）
extern int shapes[7][4][4];

// 外部旋转函数声明
extern void get_rotated_shape(int shape_index, int rotation_times, int result[4][4]);

// 前向声明
double evaluate_action_heuristic(int board[20][10], int current_shape, int next_shape,
                                int rotation, int position, int height_level,
                                int holes_level, int bumpiness_level);

// 计算给定旋转和位置的动作的落点高度
int calculate_drop_height(int board[20][10], int shape, int rotation, int position) {
    int temp_matrix[4][4];
    get_rotated_shape(shape, rotation, temp_matrix);

    // 找到方块的底部边界
    int bottommost = -1;
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            if (temp_matrix[j][i]) {
                if (i > bottommost) bottommost = i;
            }
        }
    }

    // 从顶部开始，找到第一个碰撞的位置
    int drop_y = 0;
    while (drop_y < HEIGHT) {
        int collision = 0;
        for (int i = 0; i < 4 && !collision; i++) {
            for (int j = 0; j < 4 && !collision; j++) {
                if (temp_matrix[j][i]) {
                    int new_x = position + j;
                    int new_y = drop_y + i + 1;

                    // 边界检查
                    if (new_x < 0 || new_x >= WIDTH || new_y >= HEIGHT) {
                        collision = 1;
                    } else if (new_y >= 0 && board[new_y][new_x] > 0) {
                        collision = 1;
                    }
                }
            }
        }
        if (collision) break;
        drop_y++;
    }

    // 返回最终落点的高度（从底部算）
    return HEIGHT - (drop_y + bottommost);
}

// 初始化 AI 代理
void init_ql_agent(QLearningAgent* agent) {
    agent->num_states = Q_TABLE_SIZE;
    agent->learning_rate = 0.05;      // 降低学习率，避免Q值爆炸
    agent->discount_factor = 0.95;    // 稍微提高折扣因子，更关注长期奖励
    agent->exploration_rate = 0.3;    // 提高探索率，避免陷入局部最优

    // 初始化 Q 值为 0
    for (int i = 0; i < Q_TABLE_SIZE; i++) {
        agent->q_values[i] = 0.0;
    }
}

// 基于启发式知识初始化Q表（注入先验知识）
void init_q_table_with_heuristics(QLearningAgent* agent) {
    printf("正在基于启发式知识初始化Q表...\n");

    // 遍历所有可能的状态
    int initialized_count = 0;

    // 使用固定种子确保初始化的一致性
    srand(42);  // 固定种子，确保每次初始化的Q表一致

    for (int current_shape = 0; current_shape < 7; current_shape++) {
        for (int next_shape = 0; next_shape < 7; next_shape++) {
            for (int height_level = 0; height_level < 5; height_level++) {
                for (int holes_level = 0; holes_level < 4; holes_level++) {
                    for (int bumpiness_level = 0; bumpiness_level < 5; bumpiness_level++) {
                        // 构建一个代表性棋盘，反映当前状态特征
                        int representative_board[20][10] = {0};

                        // 根据高度等级构建棋盘
                        int avg_height = height_level * 4;  // 0, 4, 8, 12, 16
                        for (int x = 0; x < WIDTH; x++) {
                            int column_height = avg_height;
                            // 添加一些不平整度变化
                            if (bumpiness_level > 0) {
                                column_height += (rand() % (bumpiness_level + 1)) - (bumpiness_level / 2);
                            }
                            if (column_height < 0) column_height = 0;
                            if (column_height > 19) column_height = 19;

                            // 填充该列
                            for (int y = HEIGHT - column_height; y < HEIGHT; y++) {
                                if (y >= 0) representative_board[y][x] = 1;
                            }

                            // 根据空洞等级添加空洞
                            if (holes_level > 0) {
                                int holes_to_add = holes_level * 2;
                                for (int h = 0; h < holes_to_add; h++) {
                                    int hole_y = HEIGHT - column_height + 1 + rand() % (column_height - 1);
                                    if (hole_y >= 0 && hole_y < HEIGHT && hole_y < HEIGHT - 1) {
                                        representative_board[hole_y][x] = 0;
                                    }
                                }
                            }
                        }

                        // 计算状态索引
                        int state_idx = get_feature_based_state_index(current_shape, next_shape,
                                                                       height_level, holes_level, bumpiness_level);

                        // 对该状态下的每个动作进行启发式评估
                        for (int rot = 0; rot < 4; rot++) {
                            int min_pos, max_pos;
                            get_valid_positions(current_shape, rot, &min_pos, &max_pos);

                            for (int pos = min_pos; pos <= max_pos; pos++) {
                                int action = rot * 10 + pos;
                                int q_idx = state_idx * 40 + action;

                                if (q_idx < Q_TABLE_SIZE) {
                                    // 基于启发式评估设置初始Q值
                                    double heuristic_value = evaluate_action_heuristic(
                                        representative_board, current_shape, next_shape,
                                        rot, pos, height_level, holes_level, bumpiness_level
                                    );

                                    // 限制Q值范围，避免数值过大
                                    if (heuristic_value > 500.0) heuristic_value = 500.0;
                                    if (heuristic_value < -500.0) heuristic_value = -500.0;

                                    agent->q_values[q_idx] = heuristic_value;
                                    initialized_count++;
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    printf("启发式初始化完成：共初始化 %d 个Q值\n", initialized_count);
}

// 启发式评估函数：评估给定动作的预期效果
double evaluate_action_heuristic(int board[20][10], int current_shape, int next_shape,
                                  int rotation, int position, int height_level,
                                  int holes_level, int bumpiness_level) {
    double score = 0.0;

    // 1. 评估方块形状与当前位置的契合度
    int temp_matrix[4][4];
    get_rotated_shape(current_shape, rotation, temp_matrix);

    // 计算方块的"适合度"
    int block_width = 0;
    int leftmost = 4, rightmost = -1, topmost = 4, bottommost = -1;
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            if (temp_matrix[j][i]) {
                if (j < leftmost) leftmost = j;
                if (j > rightmost) rightmost = j;
                if (i < topmost) topmost = i;
                if (i > bottommost) bottommost = i;
            }
        }
    }
    block_width = rightmost - leftmost + 1;

    // 2. 评估落点位置的列高度匹配
    int column_heights[10];
    for (int x = 0; x < WIDTH; x++) {
        column_heights[x] = 0;
        for (int y = 0; y < HEIGHT; y++) {
            if (board[y][x] != 0) {
                column_heights[x] = HEIGHT - y;
                break;
            }
        }
    }

    // 计算方块将放置位置的平均列高
    double avg_height_at_pos = 0.0;
    for (int x = position; x < position + block_width && x < WIDTH; x++) {
        avg_height_at_pos += column_heights[x];
    }
    if (block_width > 0) {
        avg_height_at_pos /= block_width;
    }

    // 3. 模拟方块落点
    int drop_y = 0;
    int can_place = 1;
    int valid_start = 1;

    // 检查初始位置是否合法
    for (int i = 0; i < 4 && valid_start; i++) {
        for (int j = 0; j < 4 && valid_start; j++) {
            if (temp_matrix[j][i]) {
                int new_x = position + j;
                int new_y = i;
                if (new_x < 0 || new_x >= WIDTH || new_y >= HEIGHT) {
                    valid_start = 0;
                } else if (new_y >= 0 && board[new_y][new_x] > 0) {
                    valid_start = 0;
                }
            }
        }
    }

    if (!valid_start) {
        can_place = 0;
    } else {
        // 找到落点
        drop_y = 0;
        while (drop_y < HEIGHT) {
            int collision = 0;
            for (int i = 0; i < 4 && !collision; i++) {
                for (int j = 0; j < 4 && !collision; j++) {
                    if (temp_matrix[j][i]) {
                        int new_x = position + j;
                        int new_y = drop_y + i + 1;
                        if (new_x < 0 || new_x >= WIDTH || new_y >= HEIGHT) {
                            collision = 1;
                        } else if (new_y >= 0 && board[new_y][new_x] > 0) {
                            collision = 1;
                        }
                    }
                }
            }
            if (collision) break;
            drop_y++;
        }
    }

    if (!can_place) {
        return -1000.0;  // 无法放置的动作惩罚
    }

    // 4. 评估放置后的效果
    // 模拟放置后的棋盘
    int temp_board[20][10] = {0};
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            temp_board[y][x] = board[y][x];
        }
    }

    // 放置方块
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            if (temp_matrix[j][i]) {
                int new_x = position + j;
                int new_y = drop_y + i;
                if (new_y >= 0 && new_y < HEIGHT && new_x >= 0 && new_x < WIDTH) {
                    temp_board[new_y][new_x] = 1;
                }
            }
        }
    }

    // 计算消除行数
    int lines_cleared = 0;
    for (int y = 0; y < HEIGHT; y++) {
        int full = 1;
        for (int x = 0; x < WIDTH; x++) {
            if (temp_board[y][x] == 0) {
                full = 0;
                break;
            }
        }
        if (full) {
            lines_cleared++;
            // 模拟消除
            for (int yy = y; yy > 0; yy--) {
                for (int x = 0; x < WIDTH; x++) {
                    temp_board[yy][x] = temp_board[yy-1][x];
                }
            }
            for (int x = 0; x < WIDTH; x++) {
                temp_board[0][x] = 0;
            }
        }
    }

    // 提取特征
    GameStateFeatures features_after;
    extract_game_features(temp_board, &features_after);

    // 计算落点高度（放置后的最高行）
    int final_height = HEIGHT - drop_y;
    if (bottommost >= 0) {
        final_height += bottommost;
    }

    // 5. 启发式评分
    // 首先给低落点高度大幅奖励（最优先）
    score += (20 - final_height) * 15.0;  // 每低1行加15分

    // 消除行奖励（最重要）
    if (lines_cleared == 1) score += 300.0;
    else if (lines_cleared == 2) score += 500.0;
    else if (lines_cleared == 3) score += 700.0;
    else if (lines_cleared == 4) score += 1200.0;

    // 高度变化惩罚（已经通过低落点奖励体现）
    score -= features_after.aggregate_height * 2.0;

    // 最高点惩罚（大幅增加，避免堆太高）
    score -= features_after.highest_point * 6.0;

    // 空洞惩罚（避免产生空洞）
    score -= features_after.holes * 8.0;

    // 不平整度惩罚
    score -= features_after.bumpiness * 2.0;

    // 填补接近完成的行（奖励填补缺口）
    if (features_after.near_complete_lines > 0) {
        score += features_after.near_complete_lines * 50.0;
    }

    // 底层覆盖率奖励
    score += features_after.bottom_line_coverage * 5.0;

    // 6. 前瞻：评估下一个方块的可放置性
    int next_valid_positions = 0;
    for (int next_rot = 0; next_rot < 4; next_rot++) {
        int min_next_pos, max_next_pos;
        get_valid_positions(next_shape, next_rot, &min_next_pos, &max_next_pos);

        for (int next_pos = min_next_pos; next_pos <= max_next_pos; next_pos++) {
            int next_valid = 1;
            int next_temp_matrix[4][4];
            get_rotated_shape(next_shape, next_rot, next_temp_matrix);

            for (int i = 0; i < 4 && next_valid; i++) {
                for (int j = 0; j < 4 && next_valid; j++) {
                    if (next_temp_matrix[j][i]) {
                        int new_x = next_pos + j;
                        int new_y = i;
                        if (new_x < 0 || new_x >= WIDTH || new_y >= HEIGHT) {
                            next_valid = 0;
                        } else if (new_y >= 0 && temp_board[new_y][new_x] > 0) {
                            next_valid = 0;
                        }
                    }
                }
            }

            if (next_valid) next_valid_positions++;
        }
    }

    // 奖励为下一个方块保留更多可放置位置
    score += next_valid_positions * 10.0;

    // 7. 根据当前状态调整评分
    // 早期游戏：优先铺好底层
    if (height_level == 0 || height_level == 1) {
        if (features_after.bottom_line_coverage >= 8) {
            score += 100.0;
        }
    }
    // 后期游戏：优先消除行
    else if (height_level >= 3) {
        if (lines_cleared > 0) {
            score += lines_cleared * 100.0;
        }
    }

    // 已经有很多空洞时，优先填补
    if (holes_level >= 2) {
        if (features_after.holes < holes_level * 2) {
            score += 80.0;
        }
    }

    // 8. 特定方块的偏好启发式
    // I方块：偏好放置在可以消除多行的位置
    if (current_shape == 0) {  // I方块
        if (lines_cleared >= 2) {
            score += 200.0;
        }
    }
    // T、L、J方块：优先填补空洞
    else if (current_shape == 1 || current_shape == 2 || current_shape == 5) {
        // 这些方块适合填补空洞
        if (features_after.holes < (holes_level * 2 + 2)) {
            score += 30.0;
        }
    }
    // O方块：适合放在平坦区域
    else if (current_shape == 3) {
        if (bumpiness_level <= 1) {
            score += 20.0;
        }
    }
    // S、Z方块：适合特定消除模式
    else if (current_shape == 4 || current_shape == 6) {
        if (lines_cleared >= 1) {
            score += 50.0;
        }
    }

    return score;
}

// 从文件加载 Q 表
int load_q_table(QLearningAgent* agent, const char* filename) {
    FILE* fp = fopen(filename, "r");
    if (fp == NULL) {
        printf("警告: 无法加载 Q 表文件 %s，使用初始化值\n", filename);
        return 0;
    }

    int loaded = 0;
    for (int i = 0; i < Q_TABLE_SIZE; i++) {
        if (fscanf(fp, "%lf", &agent->q_values[i]) == 1) {
            loaded++;
        }
    }

    fclose(fp);
    printf("成功加载 %d 个 Q 值\n", loaded);
    return loaded > 0;
}

// 保存 Q 表到文件
void save_q_table(QLearningAgent* agent, const char* filename) {
    FILE* fp = fopen(filename, "w");
    if (fp == NULL) {
        printf("错误: 无法保存 Q 表到 %s\n", filename);
        return;
    }

    for (int i = 0; i < Q_TABLE_SIZE; i++) {
        fprintf(fp, "%.6f\n", agent->q_values[i]);
    }

    fclose(fp);
    printf("Q 表已保存到 %s\n", filename);
}

// 获取状态索引
int get_state_index(int shape, int rotation, int position) {
    return shape * 40 + rotation * 10 + position;
}

// 提取游戏状态特征
void extract_game_features(int board[20][10], GameStateFeatures* features) {
    features->aggregate_height = 0;
    features->complete_lines = 0;
    features->holes = 0;
    features->bumpiness = 0;
    features->highest_point = 0;
    features->bottom_line_coverage = 0;
    features->near_complete_lines = 0;
    features->deepest_line_gap = 0;

    int column_heights[10] = {0};

    // 计算每列高度
    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT; y++) {
            if (board[y][x] != 0) {
                column_heights[x] = HEIGHT - y;
                break;
            }
        }
    }

    // 计算总高度
    for (int x = 0; x < WIDTH; x++) {
        features->aggregate_height += column_heights[x];
    }

    // 计算完整行数和接近完成的行数
    for (int y = 0; y < HEIGHT; y++) {
        int full = 1;
        int filled = 0;
        for (int x = 0; x < WIDTH; x++) {
            if (board[y][x] == 0) {
                full = 0;
            } else {
                filled++;
            }
        }
        if (full) features->complete_lines++;
        if (filled >= 8) features->near_complete_lines++;  // 已填8-9格的行
    }

    // 计算空洞数量
    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT; y++) {
            if (board[y][x] == 0 && y < HEIGHT - column_heights[x]) {
                features->holes++;
            }
        }
    }

    // 计算不平整度
    for (int x = 0; x < WIDTH - 1; x++) {
        features->bumpiness += abs(column_heights[x] - column_heights[x + 1]);
    }

    // 计算最高点
    for (int x = 0; x < WIDTH; x++) {
        if (column_heights[x] > features->highest_point) {
            features->highest_point = column_heights[x];
        }
    }

    // 计算底层覆盖率
    features->bottom_line_coverage = calculate_bottom_line_coverage(board);

    // 计算最深的连续空缺（用于判断是否容易消除）
    int max_consecutive_empty = 0;
    for (int y = 0; y < HEIGHT; y++) {
        int consecutive_empty = 0;
        for (int x = 0; x < WIDTH; x++) {
            if (board[y][x] == 0) {
                consecutive_empty++;
            }
        }
        if (consecutive_empty > max_consecutive_empty) {
            max_consecutive_empty = consecutive_empty;
        }
    }
    features->deepest_line_gap = max_consecutive_empty;
}

// 计算底层覆盖率（返回0-10之间的数值）
int calculate_bottom_line_coverage(int board[20][10]) {
    int coverage = 0;
    for (int x = 0; x < WIDTH; x++) {
        if (board[HEIGHT - 1][x] != 0) {
            coverage++;
        }
    }
    return coverage;
}

// 将特征离散化为状态索引
int get_feature_based_state_index(int current_shape, int next_shape,
                                   int height_level, int holes_level,
                                   int bumpiness_level) {
    // 状态索引计算公式：
    // state_idx = (当前方块 * 7 + 下一个方块) * (高度等级 * 空洞等级 * 不平整度等级) + ...
    //           = (c * 7 + n) * (5 * 4 * 5) + (h * 4 * 5) + (ho * 5) + b
    //           = (c * 7 + n) * 100 + h * 20 + ho * 5 + b
    int shape_state = current_shape * 7 + (next_shape % 7);
    int feature_state = height_level * 20 + holes_level * 5 + bumpiness_level;

    return shape_state * 100 + feature_state;
}

// 获取特征的离散化等级
void discretize_features(const GameStateFeatures* features,
                         int* height_level, int* holes_level,
                         int* bumpiness_level) {
    // 高度离散化（5个等级）
    if (features->aggregate_height <= 3) {
        *height_level = 0;
    } else if (features->aggregate_height <= 7) {
        *height_level = 1;
    } else if (features->aggregate_height <= 11) {
        *height_level = 2;
    } else if (features->aggregate_height <= 15) {
        *height_level = 3;
    } else {
        *height_level = 4;
    }

    // 空洞离散化（4个等级）
    if (features->holes == 0) {
        *holes_level = 0;
    } else if (features->holes <= 3) {
        *holes_level = 1;
    } else if (features->holes <= 6) {
        *holes_level = 2;
    } else {
        *holes_level = 3;
    }

    // 不平整度离散化（5个等级）
    if (features->bumpiness <= 3) {
        *bumpiness_level = 0;
    } else if (features->bumpiness <= 7) {
        *bumpiness_level = 1;
    } else if (features->bumpiness <= 11) {
        *bumpiness_level = 2;
    } else if (features->bumpiness <= 15) {
        *bumpiness_level = 3;
    } else {
        *bumpiness_level = 4;
    }
}

// 计算状态奖励
double calculate_reward(const GameStateFeatures* before, const GameStateFeatures* after, int lines_cleared) {
    double reward = 0.0;

    // 消除行数的奖励（最重要）
    if (lines_cleared == 1) reward += 100.0;
    else if (lines_cleared == 2) reward += 300.0;
    else if (lines_cleared == 3) reward += 500.0;
    else if (lines_cleared == 4) reward += 1000.0;  // Tetris超大奖励

    // 高度变化的惩罚（大幅增加）
    reward -= (after->aggregate_height - before->aggregate_height) * 3.0;

    // 绝对高度惩罚（堆叠越高，惩罚越大）
    if (after->highest_point > 15) {
        reward -= (after->highest_point - 15) * 10.0;  // 超过15行每行扣10分
    }
    if (after->highest_point > 18) {
        reward -= 50.0;  // 接近顶部的额外惩罚
    }

    // 空洞变化的惩罚（空洞是最糟糕的）
    reward -= (after->holes - before->holes) * 15.0;

    // 绝对空洞数惩罚
    reward -= after->holes * 5.0;  // 每个空洞扣5分

    // 不平整度变化的惩罚
    reward -= (after->bumpiness - before->bumpiness) * 2.0;

    // 最高点变化的惩罚（重点）
    reward -= (after->highest_point - before->highest_point) * 5.0;

    // 底层覆盖率提升的奖励
    reward += (after->bottom_line_coverage - before->bottom_line_coverage) * 5.0;

    // 完成底层铺满（覆盖率=10）的大幅奖励
    if (after->bottom_line_coverage == 10 && before->bottom_line_coverage < 10) {
        reward += 50.0;
    }

    // 【新增】奖励接近完成的行数（鼓励补全）
    if (after->near_complete_lines > before->near_complete_lines) {
        reward += (after->near_complete_lines - before->near_complete_lines) * 30.0;
    }

    // 【新增】惩罚增加连续空缺（不利于消除）
    if (after->deepest_line_gap > before->deepest_line_gap) {
        reward -= (after->deepest_line_gap - before->deepest_line_gap) * 10.0;
    }

    // 【新增】奖励减少连续空缺
    if (after->deepest_line_gap < before->deepest_line_gap) {
        reward += (before->deepest_line_gap - after->deepest_line_gap) * 15.0;
    }

    // 额外奖励：消除行且保持低高度
    if (lines_cleared > 0 && after->highest_point < 10) {
        reward += lines_cleared * 50.0;  // 消除行且高度控制好
    }

    // 额外惩罚：没有消除行但堆叠变高
    if (lines_cleared == 0 && after->highest_point > before->highest_point) {
        reward -= 20.0;  // 纯堆叠，无消除，大惩罚
    }

    return reward;
}

// ε-贪心策略选择动作（考虑边界限制）
int select_action_with_validation(QLearningAgent* agent, int state_idx, int current_shape, int board[20][10]) {
    // 探索：随机选择有效动作
    double r = (double)rand() / RAND_MAX;
    if (r < agent->exploration_rate) {
        // 随机选择旋转
        int rot = rand() % 4;
        // 获取有效位置范围
        int min_pos, max_pos;
        get_valid_positions(current_shape, rot, &min_pos, &max_pos);
        // 随机选择有效位置
        int pos = min_pos + rand() % (max_pos - min_pos + 1);
        // 转换为动作索引
        return rot * 10 + pos;
    }

    // 利用：选择最大 Q 值的有效动作
    int best_action = -1;
    double best_q = -1e9;

    for (int rot = 0; rot < 4; rot++) {
        int min_pos, max_pos;
        get_valid_positions(current_shape, rot, &min_pos, &max_pos);

        for (int pos = min_pos; pos <= max_pos; pos++) {
            int action = rot * 10 + pos;
            int q_idx = state_idx * 40 + action;

            // 只考虑有效的动作（Q值已初始化）
            if (agent->q_values[q_idx] > best_q) {
                best_q = agent->q_values[q_idx];
                best_action = action;
            }
        }
    }

    // 如果没有找到有效动作，返回默认动作
    if (best_action < 0) {
        best_action = 0;
    }

    return best_action;
}

// ε-贪心策略选择动作（原始版本，不考虑边界）
int select_action_epsilon_greedy(QLearningAgent* agent, int state_idx) {
    // 探索：随机选择
    double r = (double)rand() / RAND_MAX;
    if (r < agent->exploration_rate) {
        return rand() % 40;  // 4种旋转 * 10个位置 = 40种动作
    }

    // 利用：选择最大 Q 值的动作
    int best_action = 0;
    double best_q = agent->q_values[state_idx * 40];

    for (int action = 1; action < 40; action++) {
        int q_idx = state_idx * 40 + action;
        if (agent->q_values[q_idx] > best_q) {
            best_q = agent->q_values[q_idx];
            best_action = action;
        }
    }

    return best_action;
}

// 训练 AI：更新 Q 值
void ai_train(QLearningAgent* agent, int state_idx, int action, int next_state_idx, double reward) {
    int q_idx = state_idx * 40 + action;

    // 边界检查
    if (q_idx >= Q_TABLE_SIZE || next_state_idx * 40 >= Q_TABLE_SIZE) {
        return;
    }

    // 找到下一个状态的最大 Q 值
    double max_next_q = agent->q_values[next_state_idx * 40];
    for (int a = 1; a < 40; a++) {
        int idx = next_state_idx * 40 + a;
        if (idx < Q_TABLE_SIZE && agent->q_values[idx] > max_next_q) {
            max_next_q = agent->q_values[idx];
        }
    }

    // 限制max_next_q的范围，防止数值爆炸
    if (max_next_q > 10000.0) max_next_q = 10000.0;
    if (max_next_q < -10000.0) max_next_q = -10000.0;

    // Q-Learning 更新公式
    double new_q = agent->q_values[q_idx] + agent->learning_rate *
        (reward + agent->discount_factor * max_next_q - agent->q_values[q_idx]);

    // 限制Q值范围，防止数值爆炸
    if (new_q > 10000.0) new_q = 10000.0;
    if (new_q < -10000.0) new_q = -10000.0;

    agent->q_values[q_idx] = new_q;
}

// 获取方块的有效位置范围
void get_valid_positions(int shape, int rotation, int* min_pos, int* max_pos) {
    int temp_matrix[4][4];
    get_rotated_shape(shape, rotation, temp_matrix);

    // 找出方块的实际边界
    int leftmost = 4, rightmost = -1;
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            if (temp_matrix[j][i]) {
                if (j < leftmost) leftmost = j;
                if (j > rightmost) rightmost = j;
            }
        }
    }

    // 方块宽度
    int block_width = rightmost - leftmost + 1;

    // 有效位置范围：0 到 (WIDTH - block_width)
    *min_pos = 0;
    *max_pos = WIDTH - block_width;
}

// 检查某个旋转和位置组合是否有效（边界检测）
int is_valid_action(int board[20][10], int shape, int rotation, int position) {
    int temp_matrix[4][4];
    get_rotated_shape(shape, rotation, temp_matrix);

    // 检查初始放置位置是否在边界内且不碰撞
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            if (temp_matrix[j][i]) {
                int new_x = position + j;
                int new_y = i;  // 从顶部开始

                // 边界检查
                if (new_x < 0 || new_x >= WIDTH || new_y >= HEIGHT) {
                    return 0;
                }

                // 碰撞检查
                if (new_y >= 0 && board[new_y][new_x] > 0) {
                    return 0;
                }
            }
        }
    }

    return 1;
}

// 模拟放置方块
void simulate_placement(int board[20][10], int temp_board[20][10], int shape, int rotation, int position) {
    // 复制当前棋盘
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            temp_board[y][x] = board[y][x];
        }
    }

    // 模拟方块下落（简化版，只考虑最终落点）
    // 这里需要与主程序的形状定义和旋转逻辑一致
    // 实际应用中需要完整实现
}

// 简单启发式评估（用于快速决策）
AIDecision heuristic_make_decision(int board[20][10], int current_shape, int next_shape) {
    AIDecision decision;
    decision.rotation = 0;
    decision.position = 0;
    decision.confidence = 0.0;

    double best_score = -1e9;
    int best_rotation = 0;
    int best_position = 0;

    // 遍历所有旋转
    for (int rot = 0; rot < 4; rot++) {
        // 获取当前旋转的有效位置范围
        int min_pos, max_pos;
        get_valid_positions(current_shape, rot, &min_pos, &max_pos);

        // 只遍历有效位置
        for (int pos = min_pos; pos <= max_pos; pos++) {
            // 模拟从顶部放置，找到底部落点
            int drop_y = 0;
            int can_place = 1;

            // 检查初始位置是否合法
            int valid_start = 1;
            int temp_matrix[4][4];
            get_rotated_shape(current_shape, rot, temp_matrix);
            for (int i = 0; i < 4 && valid_start; i++) {
                for (int j = 0; j < 4 && valid_start; j++) {
                    if (temp_matrix[j][i]) {
                        int new_x = pos + j;
                        int new_y = 0 + i;
                        if (new_x < 0 || new_x >= WIDTH || new_y >= HEIGHT) {
                            valid_start = 0;
                        } else if (new_y >= 0 && board[new_y][new_x] > 0) {
                            valid_start = 0;
                        }
                    }
                }
            }

            if (!valid_start) {
                can_place = 0;
            } else {
                // 找到落点：从顶部逐步下落直到碰撞
                drop_y = 0;
                while (drop_y < HEIGHT) {
                    int collision = 0;
                    for (int i = 0; i < 4 && !collision; i++) {
                        for (int j = 0; j < 4 && !collision; j++) {
                            if (temp_matrix[j][i]) {
                                int new_x = pos + j;
                                int new_y = drop_y + i + 1;
                                if (new_x < 0 || new_x >= WIDTH || new_y >= HEIGHT) {
                                    collision = 1;
                                } else if (new_y >= 0 && board[new_y][new_x] > 0) {
                                    collision = 1;
                                }
                            }
                        }
                    }
                    if (collision) break;
                    drop_y++;
                }
            }

            // 评估该位置
            if (can_place) {
                // 模拟放置后的棋盘
                int temp_board[20][10] = {0};
                for (int y = 0; y < 20; y++) {
                    for (int x = 0; x < 10; x++) {
                        temp_board[y][x] = board[y][x];
                    }
                }

                // 放置方块到模拟棋盘
                int blocks_placed = 0;
                for (int i = 0; i < 4; i++) {
                    for (int j = 0; j < 4; j++) {
                        if (temp_matrix[j][i]) {
                            int new_x = pos + j;
                            int new_y = drop_y + i;
                            if (new_y >= 0 && new_y < HEIGHT && new_x >= 0 && new_x < WIDTH) {
                                temp_board[new_y][new_x] = 1;
                                blocks_placed++;
                            }
                        }
                    }
                }

                // 模拟消除完整行
                int lines_cleared = 0;
                for (int y = 0; y < HEIGHT; y++) {
                    int full = 1;
                    for (int x = 0; x < WIDTH; x++) {
                        if (temp_board[y][x] == 0) {
                            full = 0;
                            break;
                        }
                    }
                    if (full) {
                        lines_cleared++;
                        for (int yy = y; yy > 0; yy--) {
                            for (int x = 0; x < WIDTH; x++) {
                                temp_board[yy][x] = temp_board[yy-1][x];
                            }
                        }
                        for (int x = 0; x < WIDTH; x++) {
                            temp_board[0][x] = 0;
                        }
                    }
                }

                // 计算放置后的特征
                GameStateFeatures features;
                extract_game_features(temp_board, &features);

                // 启发式评分（目标：尽量占据最少方块，即消除更多行，降低高度，减少空洞）
                double score = 0.0;

                // 消除行数奖励（主要目标，大幅提升）
                score += lines_cleared * 200.0;  // 从100提升到200

                // 占据方块数惩罚（让AI倾向于用最少方块消除）
                // 但这已经被lines_cleared涵盖，因为消除会减少方块数
                score -= blocks_placed * 0.5;

                // 高度惩罚（鼓励保持低高度）
                score -= features.aggregate_height * 3.0;

                // 最高点惩罚（避免堆太高）
                score -= features.highest_point * 5.0;

                // 空洞惩罚（避免产生空洞）
                score -= features.holes * 4.0;

                // 不平整度惩罚（保持表面平整）
                score -= features.bumpiness * 1.0;

                // 底层覆盖率奖励（鼓励AI铺好底层）
                score += features.bottom_line_coverage * 8.0;

                // 游戏初期额外奖励底层覆盖率（当总方块数少于50时）
                int total_blocks = 0;
                for (int y = 0; y < HEIGHT; y++) {
                    for (int x = 0; x < WIDTH; x++) {
                        if (temp_board[y][x] != 0) total_blocks++;
                    }
                }
                if (total_blocks < 50) {
                    score += features.bottom_line_coverage * 5.0;  // 额外奖励
                }

                // 无消除的额外惩罚（防止只堆叠不消除）
                if (lines_cleared == 0) {
                    score -= 20.0;  // 强烈惩罚无消除的行为
                }

                // 前瞻：评估下一个方块的可放置性
                double next_best_score = -1e9;
                for (int next_rot = 0; next_rot < 4; next_rot++) {
                    for (int next_pos = 0; next_pos < WIDTH; next_pos++) {
                        // 检查下一个方块是否能放置
                        int next_valid_start = 1;
                        int next_drop_y = 0;
                        int next_temp_matrix[4][4];
                        get_rotated_shape(next_shape, next_rot, next_temp_matrix);
                        for (int i = 0; i < 4 && next_valid_start; i++) {
                            for (int j = 0; j < 4 && next_valid_start; j++) {
                                if (next_temp_matrix[j][i]) {
                                    int new_x = next_pos + j;
                                    int new_y = 0 + i;
                                    if (new_x < 0 || new_x >= WIDTH || new_y >= HEIGHT) {
                                        next_valid_start = 0;
                                    } else if (new_y >= 0 && temp_board[new_y][new_x] > 0) {
                                        next_valid_start = 0;
                                    }
                                }
                            }
                        }

                        if (next_valid_start) {
                            // 模拟下一个方块的落点
                            next_drop_y = 0;
                            while (next_drop_y < HEIGHT) {
                                int collision = 0;
                                for (int i = 0; i < 4 && !collision; i++) {
                                    for (int j = 0; j < 4 && !collision; j++) {
                                        if (next_temp_matrix[j][i]) {
                                            int new_x = next_pos + j;
                                            int new_y = next_drop_y + i + 1;
                                            if (new_x < 0 || new_x >= WIDTH || new_y >= HEIGHT) {
                                                collision = 1;
                                            } else if (new_y >= 0 && temp_board[new_y][new_x] > 0) {
                                                collision = 1;
                                            }
                                        }
                                    }
                                }
                                if (collision) break;
                                next_drop_y++;
                            }

                            // 评估放置后的棋盘
                            int next_temp_board[20][10] = {0};
                            for (int y = 0; y < 20; y++) {
                                for (int x = 0; x < 10; x++) {
                                    next_temp_board[y][x] = temp_board[y][x];
                                }
                            }

                            int next_blocks = 0;
                            for (int i = 0; i < 4; i++) {
                                for (int j = 0; j < 4; j++) {
                                    if (next_temp_matrix[j][i]) {
                                        int new_x = next_pos + j;
                                        int new_y = next_drop_y + i;
                                        if (new_y >= 0 && new_y < HEIGHT && new_x >= 0 && new_x < WIDTH) {
                                            next_temp_board[new_y][new_x] = 1;
                                            next_blocks++;
                                        }
                                    }
                                }
                            }

                            GameStateFeatures next_features;
                            extract_game_features(next_temp_board, &next_features);

                            double next_score = next_features.complete_lines * 100.0
                                             - next_blocks * 0.5
                                             - next_features.aggregate_height * 3.0
                                             - next_features.highest_point * 5.0
                                             - next_features.holes * 4.0;

                            if (next_score > next_best_score) {
                                next_best_score = next_score;
                            }
                        }
                    }
                }

                // 结合当前和未来得分（当前70%，未来30%）
                score = score * 0.7 + next_best_score * 0.3;

                if (score > best_score) {
                    best_score = score;
                    best_rotation = rot;
                    best_position = pos;
                }
            }
        }
    }

    decision.rotation = best_rotation;
    decision.position = best_position;
    decision.confidence = 1.0;

    return decision;
}

// AI 决策：选择最佳动作（基于特征的状态空间）
AIDecision ai_make_decision(QLearningAgent* agent, int current_shape, int next_shape, int board[20][10]) {
    // 新策略：基于特征的状态空间
    // - 状态 = (当前方块, 下一个方块, 高度等级, 空洞等级, 不平整度等级)
    // - 共有 7 * 7 * 5 * 4 * 5 = 4900 种状态
    // - 每种状态有 40 个动作（4旋转 * 10位置）
    // - Q表总大小：4900 * 40 = 196000

    AIDecision decision;
    decision.rotation = 0;
    decision.position = 0;
    decision.confidence = 0.0;

    // 提取当前棋盘特征
    GameStateFeatures features;
    extract_game_features(board, &features);

    // 离散化特征
    int height_level, holes_level, bumpiness_level;
    discretize_features(&features, &height_level, &holes_level, &bumpiness_level);

    // 计算状态索引
    int state_idx = get_feature_based_state_index(current_shape, next_shape,
                                                   height_level, holes_level, bumpiness_level);

    // ε-贪心策略
    double r = (double)rand() / RAND_MAX;
    if (r < agent->exploration_rate) {
        // 探索：随机选择有效动作，但偏向低高度位置
        int rot = rand() % 4;
        int min_pos, max_pos;
        get_valid_positions(current_shape, rot, &min_pos, &max_pos);

        // 计算所有有效位置的落点高度
        int num_positions = max_pos - min_pos + 1;
        double weights[10];  // 最多10个位置
        double total_weight = 0.0;

        for (int pos = min_pos; pos <= max_pos; pos++) {
            int drop_height = calculate_drop_height(board, current_shape, rot, pos);
            // 权重与高度成反比，高度越低权重越大
            // 使用指数函数增强低高度位置的权重
            weights[pos - min_pos] = exp(-drop_height * 0.3);
            total_weight += weights[pos - min_pos];
        }

        // 根据权重随机选择位置
        double rand_val = (double)rand() / RAND_MAX * total_weight;
        int selected_pos = min_pos;
        double cumulative_weight = 0.0;
        for (int pos = min_pos; pos <= max_pos; pos++) {
            cumulative_weight += weights[pos - min_pos];
            if (rand_val <= cumulative_weight) {
                selected_pos = pos;
                break;
            }
        }

        decision.rotation = rot;
        decision.position = selected_pos;
        decision.confidence = 0.3;
        return decision;
    }

    // 利用：选择 Q 值最大的有效动作，同时考虑落点高度
    double best_q = -1e9;
    int best_action = -1;
    int lowest_height = 100;  // 记录最低的落点高度

    for (int rot = 0; rot < 4; rot++) {
        int min_pos, max_pos;
        get_valid_positions(current_shape, rot, &min_pos, &max_pos);

        for (int pos = min_pos; pos <= max_pos; pos++) {
            int action = rot * 10 + pos;
            int q_idx = state_idx * 40 + action;

            if (q_idx < Q_TABLE_SIZE) {
                double q_value = agent->q_values[q_idx];

                // 计算落点高度
                int drop_height = calculate_drop_height(board, current_shape, rot, pos);

                // 调整Q值：给低高度位置加成
                // 高度越低，加成越大
                double height_bonus = (20 - drop_height) * 5.0;  // 每低1行加5分
                double adjusted_q = q_value + height_bonus;

                if (adjusted_q > best_q) {
                    best_q = adjusted_q;
                    best_action = action;
                    lowest_height = drop_height;
                }
            }
        }
    }

    if (best_action >= 0) {
        decision.rotation = best_action / 10;
        decision.position = best_action % 10;
        decision.confidence = 0.8;
    } else {
        // 如果没有找到有效动作，使用启发式方法
        decision = heuristic_make_decision(board, current_shape, next_shape);
    }

    return decision;
}
