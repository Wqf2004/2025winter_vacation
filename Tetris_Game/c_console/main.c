/*
 * 俄罗斯方块游戏 - C语言控制台版
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <conio.h>
#include <windows.h>

#define WIDTH 10
#define HEIGHT 20
#define BLOCK_SIZE 4

// 方块形状定义（7种形状 × 4种旋转状态）
// 0: I形, 1: J形, 2: L形, 3: O形, 4: S形, 5: T形, 6: Z形
int shapes[7][4][4][4] = {
    // I形 - 4格直线
    {
        {{0,0,0,0}, {1,1,1,1}, {0,0,0,0}, {0,0,0,0}},
        {{0,0,1,0}, {0,0,1,0}, {0,0,1,0}, {0,0,1,0}},
        {{0,0,0,0}, {0,0,0,0}, {1,1,1,1}, {0,0,0,0}},
        {{0,1,0,0}, {0,1,0,0}, {0,1,0,0}, {0,1,0,0}}
    },
    // J形 - 倒L (三横一竖，竖在右下)
    {
        {{1,1,1,0}, {0,0,1,0}, {0,0,0,0}, {0,0,0,0}},  // 横向，竖在右
        {{0,0,1,0}, {0,0,1,0}, {0,1,1,0}, {0,0,0,0}},  
        {{0,0,0,0}, {1,0,0,0}, {1,1,1,0}, {0,0,0,0}},  
        {{1,1,0,0}, {1,0,0,0}, {1,0,0,0}, {0,0,0,0}}   // 竖向，凸出在上
    },
    // L形 (三横一竖，竖在左下)
    {
        {{1,1,1,0}, {1,0,0,0}, {0,0,0,0}, {0,0,0,0}},  // 横向，竖在左
        {{0,1,1,0}, {0,0,1,0}, {0,0,1,0}, {0,0,0,0}},  
        {{0,0,0,0}, {0,0,1,0}, {1,1,1,0}, {0,0,0,0}},  
        {{1,0,0,0}, {1,0,0,0}, {1,1,0,0}, {0,0,0,0}}   
    },
    // O形 - 2x2正方形
    {
        {{1,1,0,0}, {1,1,0,0}, {0,0,0,0}, {0,0,0,0}},
        {{1,1,0,0}, {1,1,0,0}, {0,0,0,0}, {0,0,0,0}},
        {{1,1,0,0}, {1,1,0,0}, {0,0,0,0}, {0,0,0,0}},
        {{1,1,0,0}, {1,1,0,0}, {0,0,0,0}, {0,0,0,0}}
    },
    // S形
    {
        {{0,1,1,0}, {1,1,0,0}, {0,0,0,0}, {0,0,0,0}},
        {{0,1,0,0}, {0,1,1,0}, {0,0,1,0}, {0,0,0,0}},
        {{0,1,1,0}, {1,1,0,0}, {0,0,0,0}, {0,0,0,0}},
        {{0,1,0,0}, {0,1,1,0}, {0,0,1,0}, {0,0,0,0}}
    },
    // T形
    {
        {{0,1,0,0}, {1,1,1,0}, {0,0,0,0}, {0,0,0,0}},
        {{0,1,0,0}, {0,1,1,0}, {0,1,0,0}, {0,0,0,0}},
        {{0,0,0,0}, {1,1,1,0}, {0,1,0,0}, {0,0,0,0}},
        {{0,1,0,0}, {1,1,0,0}, {0,1,0,0}, {0,0,0,0}}
    },
    // Z形
    {
        {{1,1,0,0}, {0,1,1,0}, {0,0,0,0}, {0,0,0,0}},
        {{0,0,1,0}, {0,1,1,0}, {0,1,0,0}, {0,0,0,0}},
        {{1,1,0,0}, {0,1,1,0}, {0,0,0,0}, {0,0,0,0}},
        {{0,0,1,0}, {0,1,1,0}, {0,1,0,0}, {0,0,0,0}}
    }
};

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
    system("cls");

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
    for (int i = 0; i < BLOCK_SIZE; i++) {
        for (int j = 0; j < BLOCK_SIZE; j++) {
            if (shapes[current_shape][current_rotation][i][j]) {
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
    printf("╔════════╗");
    gotoxy(WIDTH * 2 + 3, 2);
    printf("║ 分数: %4d ║", score);
    gotoxy(WIDTH * 2 + 3, 3);
    printf("║ 等级: %4d ║", level);
    gotoxy(WIDTH * 2 + 3, 4);
    printf("║ 行数: %4d ║", lines_cleared);
    gotoxy(WIDTH * 2 + 3, 5);
    printf("╚════════╝");

    // 显示下一个方块
    gotoxy(WIDTH * 2 + 3, 7);
    printf("╔════════╗");
    gotoxy(WIDTH * 2 + 3, 8);
    printf("║ 下一个  ║");
    gotoxy(WIDTH * 2 + 3, 9);
    printf("╠════════╣");

    for (int i = 0; i < BLOCK_SIZE; i++) {
        gotoxy(WIDTH * 2 + 3, 10 + i);
        printf("║");
        for (int j = 0; j < BLOCK_SIZE; j++) {
            if (shapes[next_shape][0][i][j]) {
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
    for (int i = 0; i < BLOCK_SIZE; i++) {
        for (int j = 0; j < BLOCK_SIZE; j++) {
            if (shapes[shape][rotation][i][j]) {
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

// 固定方块到游戏板
void lock_block() {
    for (int i = 0; i < BLOCK_SIZE; i++) {
        for (int j = 0; j < BLOCK_SIZE; j++) {
            if (shapes[current_shape][current_rotation][i][j]) {
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
                    case 72:  // 上 - 旋转
                        current_rotation = (current_rotation + 1) % 4;
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

        if (counter >= delay && !paused) {
            counter = 0;

            int old_y = current_y;
            current_y++;

            if (check_collision(current_shape, current_rotation, current_x, current_y)) {
                current_y = old_y;
                lock_block();
                clear_lines();
                spawn_block();
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
}

int main() {
    srand(time(NULL));

    printf("========================================\n");
    printf("      俄罗斯方块游戏\n");
    printf("========================================\n\n");

    // 设置控制台标题
    SetConsoleTitleA("俄罗斯方块 - Tetris Game");

    printf("按任意键开始游戏...\n");
    _getch();

    init_game();
    draw_board();
    game_loop();

    printf("\n按任意键退出...\n");
    _getch();

    return 0;
}
