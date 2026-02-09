#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <conio.h>
#include <windows.h>

#define SIZE 10
#define MAP_SIZE (SIZE + 2)
#define MAX_NAME 50
#define MAX_PASS 50
#define MAX_USERS 100

// 全局地图数组
int map[MAP_SIZE][MAP_SIZE];
int mines_count = 10;
int mines_remaining = 10;
int cells_revealed = 0;
int game_over = 0;
int game_won = 0;
time_t start_time;

// 用户数据结构
typedef struct {
    char name[MAX_NAME];
    char pass[MAX_PASS];
    int best_time;
} User;

User users[MAX_USERS];
int user_count = 0;
User current_user;

// 文件路径
const char* USER_FILE = "../dataset/user.txt";
const char* RANK_FILE = "../dataset/rank.txt";

// 函数声明
void print_menu();
void print_game_menu();
void register_user();
int login_user();
void game_init(int rows, int cols, int mines);
void draw_map();
void count_adjacent_mines();
int reveal_cell(int x, int y);
void mark_cell(int x, int y);
int check_win();
void play_game();
void print_instructions();
void load_users();
void save_users();
void save_score(int time_used);
void display_rankings();
int get_difficulty();

// 打印主菜单
void print_menu() {
    system("cls");
    printf("========================================\n");
    printf("           扫雷游戏系统\n");
    printf("========================================\n");
    printf("1. 注册\n");
    printf("2. 登录\n");
    printf("3. 游戏说明\n");
    printf("0. 退出\n");
    printf("========================================\n");
    printf("请选择操作: ");
}

// 打印游戏菜单
void print_game_menu() {
    system("cls");
    printf("========================================\n");
    printf("        扫雷游戏 - %s\n", current_user.name);
    printf("========================================\n");
    printf("1. 开始游戏\n");
    printf("2. 查看排行榜\n");
    printf("3. 游戏说明\n");
    printf("4. 返回主菜单\n");
    printf("========================================\n");
    printf("请选择操作: ");
}

// 注册用户
void register_user() {
    char name[MAX_NAME];
    char pass[MAX_PASS];
    char confirm[MAX_PASS];
    
    system("cls");
    printf("========================================\n");
    printf("              用户注册\n");
    printf("========================================\n");
    
    printf("请输入用户名: ");
    scanf("%s", name);
    getchar();
    
    // 检查用户名是否已存在
    for (int i = 0; i < user_count; i++) {
        if (strcmp(users[i].name, name) == 0) {
            printf("\n该用户名已存在！按任意键继续...\n");
            getch();
            return;
        }
    }
    
    printf("请输入密码: ");
    scanf("%s", pass);
    getchar();
    
    printf("请确认密码: ");
    scanf("%s", confirm);
    getchar();
    
    if (strcmp(pass, confirm) != 0) {
        printf("\n两次密码不一致！按任意键继续...\n");
        getch();
        return;
    }
    
    // 添加用户
    strcpy(users[user_count].name, name);
    strcpy(users[user_count].pass, pass);
    users[user_count].best_time = -1;
    user_count++;
    
    // 保存到文件
    save_users();
    
    printf("\n注册成功！按任意键继续...\n");
    getch();
}

// 登录用户
int login_user() {
    char name[MAX_NAME];
    char pass[MAX_PASS];
    
    system("cls");
    printf("========================================\n");
    printf("              用户登录\n");
    printf("========================================\n");
    
    printf("请输入用户名: ");
    scanf("%s", name);
    getchar();
    
    printf("请输入密码: ");
    scanf("%s", pass);
    getchar();
    
    // 检查用户名和密码
    for (int i = 0; i < user_count; i++) {
        if (strcmp(users[i].name, name) == 0 && strcmp(users[i].pass, pass) == 0) {
            current_user = users[i];
            printf("\n登录成功！按任意键继续...\n");
            getch();
            return 1;
        }
    }
    
    printf("\n用户名或密码错误！按任意键继续...\n");
    getch();
    return 0;
}

// 游戏初始化
void game_init(int rows, int cols, int mines) {
    srand(time(NULL));
    
    // 初始化地图
    for (int i = 0; i < MAP_SIZE; i++) {
        for (int j = 0; j < MAP_SIZE; j++) {
            map[i][j] = 0;
        }
    }
    
    // 随机放置地雷
    int placed = 0;
    while (placed < mines) {
        int r = rand() % rows + 1;
        int c = rand() % cols + 1;
        if (map[r][c] != -1) {
            map[r][c] = -1;
            placed++;
        }
    }
    
    // 计算周围地雷数
    count_adjacent_mines();
    
    // 重置游戏状态
    mines_remaining = mines;
    cells_revealed = 0;
    game_over = 0;
    game_won = 0;
}

// 计算周围地雷数
void count_adjacent_mines() {
    for (int i = 1; i <= SIZE; i++) {
        for (int j = 1; j <= SIZE; j++) {
            if (map[i][j] != -1) {
                int count = 0;
                for (int di = -1; di <= 1; di++) {
                    for (int dj = -1; dj <= 1; dj++) {
                        if (map[i + di][j + dj] == -1) {
                            count++;
                        }
                    }
                }
                map[i][j] = count;
            }
        }
    }
}

// 绘制地图
void draw_map() {
    system("cls");
    printf("========================================\n");
    printf("          扫雷游戏\n");
    printf("========================================\n");
    printf("剩余雷数: %d\n", mines_remaining);
    time_t elapsed = time(NULL) - start_time;
    printf("时间: %lld秒\n", (long long)elapsed);
    printf("========================================\n");
    
    printf("   ");
    for (int j = 1; j <= SIZE; j++) {
        printf("%2d ", j);
    }
    printf("\n");
    
    for (int i = 1; i <= SIZE; i++) {
        printf("%2d ", i);
        for (int j = 1; j <= SIZE; j++) {
            int cell = map[i][j];
            
            if (cell > 20) {
                // 已标记
                printf(" F ");
            } else if (cell > 9) {
                // 已翻开
                int num = cell - 10;
                if (num == 0) {
                    printf(" . ");
                } else {
                    printf(" %d ", num);
                }
            } else {
                // 未翻开
                printf(" # ");
            }
        }
        printf("\n");
    }
    printf("========================================\n");
    printf("操作说明:\n");
    printf("输入格式: 行 列 操作 (操作: 1=翻开, 0=标记, q=退出)\n");
    printf("例如: 3 5 1 表示翻开第3行第5列\n");
    printf("========================================\n");
}

// 翻开格子
int reveal_cell(int x, int y) {
    if (x < 1 || x > SIZE || y < 1 || y > SIZE) return 0;
    if (map[x][y] > 9 && map[x][y] <= 20) return 0; // 已翻开
    if (map[x][y] > 20) {
        // 已标记，先取消标记再翻开
        map[x][y] -= 30;
        mines_remaining++;
    }
    
    if (map[x][y] == -1) {
        game_over = 1;
        return 1;
    }
    
    map[x][y] += 10;
    cells_revealed++;
    
    // 如果是0，递归翻开周围格子
    if (map[x][y] == 10) {
        for (int di = -1; di <= 1; di++) {
            for (int dj = -1; dj <= 1; dj++) {
                reveal_cell(x + di, y + dj);
            }
        }
    }
    
    return 0;
}

// 标记格子
void mark_cell(int x, int y) {
    if (x < 1 || x > SIZE || y < 1 || y > SIZE) return;
    if (map[x][y] > 9) return; // 已翻开
    
    if (map[x][y] > 20) {
        map[x][y] -= 30;
        mines_remaining++;
    } else {
        map[x][y] += 30;
        mines_remaining--;
    }
}

// 检查是否胜利
int check_win() {
    int total_cells = SIZE * SIZE;
    int safe_cells = total_cells - mines_count;
    return cells_revealed == safe_cells;
}

// 开始游戏
void play_game() {
    int difficulty = get_difficulty();
    int rows = SIZE, cols = SIZE, mines = 10;
    
    switch (difficulty) {
        case 1: rows = 9; cols = 9; mines = 10; break;
        case 2: rows = SIZE; cols = SIZE; mines = 10; break;
        case 3: rows = 16; cols = 16; mines = 40; break;
    }
    
    game_init(rows, cols, mines);
    mines_count = mines;
    
    start_time = time(NULL);
    
    while (!game_over && !game_won) {
        draw_map();
        
        int x, y, op;
        char input[100];
        
        printf("请输入操作: ");
        fgets(input, sizeof(input), stdin);
        
        if (input[0] == 'q' || input[0] == 'Q') {
            printf("\n游戏已退出！按任意键继续...\n");
            getch();
            return;
        }
        
        if (sscanf(input, "%d %d %d", &x, &y, &op) == 3) {
            if (op == 1) {
                if (reveal_cell(x, y) == 1) {
                    game_over = 1;
                }
            } else if (op == 0) {
                mark_cell(x, y);
            }
        }
        
        if (check_win()) {
            game_won = 1;
        }
    }
    
    // 显示结果
    system("cls");
    printf("========================================\n");
    if (game_won) {
        time_t elapsed = time(NULL) - start_time;
        printf("          恭喜你胜利了！\n");
        printf("          用时: %lld秒\n", (long long)elapsed);
        save_score((int)elapsed);
    } else {
        printf("           游戏结束！\n");
        printf("           你踩到了雷！\n");
    }
    printf("========================================\n");
    printf("\n按任意键继续...\n");
    getch();
}

// 获取难度
int get_difficulty() {
    int choice;
    printf("\n选择难度:\n");
    printf("1. 简单 (9x9, 10雷)\n");
    printf("2. 中等 (10x10, 10雷)\n");
    printf("3. 困难 (16x16, 40雷)\n");
    printf("请选择: ");
    scanf("%d", &choice);
    getchar();
    return choice;
}

// 游戏说明
void print_instructions() {
    system("cls");
    printf("========================================\n");
    printf("            游戏说明\n");
    printf("========================================\n");
    printf("1. 游戏目标：找出所有没有地雷的格子\n");
    printf("2. 操作方式：\n");
    printf("   - 输入 行 列 1 来翻开格子\n");
    printf("   - 输入 行 列 0 来标记地雷\n");
    printf("   - 输入 q 退出游戏\n");
    printf("3. 数字含义：翻开格子上的数字表示\n");
    printf("   周围8个格子中有多少个地雷\n");
    printf("4. 如果翻开的是地雷，游戏结束\n");
    printf("5. 标记所有地雷并翻开安全格子即为胜利\n");
    printf("========================================\n");
    printf("\n按任意键继续...\n");
    getch();
}

// 加载用户数据
void load_users() {
    FILE* fp = fopen(USER_FILE, "r");
    if (fp == NULL) return;
    
    user_count = 0;
    char line[200];
    while (fgets(line, sizeof(line), fp) != NULL && user_count < MAX_USERS) {
        char name[MAX_NAME], pass[MAX_PASS];
        int time;
        if (sscanf(line, "%s %s %d", name, pass, &time) == 3) {
            strcpy(users[user_count].name, name);
            strcpy(users[user_count].pass, pass);
            users[user_count].best_time = time;
            user_count++;
        }
    }
    fclose(fp);
}

// 保存用户数据
void save_users() {
    FILE* fp = fopen(USER_FILE, "w");
    if (fp == NULL) return;
    
    for (int i = 0; i < user_count; i++) {
        fprintf(fp, "%s %s %d\n", users[i].name, users[i].pass, users[i].best_time);
    }
    fclose(fp);
}

// 保存成绩
void save_score(int time_used) {
    // 更新当前用户最佳成绩
    for (int i = 0; i < user_count; i++) {
        if (strcmp(users[i].name, current_user.name) == 0) {
            if (users[i].best_time == -1 || time_used < users[i].best_time) {
                users[i].best_time = time_used;
            }
            break;
        }
    }
    save_users();
    
    // 保存到排行榜
    FILE* fp = fopen(RANK_FILE, "a");
    if (fp != NULL) {
        fprintf(fp, "%s %d\n", current_user.name, time_used);
        fclose(fp);
    }
}

// 显示排行榜
void display_rankings() {
    system("cls");
    printf("========================================\n");
    printf("            排行榜\n");
    printf("========================================\n");
    
    // 显示用户最佳成绩
    printf("\n用户最佳成绩:\n");
    printf("排名\t用户名\t最佳时间\n");
    printf("----------------------------------------\n");
    
    User sorted[MAX_USERS];
    for (int i = 0; i < user_count; i++) sorted[i] = users[i];
    
    // 按最佳成绩排序
    for (int i = 0; i < user_count - 1; i++) {
        for (int j = i + 1; j < user_count; j++) {
            if (sorted[i].best_time == -1 || 
                (sorted[j].best_time != -1 && sorted[j].best_time < sorted[i].best_time)) {
                User temp = sorted[i];
                sorted[i] = sorted[j];
                sorted[j] = temp;
            }
        }
    }
    
    int rank = 1;
    for (int i = 0; i < user_count; i++) {
        if (sorted[i].best_time != -1) {
            printf("%d\t%s\t%d秒\n", rank, sorted[i].name, sorted[i].best_time);
            rank++;
        }
    }
    
    if (rank == 1) {
        printf("暂无记录\n");
    }
    
    printf("========================================\n");
    printf("\n按任意键继续...\n");
    getch();
}

// 主函数
int main() {
    // 创建数据目录
    CreateDirectory("../dataset", NULL);
    
    // 加载用户数据
    load_users();
    
    while (1) {
        print_menu();
        int choice;
        scanf("%d", &choice);
        getchar();
        
        switch (choice) {
            case 1:
                register_user();
                break;
            case 2:
                if (login_user()) {
                    // 进入游戏菜单
                    while (1) {
                        print_game_menu();
                        int game_choice;
                        scanf("%d", &game_choice);
                        getchar();
                        
                        switch (game_choice) {
                            case 1:
                                play_game();
                                break;
                            case 2:
                                display_rankings();
                                break;
                            case 3:
                                print_instructions();
                                break;
                            case 4:
                                goto main_menu;
                            default:
                                printf("无效选择！按任意键继续...\n");
                                getch();
                        }
                    }
                }
                break;
            case 3:
                print_instructions();
                break;
            case 0:
                printf("\n感谢使用扫雷游戏系统！\n");
                return 0;
            default:
                printf("无效选择！按任意键继续...\n");
                getch();
        }
        main_menu:;
    }
    
    return 0;
}
