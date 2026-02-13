/*
 * 俄罗斯方块游戏 - C语言控制台版
 */

#include <stdio.h>   // 标准输入输出库，提供printf/scanf等基本I/O函数
#include <stdlib.h>  // 标准库，提供内存分配、随机数生成等系统函数
#include <time.h>    // 时间库，提供时间相关函数如time()用于随机数种子
#include <conio.h>  // 提供控制台输入输出函数，如_getch()用于非缓冲输入
#include <windows.h> // 提供Windows API函数，如控制台光标位置和颜色设置
#include <mmsystem.h> // 多媒体系统库，用于播放音频文件
#include <process.h>  // 进程控制库，用于创建线程
#include "tetris_ai.h"  // AI 助手头文件
#include "imitation_learning.h"  // 模仿学习头文件

#define WIDTH 10     // 游戏板的宽度（方块数量）
#define HEIGHT 20    // 游戏板的高度（方块数量）
#define BLOCK_SIZE 4 // 每个方块形状的矩阵大小（4x4）

// 方块形状定义（7种形状）
// 0: I形, 1: J形, 2: L形, 3: O形, 4: S形, 5: T形, 6: Z形
int shapes[7][4][4] = {
    // I形 - 4格直线
    {{0,0,0,0}, {1,1,1,1}, {0,0,0,0}, {0,0,0,0}},
    // J形 - 倒L (一横一竖，竖在右)
    {{1,1,1,0}, {0,0,1,0}, {0,0,0,0}, {0,0,0,0}},
    // L形 (一横一竖，竖在左)
    {{1,1,1,0}, {1,0,0,0}, {0,0,0,0}, {0,0,0,0}},
    // O形 - 2x2正方形
    {{1,1,0,0}, {1,1,0,0}, {0,0,0,0}, {0,0,0,0}},
    // S形
    {{0,1,1,0}, {1,1,0,0}, {0,0,0,0}, {0,0,0,0}},
    // T形
    {{0,1,0,0}, {1,1,1,0}, {0,0,0,0}, {0,0,0,0}},
    // Z形
    {{1,1,0,0}, {0,1,1,0}, {0,0,0,0}, {0,0,0,0}},
};

// 复制4x4矩阵
void copy_matrix(int dest[4][4], int src[4][4]) {
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            dest[i][j] = src[i][j];
        }
    }
}

// 将4x4矩阵顺时针旋转90度
void rotate_matrix(int matrix[4][4]) {
    int temp[4][4] = {0};
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            temp[j][3 - i] = matrix[i][j];
        }
    }
    copy_matrix(matrix, temp);
}

// 在上面函数的基础上，定义一个旋转n次的函数
void rotate_matrix_n_times(int matrix[4][4], int n) {
    // 绕谁旋转都一样
    for (int i = 0; i < n; i++) {
        rotate_matrix(matrix);
    }
}

// 获取指定方块形状的旋转矩阵（旋转n次）
void get_rotated_shape(int shape_index, int rotation_times, int result[4][4]) {
    copy_matrix(result, shapes[shape_index]);
    rotate_matrix_n_times(result, rotation_times);
}

// 方块颜色
int colors[] = {1, 2, 3, 4, 5, 6, 14};  // 蓝、绿、青、红、紫、黄、亮黄

// 游戏状态
int board[HEIGHT][WIDTH] = {0};
int current_shape;
int current_rotation;
int current_x;
int current_y;
int next_shape;
int score = 0;
int level = 1;
int lines_cleared = 0;
int game_over = 0;
int paused = 0;

// 音乐播放状态
volatile int music_playing = 1;  // 使用volatile确保多线程可见性

// AI 助手相关
QLearningAgent ai_agent;
int ai_mode = 0;  // 0: 关闭, 1: 观看模式, 2: 训练模式
int ai_auto_speed = 100;  // AI 自动下落速度(ms)
int ai_episode = 0;  // 当前训练回合数
int max_ai_episodes = 100;  // 最大训练回合数
int ai_early_exit = 0;  // 标记是否提前退出训练

// 模仿学习相关
GameRecords player_records;  // 玩家游戏记录
int record_player_moves = 1;  // 是否记录玩家操作（默认开启）

// 人类干预训练相关
int human_intervention_mode = 0;  // 是否启用人人干预训练（训练模式下按H键开启）
int human_intervention_active = 0;  // 当前是否正在进行人类干预
int debug_ai_decision = 0;  // 是否显示AI决策调试信息

// 音乐播放线程
unsigned __stdcall music_thread(void* param) {
    (void)param;  // 消除未使用参数警告
    char cmd[512];
    char status[128];
    int current_track = 0;
    const char* tracks[] = {
        "D:\\HuaweiMoveData\\Users\\20426\\Desktop\\2025winter_vacation\\Tetris_Game\\dataset\\22-sfx.mp3",
        "D:\\HuaweiMoveData\\Users\\20426\\Desktop\\2025winter_vacation\\Tetris_Game\\dataset\\34-sfx.mp3"
    };

    // 循环播放
    while (music_playing) {
        // 播放当前曲目
        sprintf(cmd, "open \"%s\" type mpegvideo alias bgm", tracks[current_track]);
        mciSendString(cmd, NULL, 0, NULL);
        mciSendString("play bgm notify", NULL, 0, NULL);

        // 等待音乐播放完毕或停止信号
        while (music_playing) {
            mciSendString("status bgm mode", status, sizeof(status), NULL);
            if (strstr(status, "stopped") != NULL || strstr(status, "idle") != NULL) {
                break;
            }
            Sleep(500);
        }

        mciSendString("close bgm", NULL, 0, NULL);

        // 切换到下一首
        current_track = (current_track + 1) % 2;
    }

    return 0;
}

// 设置控制台光标位置
void gotoxy(int x, int y) {
    COORD coord;
    coord.X = x;
    coord.Y = y;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

// 设置控制台颜色
void setcolor(int color) {
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), color);
}

// 获取最高分（函数声明）
int get_high_score();

// 初始化游戏
void init_game() {
    // 清空游戏板
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            board[y][x] = 0;
        }
    }

    score = 0;
    level = 1;
    lines_cleared = 0;
    game_over = 0;
    paused = 0;

    // 生成第一个方块
    current_shape = rand() % 7;
    current_rotation = 0;
    current_x = WIDTH / 2 - 2;
    current_y = 0;

    // 生成下一个方块
    next_shape = rand() % 7;
}

// 绘制游戏板
void draw_board() {
    // 使用光标定位代替 system("cls")，避免清屏导致输出消失
    gotoxy(0, 0);

    // 绘制边框和内容
    setcolor(7);

    // 上边框
    printf("┌");
    for (int i = 0; i < WIDTH; i++) printf("──");
    printf("┐\n");

    // 游戏区域
    for (int y = 0; y < HEIGHT; y++) {
        printf("│");
        for (int x = 0; x < WIDTH; x++) {
            if (board[y][x] > 0) {
                setcolor(board[y][x]);
                printf("██");
                setcolor(7);
            } else {
                printf("  ");
            }
        }
        printf("│\n");
    }

    // 下边框
    printf("└");
    for (int i = 0; i < WIDTH; i++) printf("──");
    printf("┘\n");

    // 绘制当前方块
    int current_matrix[4][4];
    get_rotated_shape(current_shape, current_rotation, current_matrix);
    for (int i = 0; i < BLOCK_SIZE; i++) {
        for (int j = 0; j < BLOCK_SIZE; j++) {
            if (current_matrix[i][j]) {
                int draw_x = (current_x + j) * 2 + 1;
                int draw_y = current_y + i + 1;
                if (draw_x >= 1 && draw_x < WIDTH * 2 && draw_y >= 1 && draw_y <= HEIGHT) {
                    gotoxy(draw_x, draw_y);
                    setcolor(colors[current_shape]);
                    printf("██");
                    setcolor(7);
                }
            }
        }
    }

    // 显示信息
    gotoxy(WIDTH * 2 + 3, 1);
    printf("╔════════════╗");
    gotoxy(WIDTH * 2 + 3, 2);
    printf("║ 分数: %4d ║", score);
    gotoxy(WIDTH * 2 + 3, 3);
    printf("║ 等级: %4d ║", level);
    gotoxy(WIDTH * 2 + 3, 4);
    printf("║ 行数: %4d ║", lines_cleared);
    gotoxy(WIDTH * 2 + 3, 5);
    printf("╚════════════╝");

    // 显示最高分
    int high_score = get_high_score();
    gotoxy(WIDTH * 2 + 3, 16);
    printf("╔═════════╗");
    gotoxy(WIDTH * 2 + 3, 17);
    printf("║ 最高分  ║");
    gotoxy(WIDTH * 2 + 3, 18);
    printf("╠═════════╣");
    gotoxy(WIDTH * 2 + 3, 19);
    printf("║ %7d ║", high_score);
    gotoxy(WIDTH * 2 + 3, 20);
    printf("╚═════════╝");

    // 显示下一个方块
    gotoxy(WIDTH * 2 + 3, 7);
    printf("╔════════╗");
    gotoxy(WIDTH * 2 + 3, 8);
    printf("║ 下一个 ║");
    gotoxy(WIDTH * 2 + 3, 9);
    printf("╠════════╣");

    int next_matrix[4][4];
    get_rotated_shape(next_shape, 0, next_matrix);
    for (int i = 0; i < BLOCK_SIZE; i++) {
        gotoxy(WIDTH * 2 + 3, 10 + i);
        printf("║");
        for (int j = 0; j < BLOCK_SIZE; j++) {
            if (next_matrix[i][j]) {
                setcolor(colors[next_shape]);
                printf("██");
                setcolor(7);
            } else {
                printf("  ");
            }
        }
        printf("║");
    }

    gotoxy(WIDTH * 2 + 3, 14);
    printf("╚════════╝");

    // 操作说明
    gotoxy(0, HEIGHT + 2);
    printf("操作说明:");
    printf("  ↑ - 旋转");
    printf("  ← - 左移");
    printf("  → - 右移");
    printf("  ↓ - 加速");
    printf("  P - 暂停");
    printf("  Q - 退出");

    if (paused) {
        gotoxy(WIDTH - 3, HEIGHT / 2);
        setcolor(14);
        printf("已暂停");
        setcolor(7);
    }
}

// 检查碰撞
int check_collision(int shape, int rotation, int x, int y) {
    int matrix[4][4];
    get_rotated_shape(shape, rotation, matrix);
    for (int i = 0; i < BLOCK_SIZE; i++) {
        for (int j = 0; j < BLOCK_SIZE; j++) {
            if (matrix[i][j]) {
                int new_x = x + j;
                int new_y = y + i;

                if (new_x < 0 || new_x >= WIDTH || new_y >= HEIGHT) {
                    return 1;
                }

                if (new_y >= 0 && board[new_y][new_x] > 0) {
                    return 1;
                }
            }
        }
    }
    return 0;
}

// 尝试旋转，支持墙踢
// 返回1表示旋转成功，0表示失败
int try_rotate_with_wall_kick(int* rotation, int* x, int* y) {
    int new_rotation = (*rotation + 1) % 4;
    int kick_tests[][2] = {{0, 0}, {-1, 0}, {1, 0}, {-2, 0}, {2, 0}, {-1, 1}, {1, 1}, {0, -1}};

    for (int i = 0; i < 8; i++) {
        int test_x = *x + kick_tests[i][0];
        int test_y = *y + kick_tests[i][1];

        if (!check_collision(current_shape, new_rotation, test_x, test_y)) {
            *rotation = new_rotation;
            *x = test_x;
            *y = test_y;
            return 1;
        }
    }

    return 0;
}

// 固定方块到游戏板
void lock_block() {
    int matrix[4][4];
    get_rotated_shape(current_shape, current_rotation, matrix);
    for (int i = 0; i < BLOCK_SIZE; i++) {
        for (int j = 0; j < BLOCK_SIZE; j++) {
            if (matrix[i][j]) {
                int board_y = current_y + i;
                int board_x = current_x + j;
                if (board_y >= 0) {
                    board[board_y][board_x] = colors[current_shape];
                }
            }
        }
    }
}

// 消除满行
void clear_lines() {
    int lines = 0;

    for (int y = HEIGHT - 1; y >= 0; y--) {
        int full = 1;
        for (int x = 0; x < WIDTH; x++) {
            if (board[y][x] == 0) {
                full = 0;
                break;
            }
        }

        if (full) {
            lines++;
            // 下移所有行
            for (int yy = y; yy > 0; yy--) {
                for (int x = 0; x < WIDTH; x++) {
                    board[yy][x] = board[yy - 1][x];
                }
            }
            // 清空顶行
            for (int x = 0; x < WIDTH; x++) {
                board[0][x] = 0;
            }
            y++;  // 重新检查当前行
        }
    }

    if (lines > 0) {
        lines_cleared += lines;
        score += lines * lines * 100 * level;
        level = lines_cleared / 10 + 1;
    }
}

// 生成新方块
void spawn_block() {
    current_shape = next_shape;
    current_rotation = 0;
    current_x = WIDTH / 2 - 2;
    current_y = 0;

    next_shape = rand() % 7;

    // 检查游戏结束
    if (check_collision(current_shape, current_rotation, current_x, current_y)) {
        game_over = 1;
    }
}

// 保存战绩记录到文件
void save_score_record(int score) {
    FILE *fp = fopen("tetris_records.txt", "a");
    if (fp == NULL) {
        return;
    }
    
    time_t now = time(NULL);
    char time_str[100];
    strftime(time_str, sizeof(time_str), "%Y-%m-%d %H:%M:%S", localtime(&now));
    
    fprintf(fp, "%s | 得分: %d\n", time_str, score);
    fclose(fp);
}

// 显示历史战绩
void show_score_records() {
    system("cls");
    printf("========================================\n");
    printf("           历史战绩记录\n");
    printf("========================================\n\n");
    
    FILE *fp = fopen("tetris_records.txt", "r");
    if (fp == NULL) {
        printf("暂无战绩记录！\n\n");
        printf("按任意键返回...");
        _getch();
        return;
    }
    
    char line[256];
    int record_count = 0;
    while (fgets(line, sizeof(line), fp) != NULL) {
        printf("%s", line);
        record_count++;
    }
    
    fclose(fp);
    
    if (record_count == 0) {
        printf("暂无战绩记录！\n\n");
    }
    
    printf("\n按任意键返回...");
    _getch();
}

// 获取最高分
int get_high_score() {
    int high_score = 0;
    FILE *fp = fopen("tetris_records.txt", "r");
    
    if (fp != NULL) {
        char line[256];
        while (fgets(line, sizeof(line), fp) != NULL) {
            int score;
            if (sscanf(line, "%*s %*s | 得分: %d", &score) == 1) {
                if (score > high_score) {
                    high_score = score;
                }
            }
        }
        fclose(fp);
    }
    
    return high_score;
}

// 初始化 AI
void init_ai() {
    init_ql_agent(&ai_agent);

    // 尝试加载已有训练数据
    if (load_q_table(&ai_agent, "tetris_qtable.txt")) {
        printf("已加载 AI 训练数据\n");
    } else {
        printf("AI 从头开始训练，正在注入启发式知识...\n");
        // 使用启发式知识初始化Q表，加快训练速度
        init_q_table_with_heuristics(&ai_agent);
        printf("启发式知识注入完成\n");
    }
}

// AI 获取最佳位置（带边界检查）
void ai_apply_decision() {
    if (ai_mode == 0) return;

    AIDecision decision = ai_make_decision(&ai_agent, current_shape, next_shape, board);

    // 应用 AI 决策
    int target_rotation = decision.rotation;
    int target_x = decision.position;

    // 检查目标旋转是否有效
    if (check_collision(current_shape, target_rotation, current_x, current_y)) {
        // 尝试其他旋转角度
        int valid_rotation = current_rotation;
        for (int rot = 0; rot < 4; rot++) {
            if (!check_collision(current_shape, rot, current_x, current_y)) {
                valid_rotation = rot;
                break;
            }
        }
        target_rotation = valid_rotation;
    }

    // 旋转到目标角度（使用墙踢）
    while (current_rotation != target_rotation) {
        int old_rot = current_rotation, old_x = current_x, old_y = current_y;
        if (!try_rotate_with_wall_kick(&current_rotation, &current_x, &current_y)) {
            current_rotation = old_rot;
            current_x = old_x;
            current_y = old_y;
            break;
        }
        draw_board();
        Sleep(50);
    }

    // 确保目标位置在有效范围内
    if (target_x < 0) target_x = 0;
    if (target_x >= WIDTH) target_x = WIDTH - 1;

    // 检查目标位置是否可达
    if (!check_collision(current_shape, current_rotation, target_x, current_y)) {
        // 移动到目标位置
        while (current_x != target_x) {
            if (target_x > current_x) {
                if (!check_collision(current_shape, current_rotation, current_x + 1, current_y)) {
                    current_x++;
                } else {
                    break;  // 右侧有障碍
                }
            } else {
                if (!check_collision(current_shape, current_rotation, current_x - 1, current_y)) {
                    current_x--;
                } else {
                    break;  // 左侧有障碍
                }
            }
            draw_board();
            Sleep(50);
        }
    } else {
        // 目标位置不可达，寻找最近的可行位置
        int best_x = current_x;
        int best_dist = abs(target_x - current_x);

        for (int x = 0; x < WIDTH; x++) {
            if (!check_collision(current_shape, current_rotation, x, current_y)) {
                int dist = abs(target_x - x);
                if (dist < best_dist) {
                    best_dist = dist;
                    best_x = x;
                }
            }
        }

        // 移动到最佳可行位置
        while (current_x != best_x) {
            if (best_x > current_x) {
                if (!check_collision(current_shape, current_rotation, current_x + 1, current_y)) {
                    current_x++;
                } else {
                    break;
                }
            } else {
                if (!check_collision(current_shape, current_rotation, current_x - 1, current_y)) {
                    current_x--;
                } else {
                    break;
                }
            }
            draw_board();
            Sleep(50);
        }
    }
}

// AI 训练模式游戏循环
void ai_game_loop() {
    // 根据模式显示不同提示
    if (ai_mode == 1) {
        printf("AI 观看模式中... 按 P 暂停, 按 Q 退出\n\n");
    } else {
        printf("AI 训练中... 按 P 暂停, 按 Q 退出训练\n");
        printf("            按 H 开启/关闭 人类干预训练（教AI怎么玩）\n\n");
    }
    Sleep(2000);

    int counter = 0;
    int delay = (ai_mode == 2) ? 200 : ai_auto_speed;  // 训练模式使用较慢的速度（便于人类干预）
    int lines_before = lines_cleared;
    int paused = 0;
    int draw_counter = 0;  // 绘制计数器，用于减少刷新频率
    int human_overridden = 0;  // 标记是否被人类覆盖

    // 观看模式：无限循环直到游戏结束；训练模式：直到达到最大回合数
    while (!game_over && (ai_mode == 1 || ai_episode < max_ai_episodes)) {
        // 检查暂停和停止
        if (_kbhit()) {
            int key = _getch();

            // 处理方向键（Windows方向键返回两个字节）
            int is_arrow = 0;
            if (key == 0 || key == 224) {
                key = _getch();
                is_arrow = 1;
            }

            // 暂停/继续
            if (!is_arrow && (key == 'p' || key == 'P')) {
                paused = !paused;
                if (ai_mode == 1) {
                    printf("\n%s\n", paused ? "观看暂停，按 P 继续..." : "观看继续...");
                } else {
                    printf("\n%s\n", paused ? "训练暂停，按 P 继续..." : "训练继续...");
                }
                if (paused) {
                    while (paused) {
                        if (_kbhit()) {
                            int pkey = _getch();
                            if (pkey == 'p' || pkey == 'P') {
                                paused = 0;
                                break;
                            }
                        }
                        Sleep(100);
                    }
                }
                printf("%s...\n", ai_mode == 1 ? "观看继续" : "训练继续");
            }
            // 退出
            else if (!is_arrow && (key == 'q' || key == 'Q')) {
                printf("\n%s已停止\n", ai_mode == 1 ? "观看" : "训练");
                if (ai_mode == 2) {
                    ai_early_exit = 1;
                }
                break;
            }
            // 人类干预训练（仅在训练模式下有效）
            else if (ai_mode == 2 && !is_arrow && (key == 'h' || key == 'H')) {
                human_intervention_active = !human_intervention_active;
                if (human_intervention_active) {
                    printf("\n[人类干预训练] 已启用！AI先决策，使用方向键修正，AI将学习您的修正\n");
                } else {
                    printf("\n[人类干预] 已关闭，恢复AI自主训练\n");
                }
            }
            // 人类控制方块（干预模式）
            else if (ai_mode == 2 && human_intervention_active && is_arrow) {
                int old_rotation = current_rotation;
                int old_x = current_x;

                switch (key) {
                    case 72:  // 上 - 旋转（带墙踢）
                        if (try_rotate_with_wall_kick(&current_rotation, &current_x, &current_y)) {
                            human_overridden = 1;
                        }
                        break;
                    case 80:  // 下 - 加速下落
                        current_y++;
                        if (check_collision(current_shape, current_rotation, current_x, current_y)) {
                            current_y--;  // 下键导致的碰撞是合法的锁定
                        } else {
                            human_overridden = 1;
                        }
                        break;
                    case 75:  // 左 - 左移
                        if (!check_collision(current_shape, current_rotation, current_x - 1, current_y)) {
                            current_x--;
                            human_overridden = 1;
                        }
                        break;
                    case 77:  // 右 - 右移
                        if (!check_collision(current_shape, current_rotation, current_x + 1, current_y)) {
                            current_x++;
                            human_overridden = 1;
                        }
                        break;
                }

                // 检查碰撞并撤销无效操作（除了已经处理的下键）
                if (key != 80 && key != 72 && check_collision(current_shape, current_rotation, current_x, current_y)) {
                    current_rotation = old_rotation;
                    current_x = old_x;
                }
            }
        }

        if (paused) {
            Sleep(100);
            continue;
        }

        // AI 自动下落
        Sleep(10);
        counter += 10;

        if (counter >= delay) {
            counter = 0;

            // AI总是自动决策，人类干预可以覆盖
            static AIDecision cached_decision;
            static int adjustment_count = 0;  // 追踪调整次数

            // AI在每个方块下落过程中做两次调整：
            // 第一次：方块刚出现时（adjustment_count == 0）
            // 第二次：方块下落到一半时（adjustment_count == 1）
            // 如果启用了人类干预且人类已经干预过，就不再调整
            if (!human_intervention_active || !human_overridden) {
                if (adjustment_count < 2) {
                    // 重新计算AI决策
                    AIDecision new_decision = ai_make_decision(&ai_agent, current_shape, next_shape, board);
                    cached_decision = new_decision;
                    adjustment_count++;

                    // 显示AI决策信息（调试模式或人类干预模式）
                    if (debug_ai_decision || human_intervention_active) {
                        GameStateFeatures features;
                        extract_game_features(board, &features);
                        int height_level, holes_level, bumpiness_level;
                        discretize_features(&features, &height_level, &holes_level, &bumpiness_level);

                        // 方块名称
                        const char* shape_names[] = {"I", "J", "L", "O", "S", "T", "Z"};
                        gotoxy(0, HEIGHT + 3);
                        printf("[AI决策#%d] 当前:%s 下一个:%s 高度:%d 空洞:%d 不平:%d -> 旋转:%d 位置:%d      ",
                               adjustment_count,
                               shape_names[current_shape],
                               shape_names[next_shape],
                               height_level, holes_level, bumpiness_level,
                               cached_decision.rotation, cached_decision.position);
                    }
                }
            }

            // 如果人类干预且被覆盖，使用人类的选择
            if (human_intervention_active && human_overridden) {
                cached_decision.rotation = current_rotation;
                cached_decision.position = current_x;
            }

            AIDecision decision = cached_decision;

            // 检查决策的边界问题
            int rotation_ok = !check_collision(current_shape, decision.rotation, current_x, current_y);
            int position_ok = !check_collision(current_shape, decision.rotation, decision.position, current_y);
            int position_valid = (decision.position >= 0 && decision.position < WIDTH);

            // 如果决策有问题，应用负反馈
            if (!rotation_ok || !position_ok || !position_valid) {
                if (ai_mode == 2 && !human_intervention_active) {
                    int state_idx = current_shape * 4;
                    int action = decision.rotation * 10 + decision.position;
                    double reward = -50.0;
                    ai_train(&ai_agent, state_idx, action, state_idx, reward);
                }
            }

            // 调整到有效的旋转
            int target_rotation = rotation_ok ? decision.rotation : current_rotation;

            // 调整到有效的位置（边界检测）
            int target_x = decision.position;
            if (target_x < 0) target_x = 0;
            if (target_x >= WIDTH) target_x = WIDTH - 1;

            // 检查目标位置是否可达
            if (!position_ok || !position_valid) {
                int best_x = current_x;
                int best_dist = abs(target_x - current_x);
                for (int x = 0; x < WIDTH; x++) {
                    if (!check_collision(current_shape, target_rotation, x, current_y)) {
                        int dist = abs(target_x - x);
                        if (dist < best_dist) {
                            best_dist = dist;
                            best_x = x;
                        }
                    }
                }
                target_x = best_x;
            }

            // 高度检查：如果最高高度在增大，考虑左右偏移
            static int previous_highest_point = 0;
            static int height_increasing_count = 0;

            // 计算当前棋盘的最高点
            GameStateFeatures current_features;
            extract_game_features(board, &current_features);

            // 检测高度是否在持续增加
            if (current_features.highest_point > previous_highest_point + 1) {
                height_increasing_count++;
                if (height_increasing_count >= 2) {
                    // 高度连续增加2次以上，考虑偏移
                    printf("[高度警告] 最高点持续上升(%d -> %d)，尝试偏移...\n",
                           previous_highest_point, current_features.highest_point);

                    // 尝试向左右偏移一格，选择更好的位置
                    int offset_positions[3] = {target_x, target_x - 1, target_x + 1};
                    int best_offset_pos = target_x;
                    double best_offset_score = -1e9;

                    for (int offset = 0; offset < 3; offset++) {
                        int test_pos = offset_positions[offset];
                        if (test_pos >= 0 && test_pos < WIDTH) {
                            // 检查这个位置是否有效
                            if (!check_collision(current_shape, target_rotation, test_pos, current_y)) {
                                // 计算该位置的落点高度
                                int test_drop_y = 0;
                                while (!check_collision(current_shape, target_rotation, test_pos, test_drop_y + 1)) {
                                    test_drop_y++;
                                }
                                int drop_height = HEIGHT - test_drop_y;

                                // 偏好低高度
                                double offset_score = (double)(20 - drop_height) * 10.0;
                                if (offset_score > best_offset_score) {
                                    best_offset_score = offset_score;
                                    best_offset_pos = test_pos;
                                }
                            }
                        }
                    }

                    if (best_offset_pos != target_x) {
                        printf("[位置调整] 位置 %d -> %d (更低的落点)\n", target_x, best_offset_pos);
                        target_x = best_offset_pos;
                        height_increasing_count = 0;  // 重置计数器
                    }
                }
            } else if (current_features.highest_point <= previous_highest_point) {
                // 高度没有增加，重置计数器
                height_increasing_count = 0;
            }

            // 更新之前的高度记录
            previous_highest_point = current_features.highest_point;

            // AI总是先执行决策，人类可以在下一个下落周期修正
            // 但是如果人类已经干预过，就不再执行AI的移动（保持人类的最终选择）
            if (!human_intervention_active || !human_overridden) {
                // 先旋转到目标角度（使用墙踢）
                while (current_rotation != target_rotation) {
                    int old_rot = current_rotation, old_x = current_x, old_y = current_y;
                    if (!try_rotate_with_wall_kick(&current_rotation, &current_x, &current_y)) {
                        current_rotation = old_rot;
                        current_x = old_x;
                        current_y = old_y;
                        break;
                    }
                }
            }

            // 再移动到目标位置（逐步移动）
            // 如果人类已经干预过，就不移动（保持人类的最终选择）
            if (!human_intervention_active || !human_overridden) {
                while (current_x != target_x) {
                    if (current_x < target_x) {
                        if (!check_collision(current_shape, current_rotation, current_x + 1, current_y)) {
                            current_x++;
                        } else {
                            break;
                        }
                    } else {
                        if (!check_collision(current_shape, current_rotation, current_x - 1, current_y)) {
                            current_x--;
                        } else {
                            break;
                        }
                    }
                }
            }

            // 更新决策，使用调整后的值
            decision.rotation = current_rotation;
            decision.position = current_x;

            // 尝试下落
            int old_y = current_y;
            current_y++;

            if (check_collision(current_shape, current_rotation, current_x, current_y)) {
                current_y = old_y;

                // 记录放置前的状态（用于学习）
                GameStateFeatures features_before;
                extract_game_features(board, &features_before);

                int score_before = score;
                int lines_before = lines_cleared;

                // 保存AI的原始决策（在锁定前）
                static AIDecision ai_original_decision;
                ai_original_decision = cached_decision;

                lock_block();
                clear_lines();
                spawn_block();

                // 每次生成新方块时，重置决策标志和人类干预标志
                static int adjustment_count = 0;
                adjustment_count = 0;
                human_overridden = 0;

                // 保存人类干预标志和AI原始决策，用于训练
                int was_human_overridden = human_overridden;

                // 训练：更新 Q 值
                if (ai_mode == 2) {
                    int lines_cleared_now = lines_cleared - lines_before;
                    int score_gain = score - score_before;

                    // 获取放置后的特征
                    GameStateFeatures features_after;
                    extract_game_features(board, &features_after);

                    // 计算AI决策的奖励（模拟）
                    double ai_reward = calculate_reward(&features_before, &features_after, lines_cleared_now);

                    // 人类干预时计算人类修正后的实际奖励
                    double human_reward = ai_reward;
                    if (human_intervention_active && was_human_overridden) {
                        // 消除行奖励
                        if (lines_cleared_now > 0) {
                            human_reward += lines_cleared_now * 250.0;
                        }

                        // 降低堆叠高度奖励
                        if (features_after.aggregate_height < features_before.aggregate_height) {
                            human_reward += 50.0;
                        }

                        // 减少空洞奖励
                        if (features_after.holes < features_before.holes) {
                            human_reward += 30.0;
                        }

                        // 填补缺口奖励
                        if (features_after.near_complete_lines > features_before.near_complete_lines) {
                            human_reward += (features_after.near_complete_lines - features_before.near_complete_lines) * 40.0;
                        }

                        // 区分AI错误和人类补充
                        if (ai_reward < 0 && human_reward > 0) {
                            // AI决策导致负奖励，人类修正后为正 -> 这是修正AI错误
                            printf("\r[修正AI错误] 原奖励%.1f -> 修正后%.1f (净提升%.1f)\n",
                                   ai_reward, human_reward, human_reward - ai_reward);
                        } else if (ai_reward >= 0 && human_reward > ai_reward) {
                            // AI决策还行，人类微调后更好 -> 这是补充AI能力
                            printf("\r[补充AI能力] 原奖励%.1f -> 微调后%.1f (提升%.1f)\n",
                                   ai_reward, human_reward, human_reward - ai_reward);
                        } else if (human_reward <= ai_reward) {
                            // 人类修正反而更差
                            printf("\r[修正未改进] 原奖励%.1f -> 修正后%.1f\n",
                                   ai_reward, human_reward);
                        }
                    } else {
                        // 人类未干预，使用AI决策
                        printf("\r[AI决策] 旋转=%d 位置=%d 消除=%d 奖励=%.1f\n",
                               ai_original_decision.rotation, ai_original_decision.position, lines_cleared_now, ai_reward);
                    }

                    // 计算最终奖励：人类干预用人类奖励，否则用AI奖励
                    double final_reward = (human_intervention_active && was_human_overridden) ? human_reward : ai_reward;

                    // 训练Q表
                    int state_idx = get_feature_based_state_index(
                        current_shape, next_shape,
                        features_before.aggregate_height / 4,  // 高度等级
                        features_before.holes / 2,             // 空洞等级
                        features_before.bumpiness / 4         // 不平整度等级
                    );

                    int action = decision.rotation * 10 + decision.position;
                    int q_idx = state_idx * 40 + action;

                    if (q_idx < Q_TABLE_SIZE) {
                        // 人类干预时使用更高的学习率
                        double learning_rate = (human_intervention_active && was_human_overridden) ? 0.5 : 0.3;
                        ai_agent.q_values[q_idx] += learning_rate * (final_reward - ai_agent.q_values[q_idx]);
                    }

                    if (!human_intervention_active && lines_before != lines_cleared) {
                        lines_before = lines_cleared;
                    }
                }
            }

            // 训练模式减少界面刷新频率（每2次绘制一次）
            draw_counter++;
            if (ai_mode != 2 || draw_counter % 2 == 0) {
                draw_board();
            }
        }
    }

    // 回合结束（仅在训练模式下）
    if (ai_mode == 2) {
        // 先检查是否已经达到最大回合数（避免超出一回合）
        if (ai_episode < max_ai_episodes) {
            ai_episode++;
            printf("\n回合 %d/%d 完成 - 得分: %d, 消除行: %d\n", ai_episode, max_ai_episodes, score, lines_cleared);
        }
    }

    // 保存训练数据（每10轮保存一次）
    if (ai_mode == 2 && ai_episode % 10 == 0) {
        save_q_table(&ai_agent, "tetris_qtable.txt");
        printf("训练参数已保存\n");
    }
}

// 主游戏循环
void game_loop() {
    int counter = 0;
    int delay = 1000 / level;

    while (!game_over) {
        // 处理输入
        if (_kbhit()) {
            int key = _getch();

            // 先判断是否是普通按键
            if (key == 'q' || key == 'Q') {
                game_over = 1;
                break;
            } else if (key == 'p' || key == 'P') {
                paused = !paused;
                draw_board();
                while (paused) {
                    if (_kbhit()) {
                        int pkey = _getch();
                        if (pkey == 'p' || pkey == 'P') {
                            paused = 0;
                            break;
                        }
                    }
                    Sleep(100);
                }
                continue;
            }

            // 处理方向键（Windows方向键返回两个字节）
            if (key == 0 || key == 224) {
                key = _getch();  // 获取第二个字节
            }

            if (!paused) {
                int old_rotation = current_rotation;
                int old_x = current_x;

                switch (key) {
                    case 72:  // 上 - 旋转（带墙踢）
                        try_rotate_with_wall_kick(&current_rotation, &current_x, &current_y);
                        break;
                    case 80:  // 下 - 加速
                        current_y++;
                        break;
                    case 75:  // 左 - 左移
                        current_x--;
                        break;
                    case 77:  // 右 - 右移
                        current_x++;
                        break;
                }

                // 检查碰撞，恢复位置
                if (check_collision(current_shape, current_rotation, current_x, current_y)) {
                    current_rotation = old_rotation;
                    current_x = old_x;

                    // 如果是下落导致的碰撞，锁定方块
                    if (key == 80) {
                        current_y--;
                        lock_block();
                        clear_lines();
                        spawn_block();
                    }
                }

                draw_board();
            }
        }

        // 自动下落
        Sleep(10);
        counter += 10;

        // AI 模式下自动决策
        if (ai_mode == 1 && counter >= ai_auto_speed) {
            ai_apply_decision();
        }

        if (counter >= delay && !paused) {
            counter = 0;

            int old_y = current_y;
            current_y++;

            if (check_collision(current_shape, current_rotation, current_x, current_y)) {
                current_y = old_y;

                // 记录玩家操作（手动模式且启用记录）
                if (ai_mode == 0 && record_player_moves) {
                    // 获取方块锁定前的特征
                    GameStateFeatures features;
                    extract_game_features(board, &features);

                    // 离散化特征
                    int height_level, holes_level, bumpiness_level;
                    discretize_features(&features, &height_level, &holes_level, &bumpiness_level);

                    // 创建记录
                    GameRecord record;
                    record.current_shape = current_shape;
                    record.next_shape = next_shape;
                    record.rotation = current_rotation;
                    record.position = current_x;
                    record.height_level = height_level;
                    record.holes_level = holes_level;
                    record.bumpiness_level = bumpiness_level;

                    // 记录放置前的状态
                    int score_before = score;
                    int lines_before_clear = lines_cleared;

                    lock_block();
                    clear_lines();

                    // 记录放置后的结果
                    record.lines_cleared = lines_cleared - lines_before_clear;
                    record.score_before = score_before;
                    record.score_after = score;

                    // 获取放置后的棋盘特征
                    GameStateFeatures after_features;
                    extract_game_features(board, &after_features);
                    record.height_after = after_features.highest_point;
                    record.holes_after = after_features.holes;
                    record.bumpiness_after = after_features.bumpiness;

                    // 添加到记录
                    add_record(&player_records, record);

                    spawn_block();
                } else {
                    lock_block();
                    clear_lines();
                    spawn_block();
                }
            }

            draw_board();
        }
    }

    // 游戏结束
    gotoxy(WIDTH - 4, HEIGHT / 2);
    setcolor(12);
    printf("游戏结束！");
    setcolor(7);
    gotoxy(WIDTH - 4, HEIGHT / 2 + 1);
    printf("最终得分: %d", score);
    gotoxy(0, HEIGHT + 5);

    // 保存战绩记录
    save_score_record(score);

    // 保存玩家游戏记录（如果有记录且是手动游戏，且得分 >= 12000）
    if (ai_mode == 0 && record_player_moves && player_records.count > 0) {
        if (score >= 12000) {
            printf("本次得分: %d >= 12000，是否保存游戏记录用于AI学习？(Y/N): ", score);
            char choice = getchar();
            while (getchar() != '\n'); // 清空输入缓冲区
            if (choice == 'Y' || choice == 'y') {
                save_records_to_file(&player_records, "tetris_player_records.txt");
                printf("游戏记录已保存！\n");
            } else {
                printf("游戏记录未保存。\n");
            }
        }
    }
}

int main() {
    srand(time(NULL));

    while (1) {
        system("cls");
        printf("========================================\n");
        printf("      俄罗斯方块游戏\n");
        printf("========================================\n\n");
        printf("  0. 退出游戏\n");
        printf("  1. 开始游戏\n");
        printf("  2. 查看战绩\n");
        printf("  3. AI 观看模式 (观看 AI 玩游戏)\n");
        printf("  4. AI 训练模式 (自动训练 AI)\n");
        printf("  5. 从玩家记录初始化 AI (模仿学习)\n\n");

        if (ai_mode > 0) {
            printf("  [AI 状态: %s]\n", ai_mode == 1 ? "观看中" : "训练中");
            if (ai_mode == 2) {
                printf("  [训练回合: %d/%d]\n\n", ai_episode, max_ai_episodes);
            } else {
                printf("  [当前得分: %d]\n\n", ai_episode > 0 ? score : 0);
            }
        }

        printf("请选择操作 (0-5): ");

        int choice;
        scanf("%d", &choice);
        while (getchar() != '\n');  // 清除输入缓冲区

        if (choice == 1) {
            // 开始游戏（手动模式）
            ai_mode = 0;
            SetConsoleTitleA("俄罗斯方块 - Tetris Game");

            printf("\n按任意键开始游戏...\n");
            _getch();

            // 重置音乐播放标志
            music_playing = 1;

            // 启动音乐播放线程
            // 设置控制台标题
            SetConsoleTitleA("俄罗斯方块 - Tetris Game");

            printf("\n按任意键开始游戏...\n");
            _getch();

            // 重置音乐播放标志
            music_playing = 1;

            // 启动音乐播放线程
            HANDLE hMusicThread = (HANDLE)_beginthreadex(NULL, 0, music_thread, NULL, 0, NULL);

            init_game();
            draw_board();
            game_loop();

            // 停止音乐线程
            music_playing = 0;
            mciSendString("stop bgm", NULL, 0, NULL);
            mciSendString("close bgm", NULL, 0, NULL);
            WaitForSingleObject(hMusicThread, 3000);  // 等待线程结束
            CloseHandle(hMusicThread);

            printf("\n按任意键返回主菜单...\n");
            _getch();

            // 重置AI模式
            ai_mode = 0;
        } else if (choice == 2) {
            show_score_records();
        } else if (choice == 3) {
            // AI 观看模式
            ai_mode = 1;
            ai_episode = 0;  // 重置回合计数（虽然观看模式不使用）
            init_ai();
            SetConsoleTitleA("AI 观看模式 - Tetris AI");

            printf("\n按任意键开始 AI 游戏...\n");
            _getch();

            music_playing = 1;
            HANDLE hMusicThread = (HANDLE)_beginthreadex(NULL, 0, music_thread, NULL, 0, NULL);

            init_game();
            draw_board();
            ai_game_loop();

            music_playing = 0;
            mciSendString("stop bgm", NULL, 0, NULL);
            mciSendString("close bgm", NULL, 0, NULL);
            WaitForSingleObject(hMusicThread, 3000);
            CloseHandle(hMusicThread);

            printf("\n按任意键返回主菜单...\n");
            _getch();

            // 重置AI模式
            ai_mode = 0;
        } else if (choice == 4) {
            // AI 训练模式
            ai_mode = 2;
            init_ai();

            printf("\n设置训练回合数 (默认 100): ");
            char input[10];
            fgets(input, sizeof(input), stdin);
            int episodes = atoi(input);
            if (episodes > 0) max_ai_episodes = episodes;

            printf("\n显示AI决策调试信息? (Y/N, 默认N): ");
            char debug_choice = getchar();
            while (getchar() != '\n');  // 清空输入缓冲区
            debug_ai_decision = (debug_choice == 'Y' || debug_choice == 'y');

            printf("\n========================================\n");
            printf("AI 训练模式准备就绪\n");
            printf("========================================\n");
            printf("  训练回合数: %d\n", max_ai_episodes);
            printf("  调试信息: %s\n", debug_ai_decision ? "开启" : "关闭");
            printf("  操作说明:\n");
            printf("    P - 暂停/继续训练\n");
            printf("    Q - 退出训练模式\n");
            printf("    H - 开启/关闭 人类干预训练（教AI怎么玩）\n");
            printf("  人类干预模式下:\n");
            printf("    ↑ - 旋转  ↓ - 加速  ← → - 左右移动\n");
            printf("========================================\n");
            printf("\n按任意键开始训练...\n");
            _getch();

            ai_episode = 0;
            ai_early_exit = 0;  // 重置提前退出标志
            while (ai_episode < max_ai_episodes && !ai_early_exit) {
                init_game();
                ai_game_loop();
            }

            // 保存最终训练数据
            save_q_table(&ai_agent, "tetris_qtable.txt");

            if (ai_early_exit) {
                printf("\n训练已提前停止，共训练 %d 回合\n", ai_episode);
            } else {
                printf("\n训练完成！共训练 %d 回合\n", ai_episode);
            }
            printf("按任意键返回主菜单...\n");
            _getch();

            // 重置AI模式，避免主菜单显示错误状态
            ai_mode = 0;
        } else if (choice == 5) {
            // 从玩家记录初始化 AI（模仿学习）
            ai_mode = 0;
            printf("\n加载玩家游戏记录...\n");
            load_records_from_file(&player_records, "tetris_player_records.txt");

            if (player_records.count > 0) {
                printf("从 %d 条玩家记录中初始化Q表...\n", player_records.count);
                initialize_q_from_records(&ai_agent, &player_records);
                printf("Q表初始化完成！\n");
                printf("现在可以使用 AI 训练模式继续优化策略\n");
            } else {
                printf("未找到玩家记录！请先手动游戏以生成记录。\n");
            }

            printf("\n按任意键返回主菜单...\n");
            _getch();
        } else if (choice == 0) {
            printf("\n感谢游玩！再见！\n");
            break;
        } else {
            printf("\n无效的选择，请重新输入...\n");
            Sleep(1000);
        }

        system("cls");
    }

    return 0;
}
