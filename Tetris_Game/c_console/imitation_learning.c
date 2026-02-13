/*
 * 俄罗斯方块 AI - 模仿学习实现
 */

#include "imitation_learning.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 从人类玩家的游戏记录初始化Q表
void initialize_q_from_records(QLearningAgent* agent, GameRecords* records) {
    printf("\n从 %d 条人类玩家记录中学习策略...\n", records->count);

    // 统计每个状态下各个动作的平均奖励（不使用频率加权）
    int* action_counts = (int*)calloc(Q_TABLE_SIZE, sizeof(int));
    double* action_rewards = (double*)calloc(Q_TABLE_SIZE, sizeof(double));

    // 统计每个状态下所有动作的平均奖励（用于归一化）
    double* state_avg_rewards = (double*)calloc(Q_TABLE_SIZE / 40, sizeof(double));
    int* state_action_counts = (int*)calloc(Q_TABLE_SIZE / 40, sizeof(int));

    // 第一遍：统计玩家选择
    for (int i = 0; i < records->count; i++) {
        GameRecord* rec = &records->records[i];

        // 计算状态索引
        int state_idx = get_feature_based_state_index(
            rec->current_shape,
            rec->next_shape,
            rec->height_level,
            rec->holes_level,
            rec->bumpiness_level
        );

        // 计算动作索引
        int action = rec->rotation * 10 + rec->position;

        // 计算Q表索引
        int q_idx = state_idx * 40 + action;

        // 边界检查
        if (q_idx >= Q_TABLE_SIZE) {
            continue;
        }

        // 统计该动作被选择的次数
        action_counts[q_idx]++;

        // 计算该动作的得分（基于玩家的实际表现）
        double reward = evaluate_player_action(rec);

        // 累积奖励
        action_rewards[q_idx] += reward;

        // 统计该状态下的所有动作
        state_action_counts[state_idx]++;
        state_avg_rewards[state_idx] += reward;
    }

    // 第二遍：根据平均奖励设置Q值（去除频率偏见）
    for (int i = 0; i < Q_TABLE_SIZE; i++) {
        if (action_counts[i] > 0) {
            // 使用平均奖励，不添加频率奖励
            double avg_reward = action_rewards[i] / action_counts[i];

            // 获取该状态的平均奖励（用于归一化）
            int state_idx = i / 40;
            if (state_action_counts[state_idx] > 0) {
                double state_avg = state_avg_rewards[state_idx] / state_action_counts[state_idx];

                // 相对于该状态下其他动作的优势
                // 如果这个动作比该状态的平均水平好，给予更高的Q值
                if (avg_reward > state_avg) {
                    agent->q_values[i] = avg_reward * 1.5;  // 好动作强化
                } else if (avg_reward < state_avg - 50) {
                    agent->q_values[i] = avg_reward * 0.8;  // 差动作弱化
                } else {
                    agent->q_values[i] = avg_reward;  // 一般动作
                }
            } else {
                agent->q_values[i] = avg_reward;
            }
        }
    }

    // 统计学习结果
    int learned_states = 0;
    for (int i = 0; i < Q_TABLE_SIZE / 40; i++) {
        if (state_action_counts[i] > 0) {
            learned_states++;
        }
    }

    printf("策略学习完成！\n");
    printf("- 共分析了 %d 条玩家记录\n", records->count);
    printf("- 学习了 %d 个状态\n", learned_states);
    printf("- 平均每个状态有 %.1f 个动作样本\n", (double)records->count / learned_states);

    free(action_counts);
    free(action_rewards);
    free(state_avg_rewards);
    free(state_action_counts);
}

// 评估玩家选择的动作的得分（基于实际游戏结果）
double evaluate_player_action(const GameRecord* rec) {
    double action_score = 0.0;

    // 1. 核心奖励：实际得分增量（真实反映玩家决策效果）
    int score_gain = rec->score_after - rec->score_before;
    action_score += score_gain * 1.0;  // 每得1分 = 1.0奖励

    // 2. 消除行的奖励（放大权重）
    if (rec->lines_cleared == 1) action_score += 100.0;
    else if (rec->lines_cleared == 2) action_score += 300.0;
    else if (rec->lines_cleared == 3) action_score += 500.0;
    else if (rec->lines_cleared == 4) action_score += 1000.0;  // Tetris

    // 3. 放置后的棋盘质量（使用实际值而非离散等级）
    // 越低越好
    action_score -= rec->height_after * 5.0;  // 每高1行扣5分
    // 越少越好
    action_score -= rec->holes_after * 20.0;  // 每个空洞扣20分
    // 越平滑越好
    action_score -= rec->bumpiness_after * 10.0;  // 每单位不平整扣10分

    // 4. 关键：惩罚"无消除但堆叠高"的行为
    if (rec->lines_cleared == 0) {
        // 没有消除行，且堆叠较高，这是不良决策
        if (rec->height_after > 12) {
            action_score -= 150.0;  // 大惩罚
        } else if (rec->height_after > 8) {
            action_score -= 80.0;  // 中等惩罚
        }
        // 特别是竖直放置I型却没有消除行
        if (rec->current_shape == 0 && rec->rotation == 0 && rec->height_after > 10) {
            action_score -= 200.0;  // 竖I型堆叠，极差决策
        }
    }

    // 5. 特殊情况奖励
    // 消除多行且高度控制好
    if (rec->lines_cleared >= 2 && rec->height_after <= 10) {
        action_score += 200.0;
    }
    // Tetris且高度控制非常好
    if (rec->lines_cleared == 4 && rec->height_after <= 8) {
        action_score += 500.0;
    }
    // 消除行且高度降低（好决策）
    if (rec->lines_cleared >= 1 && rec->height_after <= 8) {
        action_score += 100.0;
    }

    // 6. 避免危险操作
    // 如果放置后高度超过15，说明危险
    if (rec->height_after > 15) {
        action_score -= 300.0;
    }
    // 如果放置后空洞超过3个，说明危险
    if (rec->holes_after > 3) {
        action_score -= 200.0;
    }

    return action_score;
}

// 保存游戏记录到文件
void save_records_to_file(GameRecords* records, const char* filename) {
    FILE* fp = fopen(filename, "w");
    if (!fp) {
        printf("无法打开文件 %s 进行写入\n", filename);
        return;
    }

    // 文件头
    fprintf(fp, "# 俄罗斯方块游戏记录\n");
    fprintf(fp, "# 格式: current_shape next_shape rotation position height_level holes_level bumpiness_level lines_cleared score_before score_after height_after holes_after bumpiness_after\n");
    fprintf(fp, "# 记录数: %d\n", records->count);
    fprintf(fp, "\n");

    // 写入记录
    for (int i = 0; i < records->count; i++) {
        GameRecord* rec = &records->records[i];
        fprintf(fp, "%d %d %d %d %d %d %d %d %d %d %d %d %d\n",
            rec->current_shape,
            rec->next_shape,
            rec->rotation,
            rec->position,
            rec->height_level,
            rec->holes_level,
            rec->bumpiness_level,
            rec->lines_cleared,
            rec->score_before,
            rec->score_after,
            rec->height_after,
            rec->holes_after,
            rec->bumpiness_after
        );
    }

    fclose(fp);
    printf("已保存 %d 条游戏记录到 %s\n", records->count, filename);
}

// 从文件加载游戏记录
void load_records_from_file(GameRecords* records, const char* filename) {
    FILE* fp = fopen(filename, "r");
    if (!fp) {
        printf("文件 %s 不存在或无法打开\n", filename);
        records->count = 0;
        return;
    }

    records->count = 0;
    char line[512];

    // 跳过注释行
    while (fgets(line, sizeof(line), fp)) {
        if (line[0] == '#') continue;
        if (line[0] == '\n' || line[0] == '\r') continue;
        break;
    }

    // 读取记录
    while (records->count < MAX_RECORDS && fgets(line, sizeof(line), fp)) {
        // 跳过空行和注释
        if (line[0] == '#') continue;
        if (line[0] == '\n' || line[0] == '\r') continue;

        GameRecord* rec = &records->records[records->count];
        int parsed = sscanf(line, "%d %d %d %d %d %d %d %d %d %d %d %d %d",
            &rec->current_shape,
            &rec->next_shape,
            &rec->rotation,
            &rec->position,
            &rec->height_level,
            &rec->holes_level,
            &rec->bumpiness_level,
            &rec->lines_cleared,
            &rec->score_before,
            &rec->score_after,
            &rec->height_after,
            &rec->holes_after,
            &rec->bumpiness_after
        );

        // 新格式：13个字段
        if (parsed == 13) {
            records->count++;
        }
        // 旧格式：8个字段（兼容旧记录）
        else {
            int parsed_old = sscanf(line, "%d %d %d %d %d %d %d %d",
                &rec->current_shape,
                &rec->next_shape,
                &rec->rotation,
                &rec->position,
                &rec->height_level,
                &rec->holes_level,
                &rec->bumpiness_level,
                &rec->lines_cleared
            );

            if (parsed_old == 8) {
                // 初始化新增字段为0
                rec->score_before = 0;
                rec->score_after = rec->lines_cleared * 100;  // 估算
                rec->height_after = 0;
                rec->holes_after = 0;
                rec->bumpiness_after = 0;
                records->count++;
            }
        }
    }

    fclose(fp);
    printf("已从 %s 加载 %d 条游戏记录\n", filename, records->count);
}

// 添加一条游戏记录
void add_record(GameRecords* records, GameRecord record) {
    if (records->count < MAX_RECORDS) {
        records->records[records->count] = record;
        records->count++;
    }
}

// 清空游戏记录
void clear_records(GameRecords* records) {
    records->count = 0;
}
