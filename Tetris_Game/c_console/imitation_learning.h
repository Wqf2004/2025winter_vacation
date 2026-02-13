/*
 * 俄罗斯方块 AI - 模仿学习模块
 * 从人类玩家的游戏记录中学习策略
 */

#ifndef IMITATION_LEARNING_H
#define IMITATION_LEARNING_H

#include "tetris_ai.h"

// 游戏记录结构：记录每一步的决策和结果
typedef struct {
    int current_shape;      // 当前方块类型
    int next_shape;        // 下一个方块类型
    int rotation;          // 玩家选择的旋转
    int position;          // 玩家选择的位置
    int height_level;      // 棋盘高度等级（离散化）
    int holes_level;       // 棋盘空洞等级（离散化）
    int bumpiness_level;   // 棋盘不平整度等级（离散化）
    int lines_cleared;     // 这一步消除的行数
    int score_before;      // 这一步前的得分
    int score_after;       // 这一步后的得分
    int height_after;      // 放置后的棋盘高度
    int holes_after;       // 放置后的空洞数
    int bumpiness_after;   // 放置后的不平整度
} GameRecord;

// 游戏记录集合
#define MAX_RECORDS 10000
typedef struct {
    GameRecord records[MAX_RECORDS];
    int count;
} GameRecords;

// 从人类玩家的游戏记录初始化Q表
void initialize_q_from_records(QLearningAgent* agent, GameRecords* records);

// 评估玩家选择的动作的得分（用于学习策略）
double evaluate_player_action(const GameRecord* rec);

// 保存游戏记录到文件
void save_records_to_file(GameRecords* records, const char* filename);

// 从文件加载游戏记录
void load_records_from_file(GameRecords* records, const char* filename);

// 添加一条游戏记录
void add_record(GameRecords* records, GameRecord record);

// 清空游戏记录
void clear_records(GameRecords* records);

#endif // IMITATION_LEARNING_H
