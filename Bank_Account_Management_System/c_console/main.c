#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>

#define MAX_ACCOUNTS 1000
#define MAX_NAME_LEN 50
#define MAX_ID_LEN 20
#define MAX_DATE_LEN 11
#define PASSWORD_FILE "../dataset/password.txt"
#define BASIC_FILE "../dataset/AccountBasic.txt"
#define BALANCE_FILE "../dataset/AccountBalance.txt"

/* 账户基本信息结构体 */
typedef struct {
    int account_no;
    char name[MAX_NAME_LEN];
    char id_card[MAX_ID_LEN];
    char create_date[MAX_DATE_LEN];
} AccountBasic;

/* 账户余额结构体 */
typedef struct {
    int account_no;
    double balance;
} AccountBalance;

/* 全局变量 */
AccountBasic basics[MAX_ACCOUNTS];
AccountBalance balances[MAX_ACCOUNTS];
int account_count = 0;
int next_account_no = 10001;

/* 函数声明 */
int verify_password(void);
void load_data(void);
void save_data(void);
void show_menu(void);
void open_account(void);
void borrow_money(void);
void repay_money(void);
void deposit_money(void);
void delete_account(void);
void compact_files(void);
void query_account(void);
void query_max_borrower(void);
void query_max_depositor(void);
void sort_by_borrow(void);
void sort_by_deposit(void);
void sort_by_date(void);
void show_statistics(void);
void check_warning_accounts(void);
int validate_id_card(const char *id_card);
int validate_date(const char *date);
void print_separator(void);
void clear_screen(void);
void pause_screen(void);

/* 主函数 */
int main(void) {
    char input[10];

    /* 密码验证 */
    if (!verify_password()) {
        printf("\n密码验证失败，程序退出！\n");
        pause_screen();
        return 0;
    }

    /* 加载数据 */
    load_data();

    /* 检查预警账户 */
    check_warning_accounts();

    /* 主循环 */
    while (1) {
        clear_screen();
        show_menu();
        printf("\n请选择功能（0-9, A-D）：");
        scanf("%s", input);
        getchar(); /* 清除输入缓冲区 */

        if (strlen(input) == 1) {
            char choice = toupper(input[0]);

            switch (choice) {
                case '1':
                    open_account();
                    break;
                case '2':
                    borrow_money();
                    break;
                case '3':
                    repay_money();
                    break;
                case '4':
                    deposit_money();
                    break;
                case '5':
                    query_account();
                    break;
                case '6':
                    query_max_borrower();
                    break;
                case '7':
                    query_max_depositor();
                    break;
                case '8':
                    sort_by_borrow();
                    break;
                case '9':
                    sort_by_deposit();
                    break;
                case 'A':
                    sort_by_date();
                    break;
                case 'B':
                    delete_account();
                    break;
                case 'C':
                    compact_files();
                    break;
                case 'D':
                    show_statistics();
                    break;
                case '0':
                    save_data();
                    printf("\n数据已保存，感谢使用！\n");
                    pause_screen();
                    return 0;
                default:
                    printf("\n无效的选择，请重新输入！\n");
                    pause_screen();
            }
        } else {
            printf("\n无效的选择，请重新输入！\n");
            pause_screen();
        }
    }

    return 0;
}

/* 密码验证 */
int verify_password(void) {
    FILE *fp;
    char stored_password[50];
    char input_password[50];
    int attempts = 0;
    int result = 0;

    /* 读取存储的密码 */
    fp = fopen(PASSWORD_FILE, "r");
    if (fp == NULL) {
        printf("无法打开密码文件！\n");
        return 0;
    }
    fscanf(fp, "%s", stored_password);
    fclose(fp);

    printf("\n========================================\n");
    printf("          银行账目管理系统\n");
    printf("========================================\n\n");

    /* 允许三次尝试 */
    while (attempts < 3) {
        printf("请输入密码（还剩 %d 次机会）：", 3 - attempts);
        scanf("%s", input_password);
        getchar();

        if (strcmp(input_password, stored_password) == 0) {
            printf("\n登录成功！\n");
            result = 1;
            break;
        } else {
            printf("密码错误！\n");
            attempts++;
        }
    }

    return result;
}

/* 加载数据 */
void load_data(void) {
    FILE *fp_basic, *fp_balance;
    char line[200];

    /* 加载基本信息 */
    fp_basic = fopen(BASIC_FILE, "rb");
    if (fp_basic == NULL) {
        printf("无法打开账户基本信息文件！\n");
        printf("请确认文件路径：%s\n", BASIC_FILE);
        return;
    }

    account_count = 0;
    while (fgets(line, sizeof(line), fp_basic) != NULL && account_count < MAX_ACCOUNTS) {
        /* 去除行尾符 (处理 \r\n 或 \n) */
        size_t len = strlen(line);
        if (len > 0 && line[len - 1] == '\n') {
            line[len - 1] = '\0';
            if (len > 1 && line[len - 2] == '\r') {
                line[len - 2] = '\0';
            }
        }
        if (strlen(line) == 0) continue;

        char *token = strtok(line, "|");
        if (token != NULL) {
            basics[account_count].account_no = atoi(token);
            token = strtok(NULL, "|");
            if (token != NULL) strcpy(basics[account_count].name, token);
            token = strtok(NULL, "|");
            if (token != NULL) strcpy(basics[account_count].id_card, token);
            token = strtok(NULL, "|");
            if (token != NULL) strcpy(basics[account_count].create_date, token);

            if (basics[account_count].account_no >= next_account_no) {
                next_account_no = basics[account_count].account_no + 1;
            }

            account_count++;
        }
    }
    fclose(fp_basic);

    /* 加载余额信息 */
    fp_balance = fopen(BALANCE_FILE, "rb");
    if (fp_balance == NULL) {
        printf("无法打开账户余额文件！\n");
        return;
    }

    while (fgets(line, sizeof(line), fp_balance) != NULL) {
        /* 去除行尾符 (处理 \r\n 或 \n) */
        size_t len = strlen(line);
        if (len > 0 && line[len - 1] == '\n') {
            line[len - 1] = '\0';
            if (len > 1 && line[len - 2] == '\r') {
                line[len - 2] = '\0';
            }
        }
        if (strlen(line) == 0) continue;

        char *token = strtok(line, "|");
        if (token != NULL) {
            int account_no = atoi(token);
            token = strtok(NULL, "|");
            if (token != NULL) {
                double balance = atof(token);

                /* 查找对应的账户并更新余额 */
                for (int i = 0; i < account_count; i++) {
                    if (basics[i].account_no == account_no) {
                        balances[i].account_no = account_no;
                        balances[i].balance = balance;
                        break;
                    }
                }
            }
        }
    }
    fclose(fp_balance);
}

/* 保存数据 */
void save_data(void) {
    FILE *fp_basic, *fp_balance;
    int i;

    /* 保存基本信息 (使用二进制模式保持原行尾格式) */
    fp_basic = fopen(BASIC_FILE, "wb");
    if (fp_basic == NULL) {
        printf("无法保存账户基本信息文件！\n");
        return;
    }

    for (i = 0; i < account_count; i++) {
        fprintf(fp_basic, "%d|%s|%s|%s\r\n",
                basics[i].account_no,
                basics[i].name,
                basics[i].id_card,
                basics[i].create_date);
    }
    fclose(fp_basic);

    /* 保存余额信息 */
    fp_balance = fopen(BALANCE_FILE, "wb");
    if (fp_balance == NULL) {
        printf("无法保存账户余额文件！\n");
        return;
    }

    for (i = 0; i < account_count; i++) {
        fprintf(fp_balance, "%d|%.2f\r\n",
                balances[i].account_no,
                balances[i].balance);
    }
    fclose(fp_balance);
}

/* 显示菜单 */
void show_menu(void) {
    printf("========================================\n");
    printf("          银行账目管理系统\n");
    printf("========================================\n");
    printf("1. 开户\n");
    printf("2. 借款\n");
    printf("3. 还款\n");
    printf("4. 存款\n");
    printf("5. 查询账户\n");
    printf("6. 查询最大借款账户\n");
    printf("7. 查询最大存款账户\n");
    printf("8. 按借款余额排序\n");
    printf("9. 按存款余额排序\n");
    printf("A. 按开户日期排序\n");
    printf("B. 清户\n");
    printf("C. 文件紧缩\n");
    printf("D. 统计信息\n");
    printf("0. 退出\n");
    printf("========================================\n");
}

/* 开户 */
void open_account(void) {
    char name[MAX_NAME_LEN];
    char id_card[MAX_ID_LEN];
    char date[MAX_DATE_LEN];
    double amount;

    printf("\n=== 开户 ===\n");

    printf("请输入姓名：");
    fgets(name, sizeof(name), stdin);
    name[strcspn(name, "\n")] = '\0';

    /* 验证身份证号 */
    while (1) {
        printf("请输入身份证号：");
        fgets(id_card, sizeof(id_card), stdin);
        id_card[strcspn(id_card, "\n")] = '\0';

        if (validate_id_card(id_card)) {
            break;
        }
        printf("身份证号格式不正确，请重新输入！\n");
    }

    /* 验证日期 */
    while (1) {
        printf("请输入开户日期（YYYY-MM-DD）：");
        fgets(date, sizeof(date), stdin);
        date[strcspn(date, "\n")] = '\0';

        if (validate_date(date)) {
            break;
        }
        printf("日期格式不正确，请重新输入！\n");
    }

    printf("请输入开户金额：");
    scanf("%lf", &amount);
    getchar();

    /* 添加账户 */
    if (account_count >= MAX_ACCOUNTS) {
        printf("账户数量已达上限！\n");
        pause_screen();
        return;
    }

    basics[account_count].account_no = next_account_no;
    strcpy(basics[account_count].name, name);
    strcpy(basics[account_count].id_card, id_card);
    strcpy(basics[account_count].create_date, date);

    balances[account_count].account_no = next_account_no;
    balances[account_count].balance = amount;

    printf("\n开户成功！\n");
    printf("账号：%d\n", next_account_no);
    printf("余额：%.2f\n", amount);

    next_account_no++;
    account_count++;

    save_data();
    pause_screen();
}

/* 借款 */
void borrow_money(void) {
    int account_no;
    double amount;
    int i;

    printf("\n=== 借款 ===\n");

    printf("请输入账号：");
    scanf("%d", &account_no);
    getchar();

    /* 查找账户 */
    for (i = 0; i < account_count; i++) {
        if (basics[i].account_no == account_no) {
            printf("请输入借款金额：");
            scanf("%lf", &amount);
            getchar();

            if (amount <= 0) {
                printf("借款金额必须大于0！\n");
                pause_screen();
                return;
            }

            balances[i].balance -= amount;
            printf("\n借款成功！\n");
            printf("账号：%d\n", account_no);
            printf("当前余额：%.2f\n", balances[i].balance);

            save_data();
            pause_screen();
            return;
        }
    }

    printf("未找到该账户！\n");
    pause_screen();
}

/* 还款 */
void repay_money(void) {
    int account_no;
    double amount;
    int i;

    printf("\n=== 还款 ===\n");

    printf("请输入账号：");
    scanf("%d", &account_no);
    getchar();

    /* 查找账户 */
    for (i = 0; i < account_count; i++) {
        if (basics[i].account_no == account_no) {
            printf("当前余额：%.2f\n", balances[i].balance);

            printf("请输入还款金额：");
            scanf("%lf", &amount);
            getchar();

            if (amount <= 0) {
                printf("还款金额必须大于0！\n");
                pause_screen();
                return;
            }

            if (balances[i].balance + amount > 0) {
                printf("还款金额超过借款额！\n");
                pause_screen();
                return;
            }

            balances[i].balance += amount;
            printf("\n还款成功！\n");
            printf("账号：%d\n", account_no);
            printf("当前余额：%.2f\n", balances[i].balance);

            save_data();
            pause_screen();
            return;
        }
    }

    printf("未找到该账户！\n");
    pause_screen();
}

/* 存款 */
void deposit_money(void) {
    int account_no;
    double amount;
    int i;

    printf("\n=== 存款 ===\n");

    printf("请输入账号：");
    scanf("%d", &account_no);
    getchar();

    /* 查找账户 */
    for (i = 0; i < account_count; i++) {
        if (basics[i].account_no == account_no) {
            printf("请输入存款金额：");
            scanf("%lf", &amount);
            getchar();

            if (amount <= 0) {
                printf("存款金额必须大于0！\n");
                pause_screen();
                return;
            }

            balances[i].balance += amount;
            printf("\n存款成功！\n");
            printf("账号：%d\n", account_no);
            printf("当前余额：%.2f\n", balances[i].balance);

            save_data();
            pause_screen();
            return;
        }
    }

    printf("未找到该账户！\n");
    pause_screen();
}

/* 查询账户 */
void query_account(void) {
    int account_no;
    int i;

    printf("\n=== 查询账户 ===\n");

    printf("请输入账号：");
    scanf("%d", &account_no);
    getchar();

    /* 查找账户 */
    for (i = 0; i < account_count; i++) {
        if (basics[i].account_no == account_no) {
            printf("\n账户信息：\n");
            printf("账号：%d\n", basics[i].account_no);
            printf("姓名：%s\n", basics[i].name);
            printf("身份证号：%s\n", basics[i].id_card);
            printf("开户日期：%s\n", basics[i].create_date);
            printf("当前余额：%.2f\n", balances[i].balance);

            pause_screen();
            return;
        }
    }

    printf("未找到该账户！\n");
    pause_screen();
}

/* 查询最大借款账户 */
void query_max_borrower(void) {
    int max_index = -1;
    double max_borrow = 0;
    int i;

    printf("\n=== 查询最大借款账户 ===\n");

    for (i = 0; i < account_count; i++) {
        if (balances[i].balance < 0) {
            if (balances[i].balance < max_borrow) {
                max_borrow = balances[i].balance;
                max_index = i;
            }
        }
    }

    if (max_index == -1) {
        printf("没有借款账户！\n");
    } else {
        printf("\n最大借款账户信息：\n");
        printf("账号：%d\n", basics[max_index].account_no);
        printf("姓名：%s\n", basics[max_index].name);
        printf("身份证号：%s\n", basics[max_index].id_card);
        printf("开户日期：%s\n", basics[max_index].create_date);
        printf("当前余额：%.2f\n", balances[max_index].balance);
        printf("借款金额：%.2f\n", -balances[max_index].balance);
    }

    pause_screen();
}

/* 查询最大存款账户 */
void query_max_depositor(void) {
    int max_index = -1;
    double max_deposit = 0;
    int i;

    printf("\n=== 查询最大存款账户 ===\n");

    for (i = 0; i < account_count; i++) {
        if (balances[i].balance > 0) {
            if (balances[i].balance > max_deposit) {
                max_deposit = balances[i].balance;
                max_index = i;
            }
        }
    }

    if (max_index == -1) {
        printf("没有存款账户！\n");
    } else {
        printf("\n最大存款账户信息：\n");
        printf("账号：%d\n", basics[max_index].account_no);
        printf("姓名：%s\n", basics[max_index].name);
        printf("身份证号：%s\n", basics[max_index].id_card);
        printf("开户日期：%s\n", basics[max_index].create_date);
        printf("当前余额：%.2f\n", balances[max_index].balance);
    }

    pause_screen();
}

/* 按借款余额排序 */
void sort_by_borrow(void) {
    int indices[MAX_ACCOUNTS];
    int count = 0;
    int i, j, temp;

    printf("\n=== 按借款余额排序（从大到小） ===\n");

    /* 筛选借款账户 */
    for (i = 0; i < account_count; i++) {
        if (balances[i].balance < 0) {
            indices[count] = i;
            count++;
        }
    }

    if (count == 0) {
        printf("没有借款账户！\n");
        pause_screen();
        return;
    }

    /* 冒泡排序（从大到小，即从-1、-2、-100等接近0的在前） */
    for (i = 0; i < count - 1; i++) {
        for (j = 0; j < count - 1 - i; j++) {
            if (balances[indices[j]].balance < balances[indices[j + 1]].balance) {
                temp = indices[j];
                indices[j] = indices[j + 1];
                indices[j + 1] = temp;
            }
        }
    }

    /* 输出结果 */
    printf("\n%-8s %-10s %-15s\n", "账号", "姓名", "借款金额");
    print_separator();

    for (i = 0; i < count; i++) {
        int idx = indices[i];
        printf("%-8d %-10s %-15.2f\n",
               basics[idx].account_no,
               basics[idx].name,
               -balances[idx].balance);
    }

    pause_screen();
}

/* 按存款余额排序 */
void sort_by_deposit(void) {
    int indices[MAX_ACCOUNTS];
    int count = 0;
    int i, j, temp;

    printf("\n=== 按存款余额排序（从大到小） ===\n");

    /* 筛选存款账户 */
    for (i = 0; i < account_count; i++) {
        if (balances[i].balance > 0) {
            indices[count] = i;
            count++;
        }
    }

    if (count == 0) {
        printf("没有存款账户！\n");
        pause_screen();
        return;
    }

    /* 冒泡排序（从大到小） */
    for (i = 0; i < count - 1; i++) {
        for (j = 0; j < count - 1 - i; j++) {
            if (balances[indices[j]].balance < balances[indices[j + 1]].balance) {
                temp = indices[j];
                indices[j] = indices[j + 1];
                indices[j + 1] = temp;
            }
        }
    }

    /* 输出结果 */
    printf("\n%-8s %-10s %-15s\n", "账号", "姓名", "存款金额");
    print_separator();

    for (i = 0; i < count; i++) {
        int idx = indices[i];
        printf("%-8d %-10s %-15.2f\n",
               basics[idx].account_no,
               basics[idx].name,
               balances[idx].balance);
    }

    pause_screen();
}

/* 按开户日期排序 */
void sort_by_date(void) {
    int indices[MAX_ACCOUNTS];
    int count = 0;
    int i, j, temp;

    printf("\n=== 按开户日期排序（从小到大） ===\n");

    /* 筛选所有有效账户 */
    for (i = 0; i < account_count; i++) {
        if (basics[i].account_no != -1) {
            indices[count] = i;
            count++;
        }
    }

    if (count == 0) {
        printf("没有有效账户！\n");
        pause_screen();
        return;
    }

    /* 冒泡排序（从小到大） */
    for (i = 0; i < count - 1; i++) {
        for (j = 0; j < count - 1 - i; j++) {
            if (strcmp(basics[indices[j]].create_date, basics[indices[j + 1]].create_date) > 0) {
                temp = indices[j];
                indices[j] = indices[j + 1];
                indices[j + 1] = temp;
            }
        }
    }

    /* 输出结果 */
    printf("\n%-8s %-10s %-15s %-12s\n", "账号", "姓名", "身份证号", "开户日期");
    print_separator();

    for (i = 0; i < count; i++) {
        int idx = indices[i];
        printf("%-8d %-10s %-15s %-12s\n",
               basics[idx].account_no,
               basics[idx].name,
               basics[idx].id_card,
               basics[idx].create_date);
    }

    pause_screen();
}

/* 清户 */
void delete_account(void) {
    int account_no;
    int i;

    printf("\n=== 清户 ===\n");

    printf("请输入要删除的账号：");
    scanf("%d", &account_no);
    getchar();

    /* 查找账户 */
    for (i = 0; i < account_count; i++) {
        if (basics[i].account_no == account_no) {
            printf("\n账户信息：\n");
            printf("账号：%d\n", basics[i].account_no);
            printf("姓名：%s\n", basics[i].name);
            printf("身份证号：%s\n", basics[i].id_card);
            printf("开户日期：%s\n", basics[i].create_date);
            printf("当前余额：%.2f\n", balances[i].balance);

            printf("\n确认删除该账户？(y/n)：");
            char confirm;
            scanf("%c", &confirm);
            getchar();

            if (confirm == 'y' || confirm == 'Y') {
                /* 将账号置为 -1（逻辑删除） */
                basics[i].account_no = -1;
                balances[i].account_no = -1;
                printf("\n账户已删除（逻辑删除）！\n");
                printf("提示：请使用'文件紧缩'功能清除已删除账户。\n");
            } else {
                printf("\n取消删除！\n");
            }

            pause_screen();
            return;
        }
    }

    printf("未找到该账户！\n");
    pause_screen();
}

/* 文件紧缩 */
void compact_files(void) {
    int i, j;
    int original_count = account_count;

    printf("\n=== 文件紧缩 ===\n");

    /* 移除账号为 -1 的记录 */
    j = 0;
    for (i = 0; i < account_count; i++) {
        if (basics[i].account_no != -1) {
            if (i != j) {
                basics[j] = basics[i];
                balances[j] = balances[i];
            }
            j++;
        }
    }

    account_count = j;

    printf("\n文件紧缩完成！\n");
    printf("原账户数：%d\n", original_count);
    printf("现账户数：%d\n", account_count);
    printf("删除账户数：%d\n", original_count - account_count);

    save_data();
    pause_screen();
}

/* 统计信息 */
void show_statistics(void) {
    int i;
    int borrow_count = 0;
    int deposit_count = 0;
    double total_borrow = 0;
    double total_deposit = 0;

    printf("\n=== 统计信息 ===\n");

    for (i = 0; i < account_count; i++) {
        if (balances[i].balance < 0) {
            borrow_count++;
            total_borrow += -balances[i].balance;
        } else if (balances[i].balance > 0) {
            deposit_count++;
            total_deposit += balances[i].balance;
        }
    }

    printf("\n当前账户个数：%d\n", account_count);
    printf("借款账户数：%d\n", borrow_count);
    printf("存款账户数：%d\n", deposit_count);
    printf("当前借款总额：%.2f 元\n", total_borrow);
    printf("当前存款总额：%.2f 元\n", total_deposit);
    printf("借款总额与存款总额的差额：%.2f 元\n", total_deposit - total_borrow);

    pause_screen();
}

/* 检查预警账户 */
void check_warning_accounts(void) {
    int i;
    int warning_count = 0;

    printf("\n正在检查借款超额账户...\n");

    for (i = 0; i < account_count; i++) {
        if (balances[i].balance < -50000) {
            printf("\n【预警】账号 %d（%s）借款额超过5万元！\n",
                   basics[i].account_no,
                   basics[i].name);
            printf("当前借款额：%.2f 元\n", -balances[i].balance);
            warning_count++;
        }
    }

    if (warning_count == 0) {
        printf("无借款超额账户。\n");
    }

    pause_screen();
}

/* 验证身份证号 */
int validate_id_card(const char *id_card) {
    int len = strlen(id_card);

    /* 检查长度（18位） */
    if (len != 18) {
        return 0;
    }

    /* 检查前17位是否为数字 */
    for (int i = 0; i < 17; i++) {
        if (!isdigit(id_card[i])) {
            return 0;
        }
    }

    /* 检查第18位是否为数字或X */
    if (!isdigit(id_card[17]) && toupper(id_card[17]) != 'X') {
        return 0;
    }

    return 1;
}

/* 验证日期 */
int validate_date(const char *date) {
    int year, month, day;
    int days_in_month[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    /* 检查格式 YYYY-MM-DD */
    if (strlen(date) != 10) {
        return 0;
    }

    if (date[4] != '-' || date[7] != '-') {
        return 0;
    }

    /* 检查各部分是否为数字 */
    for (int i = 0; i < 10; i++) {
        if (i == 4 || i == 7) continue;
        if (!isdigit(date[i])) {
            return 0;
        }
    }

    /* 解析日期 */
    sscanf(date, "%d-%d-%d", &year, &month, &day);

    /* 检查年份范围 */
    if (year < 1900 || year > 2100) {
        return 0;
    }

    /* 检查月份范围 */
    if (month < 1 || month > 12) {
        return 0;
    }

    /* 检查闰年二月 */
    if ((year % 400 == 0) || (year % 100 != 0 && year % 4 == 0)) {
        days_in_month[1] = 29;
    }

    /* 检查日期范围 */
    if (day < 1 || day > days_in_month[month - 1]) {
        return 0;
    }

    return 1;
}

/* 打印分隔线 */
void print_separator(void) {
    printf("----------------------------------------\n");
}

/* 清屏 */
void clear_screen(void) {
    system("cls");
}

/* 暂停 */
void pause_screen(void) {
    printf("\n按回车键继续...");
    getchar();
}
