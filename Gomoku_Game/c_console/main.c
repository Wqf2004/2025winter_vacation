#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <conio.h>
#include <windows.h>

#define BOARD_SIZE 15
#define ARRAY_SIZE (BOARD_SIZE + 2)

// 棋子颜色
#define EMPTY 0
#define BLACK 1
#define WHITE 2

// 棋盘符号
const unsigned char element[][3] = {
    {0xA9, 0xB3},  // ┏ top left
    {0xA9, 0xD3},  // ┯ top center
    {0xA9, 0xB7},  // ┓ top right
    {0xA9, 0xC4},  // ┠ middle left
    {0xA9, 0xE0},  // ┼ middle center
    {0xA9, 0xCC},  // ┨ middle right
    {0xA9, 0xBB},  // ┗ bottom left
    {0xA9, 0xDB},  // ┷ bottom center
    {0xA9, 0xBF},  // ┛ bottom right
    {0xA1, 0xF1},  // ● black
    {0xA1, 0xF0}   // ○ white
};

#define TAB_TOP_LEFT 0
#define TAB_TOP_CENTER 1
#define TAB_TOP_RIGHT 2
#define TAB_MIDDLE_LEFT 3
#define TAB_MIDDLE_CENTER 4
#define TAB_MIDDLE_RIGHT 5
#define TAB_BOTTOM_LEFT 6
#define TAB_BOTTOM_CENTER 7
#define TAB_BOTTOM_RIGHT 8
#define CHESSMAN_BLACK 9
#define CHESSMAN_WHITE 10

// 枚举
enum { false = 0, true = !false };

// 坐标结构体 - 使用 GomokuPoint 避免与 Windows.h 的 POINT 冲突
typedef struct {
    int x, y;
} GomokuPoint;

// 历史记录
GomokuPoint history[ARRAY_SIZE * ARRAY_SIZE];
int history_count = 0;

// 棋盘
int chessboard[ARRAY_SIZE][ARRAY_SIZE];

// 游戏模式
typedef enum {
    MODE_COMPUTER_FIRST,  // 计-人
    MODE_PLAYER_FIRST,    // 人-计
    MODE_PLAYER_VS_PLAYER // 人-人
} GameMode;

// 方向数组
const int dir[4][2] = {
    {0, 1},   // 横
    {1, 0},   // 竖
    {1, 1},   // 捺
    {1, -1}   // 撇
};

// 清屏宏
#ifdef WIN32
#define CLS "cls"
#else
#define CLS "clear"
#endif

// 函数声明
void init_chessboard(void);
void show_chessboard(void);
int choice(void);
GomokuPoint from_user(int color);
GomokuPoint from_computer(int color);
int calc_value(GomokuPoint p, int color);
int has_end(GomokuPoint p);
int in_board(GomokuPoint p);
int equal(GomokuPoint p1, GomokuPoint p2, int color);
void undo_move(void);
void save_game(void);
void load_game(void);

// 初始化棋盘
void init_chessboard(void) {
    int x, y;
    
    // 四个角
    chessboard[0][0] = TAB_TOP_LEFT;
    chessboard[0][BOARD_SIZE + 1] = TAB_TOP_RIGHT;
    chessboard[BOARD_SIZE + 1][0] = TAB_BOTTOM_LEFT;
    chessboard[BOARD_SIZE + 1][BOARD_SIZE + 1] = TAB_BOTTOM_RIGHT;
    
    // 上边
    for (x = 1; x <= BOARD_SIZE; x++) {
        chessboard[0][x] = TAB_TOP_CENTER;
    }
    
    // 下边
    for (x = 1; x <= BOARD_SIZE; x++) {
        chessboard[BOARD_SIZE + 1][x] = TAB_BOTTOM_CENTER;
    }
    
    // 左边
    for (y = 1; y <= BOARD_SIZE; y++) {
        chessboard[y][0] = TAB_MIDDLE_LEFT;
    }
    
    // 右边
    for (y = 1; y <= BOARD_SIZE; y++) {
        chessboard[y][BOARD_SIZE + 1] = TAB_MIDDLE_RIGHT;
    }
    
    // 中间
    for (y = 1; y <= BOARD_SIZE; y++) {
        for (x = 1; x <= BOARD_SIZE; x++) {
            chessboard[y][x] = TAB_MIDDLE_CENTER;
        }
    }
    
    // 清空历史记录
    history_count = 0;
}

// 显示棋盘
void show_chessboard(void) {
    int x, y;
    
    system(CLS);
#ifdef WIN32
    system("color F0");
#endif
    
    printf("========================================\n");
    printf("           五子棋游戏\n");
    printf("========================================\n");
    
    // 显示列号
    printf("   ");
    for (x = 1; x <= BOARD_SIZE; x++) {
        printf("%2d", x);
    }
    printf("\n");
    
    for (y = 1; y <= BOARD_SIZE; y++) {
        printf("%2d ", y);
        for (x = 1; x <= BOARD_SIZE; x++) {
            printf("%3s", element[chessboard[y][x]]);
        }
        printf("\n");
    }
    
    printf("========================================\n");
    printf("当前步数: %d\n", history_count);
    printf("========================================\n");
}

// 菜单选择
int choice(void) {
    int res = 0;
    printf("1) 计-人 (计算机先手)\n");
    printf("2) 人-计 (玩家先手)\n");
    printf("3) 人-人 (双人对战)\n");
    printf("4) 读取存档\n");
    printf("0) 退出\n");
    printf("请选择: ");
    scanf("%d", &res);
    getchar();
    return res;
}

// 玩家落子
GomokuPoint from_user(int color) {
    (void)color;  // 避免未使用参数警告
    GomokuPoint p = {0, 0};
    int failure = false;
    
    while (1) {
        printf("请输入落子位置 (x y, 输入 u 悔棋, q 退出): ");
        
        char input[100];
        fgets(input, sizeof(input), stdin);
        
        if (input[0] == 'q' || input[0] == 'Q') {
            p.x = -1;
            return p;
        }
        
        if (input[0] == 'u' || input[0] == 'U') {
            if (history_count >= 2) {
                undo_move();
                undo_move();
                show_chessboard();
            } else {
                printf("步数不足，无法悔棋！\n");
            }
            continue;
        }
        
        if (sscanf(input, "%d %d", &p.x, &p.y) != 2) {
            failure = true;
        } else if (!in_board(p)) {
            failure = true;
        } else if (chessboard[p.y][p.x] != TAB_MIDDLE_CENTER) {
            failure = true;
        }
        
        if (failure) {
            printf("无效位置！请重新输入。\n");
            failure = false;
        } else {
            return p;
        }
    }
}

// 计算落子价值
int calc_value(GomokuPoint p, int color) {
    static const int values[] = {
        0, 100, 600, 6000, 40000
    };
    static const int center = BOARD_SIZE / 2 + BOARD_SIZE % 2;

    int d, i;
    int sum = 0;
    int opponent = (color == BLACK) ? WHITE : BLACK;
    
    // 检查每个方向
    for (d = 0; d < 4; d++) {
        int count = 1;
        int blocked = 0;
        
        // 正方向
        for (i = 1; i < 5; i++) {
            GomokuPoint check = {p.x + i * dir[d][0], p.y + i * dir[d][1]};
            if (!in_board(check)) {
                blocked++;
                break;
            }
            if (equal(check, p, color)) {
                count++;
            } else if (chessboard[check.y][check.x] == TAB_MIDDLE_CENTER) {
                break;
            } else {
                blocked++;
                break;
            }
        }

        // 反方向
        for (i = 1; i < 5; i++) {
            GomokuPoint check = {p.x - i * dir[d][0], p.y - i * dir[d][1]};
            if (!in_board(check)) {
                blocked++;
                break;
            }
            if (equal(check, p, color)) {
                count++;
            } else if (chessboard[check.y][check.x] == TAB_MIDDLE_CENTER) {
                break;
            } else {
                blocked++;
                break;
            }
        }
        
        if (count >= 5) {
            return 100000;
        }
        
        if (count <= 4) {
            sum += values[count] * (2 - blocked);
        }
        
        // 检查阻挡对手
        int block_count = 1;
        for (i = 1; i < 5; i++) {
            GomokuPoint check = {p.x + i * dir[d][0], p.y + i * dir[d][1]};
            if (!in_board(check)) break;
            if (chessboard[check.y][check.x] == (opponent == BLACK ? CHESSMAN_BLACK : CHESSMAN_WHITE)) {
                block_count++;
            } else {
                break;
            }
        }
        for (i = 1; i < 5; i++) {
            GomokuPoint check = {p.x - i * dir[d][0], p.y - i * dir[d][1]};
            if (!in_board(check)) break;
            if (chessboard[check.y][check.x] == (opponent == BLACK ? CHESSMAN_BLACK : CHESSMAN_WHITE)) {
                block_count++;
            } else {
                break;
            }
        }
        
        if (block_count >= 3) {
            sum += values[block_count] / 2;
        }
    }
    
    // 位置价值（越靠近中心价值越高）
    sum += (center - abs(center - p.x)) * (center - abs(center - p.y));
    
    return sum;
}

// 计算机落子
GomokuPoint from_computer(int color) {
    GomokuPoint p = {0, 0}, m = p;
    int max = 0, v;
    int x, y;
    
    printf("计算机正在思考...\n");
    
    // 如果是第一步，下在中心
    if (history_count == 0) {
        m.x = (BOARD_SIZE + 1) / 2;
        m.y = (BOARD_SIZE + 1) / 2;
        return m;
    }
    
    // 扫描整个棋盘
    for (y = 1; y <= BOARD_SIZE; y++) {
        for (x = 1; x <= BOARD_SIZE; x++) {
            p.x = x;
            p.y = y;
            
            if (chessboard[y][x] == TAB_MIDDLE_CENTER) {
                v = calc_value(p, color);
                if (v > max) {
                    max = v;
                    m = p;
                }
            }
        }
    }
    
    return m;
}

// 悔棋
void undo_move(void) {
    if (history_count > 0) {
        GomokuPoint p = history[history_count - 1];
        chessboard[p.y][p.x] = TAB_MIDDLE_CENTER;
        history_count--;
    }
}

// 判断是否在棋盘内
int in_board(GomokuPoint p) {
    return p.x >= 1 && p.x <= BOARD_SIZE && p.y >= 1 && p.y <= BOARD_SIZE;
}

// 判断两个位置棋子颜色是否相同
int equal(GomokuPoint p1, GomokuPoint p2, int color) {
    (void)p2;  // 避免未使用参数警告
    int chess_symbol = (color == BLACK) ? CHESSMAN_BLACK : CHESSMAN_WHITE;
    return chessboard[p1.y][p1.x] == chess_symbol;
}

// 判断游戏是否结束
int has_end(GomokuPoint p) {
    int d, i;
    int color = chessboard[p.y][p.x] == CHESSMAN_BLACK ? BLACK : WHITE;
    
    for (d = 0; d < 4; d++) {
        int count = 1;
        
        // 正方向
        for (i = 1; i < 5; i++) {
            GomokuPoint check = {p.x + i * dir[d][0], p.y + i * dir[d][1]};
            if (!in_board(check) || !equal(check, p, color)) {
                break;
            }
            count++;
        }

        // 反方向
        for (i = 1; i < 5; i++) {
            GomokuPoint check = {p.x - i * dir[d][0], p.y - i * dir[d][1]};
            if (!in_board(check) || !equal(check, p, color)) {
                break;
            }
            count++;
        }
        
        if (count >= 5) {
            return true;
        }
    }
    
    return false;
}

// 保存游戏
void save_game(void) {
    FILE* fp = fopen("../dataset/save.txt", "w");
    if (fp == NULL) {
        printf("无法保存游戏！\n");
        return;
    }
    
    fprintf(fp, "%d\n", history_count);
    for (int i = 0; i < history_count; i++) {
        fprintf(fp, "%d %d\n", history[i].x, history[i].y);
    }
    
    fclose(fp);
    printf("游戏已保存！\n");
}

// 读取游戏
void load_game(void) {
    FILE* fp = fopen("../dataset/save.txt", "r");
    if (fp == NULL) {
        printf("没有存档！\n");
        return;
    }
    
    init_chessboard();
    
    fscanf(fp, "%d", &history_count);
    for (int i = 0; i < history_count; i++) {
        fscanf(fp, "%d %d", &history[i].x, &history[i].y);
        int color = (i % 2 == 0) ? BLACK : WHITE;
        chessboard[history[i].y][history[i].x] = (color == BLACK) ? CHESSMAN_BLACK : CHESSMAN_WHITE;
    }
    
    fclose(fp);
    printf("存档已读取！\n");
    show_chessboard();
}

// 主游戏循环
void play_game(GameMode mode) {
    init_chessboard();
    show_chessboard();

    int current_color = BLACK;
    GomokuPoint (*get_point[2])(int);
    
    // 设置落子函数
    if (mode == MODE_COMPUTER_FIRST) {
        get_point[0] = from_computer;
        get_point[1] = from_user;
    } else if (mode == MODE_PLAYER_FIRST) {
        get_point[0] = from_user;
        get_point[1] = from_computer;
    } else {
        get_point[0] = from_user;
        get_point[1] = from_user;
    }
    
    int who = 0;
    
    while (1) {
        GomokuPoint p = (*get_point[who])(current_color);
        
        // 检查是否退出
        if (p.x == -1) {
            printf("游戏结束！\n");
            break;
        }
        
        // 落子
        chessboard[p.y][p.x] = (current_color == BLACK) ? CHESSMAN_BLACK : CHESSMAN_WHITE;
        history[history_count++] = p;
        
        // 显示棋盘
        show_chessboard();
        
        // 检查是否胜利
        if (has_end(p)) {
            char* winner = (current_color == BLACK) ? "黑方" : "白方";
            printf("========================================\n");
            printf("        %s获胜！\n", winner);
            printf("========================================\n");
            
            // 询问是否保存
            printf("是否保存对局记录？(y/n): ");
            char choice;
            scanf(" %c", &choice);
            getchar();
            if (choice == 'y' || choice == 'Y') {
                save_game();
            }
            break;
        }
        
        // 检查是否平局
        if (history_count >= BOARD_SIZE * BOARD_SIZE) {
            printf("========================================\n");
            printf("           平局！\n");
            printf("========================================\n");
            break;
        }
        
        // 切换颜色
        current_color = (current_color == BLACK) ? WHITE : BLACK;
        who = (who + 1) % 2;
    }
}

// 主函数
int main(void) {
    // 创建数据目录
    CreateDirectory("../dataset", NULL);
    
    while (1) {
        int choice_val = choice();
        
        switch (choice_val) {
            case 1:
                play_game(MODE_COMPUTER_FIRST);
                break;
            case 2:
                play_game(MODE_PLAYER_FIRST);
                break;
            case 3:
                play_game(MODE_PLAYER_VS_PLAYER);
                break;
            case 4:
                load_game();
                printf("继续游戏？(y/n): ");
                char c;
                scanf(" %c", &c);
                getchar();
                if (c == 'y' || c == 'Y') {
                    play_game(MODE_PLAYER_VS_PLAYER);
                }
                break;
            case 0:
                printf("感谢使用五子棋游戏！\n");
                return 0;
            default:
                printf("无效选择！\n");
        }
        
        printf("\n按任意键继续...\n");
        getch();
    }
    
    return 0;
}
