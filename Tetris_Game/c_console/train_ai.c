/*
 * 俄罗斯方块 AI 训练程序
 * 通过自我对弈训练 Q-Learning 模型
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "tetris_ai.h"

#define WIDTH 10
#define HEIGHT 20
#define MAX_EPISODES 10000

// 方块形状定义
int SHAPES[7][4][4] = {
    {{0,1,0,0}, {1,1,1,0}, {0,0,0,0}, {0,0,0,0}},  // I
    {{2,0,0}, {2,2,2}},                              // J
    {{0,0,3}, {3,3,3}},                              // L
    {{4,4}, {4,4}},                                  // O
    {{0,5,5}, {5,5,0}},                              // S
    {{0,6,0}, {6,6,6}},                              // T
    {{7,7,0}, {0,7,7}}                               // Z
};

// 旋转矩阵
void rotate_matrix(int matrix[4][4]) {
    int new_matrix[4][4] = {0};
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            new_matrix[j][3 - i] = matrix[i][j];
        }
    }
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            matrix[i][j] = new_matrix[i][j];
        }
    }
}

// 获取旋转后的形状
void get_rotated_shape(int shape_type, int rotation, int result[4][4]) {
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            result[i][j] = SHAPES[shape_type][i][j];
        }
    }
    for (int r = 0; r < rotation; r++) {
        rotate_matrix(result);
    }
}

// 全局变量（简化版训练环境）
int board[HEIGHT][WIDTH] = {0};
int score = 0;
int game_over = 0;

// 初始化训练环境
void init_training_env() {
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            board[y][x] = 0;
        }
    }
    score = 0;
    game_over = 0;
}

// 训练一局游戏
void train_episode(QLearningAgent* agent, int episode_num) {
    init_training_env();

    // 模拟游戏（简化版）
    int steps = 0;
    double total_reward = 0.0;

    while (!game_over && steps < 1000) {
        // 获取当前状态
        GameStateFeatures current_features;
        extract_game_features(board, &current_features);
        int state_idx = current_features.complete_lines * 10 + current_features.aggregate_height % 10;
        if (state_idx >= Q_TABLE_SIZE) state_idx = 0;

        // AI 选择动作
        int next_shape = rand() % 7;  // 随机下一个方块
        AIDecision decision = ai_make_decision(agent, 0, next_shape, board);

        // 执行动作（简化版：随机模拟）
        int action = decision.rotation * 10 + decision.position;
        int next_state_idx = (state_idx + 1) % Q_TABLE_SIZE;

        // 计算奖励（简化版）
        double reward = 0.0;
        if (rand() % 10 == 0) {
            reward += 10.0;  // 随机消除行
        } else {
            reward -= 1.0;  // 普通惩罚
        }

        if (steps > 500) {
            game_over = 1;
            reward -= 100.0;  // 游戏结束惩罚
        }

        total_reward += reward;

        // 更新 Q 值
        ai_train(agent, state_idx, action % 40, next_state_idx, reward);

        steps++;
    }

    // 随着训练进行，降低探索率
    if (episode_num % 100 == 0 && agent->exploration_rate > 0.01) {
        agent->exploration_rate *= 0.99;
    }

    // 每100回合输出进度
    if (episode_num % 100 == 0) {
        printf("回合 %d: 总奖励 %.2f, 探索率 %.3f\n",
               episode_num, total_reward, agent->exploration_rate);
    }
}

// 主训练函数
void train_ai() {
    printf("========================================\n");
    printf("       俄罗斯方块 AI 训练\n");
    printf("========================================\n\n");

    srand(time(NULL));

    QLearningAgent agent;
    init_ql_agent(&agent);

    // 尝试加载已有模型
    if (load_q_table(&agent, "tetris_qtable.txt")) {
        printf("继续训练现有模型...\n\n");
    } else {
        printf("从头开始训练，正在注入启发式知识...\n\n");
        // 使用启发式知识初始化Q表
        init_q_table_with_heuristics(&agent);
        printf("启发式知识注入完成\n\n");
    }

    printf("开始训练 %d 回合...\n\n", MAX_EPISODES);

    // 训练
    for (int episode = 0; episode < MAX_EPISODES; episode++) {
        train_episode(&agent, episode);
    }

    printf("\n训练完成！\n");

    // 保存训练结果
    save_q_table(&agent, "tetris_qtable.txt");
}

int main() {
    train_ai();
    return 0;
}
