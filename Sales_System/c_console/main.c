/*
 * 销售系统 - C语言控制台版
 * 功能：管理员、店长、销售员三种角色的销售管理系统
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

#define MAX_USERS 100
#define MAX_PRODUCTS 100
#define MAX_SALES 1000
#define MAX_NAME_LEN 50
#define MAX_PASSWORD_LEN 50
#define MAX_DATE_LEN 11

/* 文件路径 */
#define PASSWORD_FILE "../dataset/password.txt"
#define USERS_FILE "../dataset/users.txt"
#define PRODUCTS_FILE "../dataset/products.txt"
#define SALES_FILE "../dataset/sales.txt"

/* 用户结构体 */
typedef struct {
    int id;
    char username[MAX_NAME_LEN];
    char password[MAX_PASSWORD_LEN];
    int role;  /* 1-管理员, 2-店长, 3-销售员 */
} User;

/* 商品结构体 */
typedef struct {
    int id;
    char name[MAX_NAME_LEN];
    double price;
    int stock;
} Product;

/* 销售记录结构体 */
typedef struct {
    int id;
    int product_id;
    char product_name[MAX_NAME_LEN];
    int quantity;
    double unit_price;
    double total_amount;
    char date[MAX_DATE_LEN];
    int seller_id;
} Sale;

/* 全局变量 */
User users[MAX_USERS];
Product products[MAX_PRODUCTS];
Sale sales[MAX_SALES];
int user_count = 0;
int product_count = 0;
int sale_count = 0;
int current_user_id = 0;
int current_role = 0;

/* 函数声明 */
void clear_screen(void);
void pause_screen(void);
void print_separator(void);
int verify_password(void);
void load_data(void);
void save_data(void);

void show_menu(void);
void modify_password(void);
void manage_users(void);
void manage_products(void);
void browse_products(void);
void sell_product(void);
void show_daily_report(void);
void show_monthly_report(void);
void show_product_sales_report(void);
void show_seller_performance_report(void);

/* 主函数 */
int main(void) {
    char input[10];

    /* 加载数据 */
    load_data();

    /* 密码验证 */
    if (!verify_password()) {
        printf("\n密码验证失败，程序退出！\n");
        pause_screen();
        return 0;
    }

    /* 主循环 */
    while (1) {
        clear_screen();
        show_menu();
        printf("\n请选择功能（0-8）：");
        scanf("%s", input);
        getchar(); /* 清除输入缓冲区 */

        if (strlen(input) == 1) {
            char choice = toupper(input[0]);

            switch (choice) {
                case '1':
                    modify_password();
                    break;
                case '2':
                    if (current_role == 1) {
                        manage_users();
                    } else {
                        printf("\n权限不足！只有管理员可以管理用户。\n");
                        pause_screen();
                    }
                    break;
                case '3':
                    if (current_role == 3) {
                        browse_products();
                    } else if (current_role == 1 || current_role == 2) {
                        manage_products();
                    }
                    break;
                case '4':
                    if (current_role == 3) {
                        sell_product();
                    } else {
                        printf("\n权限不足！只有销售员可以销售商品。\n");
                        pause_screen();
                    }
                    break;
                case '5':
                    show_daily_report();
                    break;
                case '6':
                    show_monthly_report();
                    break;
                case '7':
                    if (current_role == 1 || current_role == 2) {
                        show_product_sales_report();
                    } else {
                        printf("\n权限不足！只有管理员和店长可以查看商品销售报表。\n");
                        pause_screen();
                    }
                    break;
                case '8':
                    if (current_role == 1 || current_role == 2) {
                        show_seller_performance_report();
                    } else {
                        printf("\n权限不足！只有管理员和店长可以查看销售员业绩报表。\n");
                        pause_screen();
                    }
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

/* 清屏 */
void clear_screen(void) {
    system("cls");
}

/* 暂停 */
void pause_screen(void) {
    printf("\n按回车键继续...");
    getchar();
}

/* 打印分隔线 */
void print_separator(void) {
    printf("----------------------------------------\n");
}

/* 密码验证 */
int verify_password(void) {
    FILE *fp;
    char stored_password[50];
    char input_password[50];
    int attempts = 0;
    int result = 0;

    /* 读取存储的密码 */
    fp = fopen(PASSWORD_FILE, "rb");
    if (fp == NULL) {
        printf("无法打开密码文件！\n");
        return 0;
    }

    char line[256];
    if (fgets(line, sizeof(line), fp) != NULL) {
        /* 去除行尾符 (处理 \r\n 和 \n) */
        size_t len = strlen(line);
        if (len > 0 && line[len - 1] == '\n') {
            line[len - 1] = '\0';
            if (len > 1 && line[len - 2] == '\r') {
                line[len - 2] = '\0';
            }
        }
        strcpy(stored_password, line);
    }
    fclose(fp);

    printf("\n========================================\n");
    printf("          销售系统\n");
    printf("========================================\n\n");

    /* 用户登录 */
    char username[MAX_NAME_LEN];
    printf("请输入用户名：");
    fgets(username, sizeof(username), stdin);
    username[strcspn(username, "\n")] = '\0';

    /* 查找用户 */
    int found = 0;
    for (int i = 0; i < user_count; i++) {
        if (strcmp(users[i].username, username) == 0) {
            current_user_id = users[i].id;
            current_role = users[i].role;
            strcpy(stored_password, users[i].password);
            found = 1;
            break;
        }
    }

    if (!found) {
        printf("\n用户不存在！\n");
        return 0;
    }

    /* 验证密码 */
    while (attempts < 3) {
        printf("请输入密码（还剩 %d 次机会）：", 3 - attempts);
        fgets(input_password, sizeof(input_password), stdin);
        input_password[strcspn(input_password, "\n")] = '\0';

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
    FILE *fp_users, *fp_products, *fp_sales;
    char line[256];

    /* 加载用户数据 */
    fp_users = fopen(USERS_FILE, "rb");
    if (fp_users != NULL) {
        while (fgets(line, sizeof(line), fp_users) != NULL && user_count < MAX_USERS) {
            /* 去除行尾符 */
            size_t len = strlen(line);
            if (len > 0 && line[len - 1] == '\n') {
                line[len - 1] = '\0';
                if (len > 1 && line[len - 2] == '\r') {
                    line[len - 2] = '\0';
                }
            }
            if (strlen(line) == 0) continue;

            char *token = strtok(line, "|");
            if (token) {
                users[user_count].id = atoi(token);
                token = strtok(NULL, "|");
                if (token) strcpy(users[user_count].username, token);
                token = strtok(NULL, "|");
                if (token) strcpy(users[user_count].password, token);
                token = strtok(NULL, "|");
                if (token) users[user_count].role = atoi(token);
                user_count++;
            }
        }
        fclose(fp_users);
    }

    /* 加载商品数据 */
    fp_products = fopen(PRODUCTS_FILE, "rb");
    if (fp_products != NULL) {
        while (fgets(line, sizeof(line), fp_products) != NULL && product_count < MAX_PRODUCTS) {
            size_t len = strlen(line);
            if (len > 0 && line[len - 1] == '\n') {
                line[len - 1] = '\0';
                if (len > 1 && line[len - 2] == '\r') {
                    line[len - 2] = '\0';
                }
            }
            if (strlen(line) == 0) continue;

            char *token = strtok(line, "|");
            if (token) {
                products[product_count].id = atoi(token);
                token = strtok(NULL, "|");
                if (token) strcpy(products[product_count].name, token);
                token = strtok(NULL, "|");
                if (token) products[product_count].price = atof(token);
                token = strtok(NULL, "|");
                if (token) products[product_count].stock = atoi(token);
                product_count++;
            }
        }
        fclose(fp_products);
    }

    /* 加载销售数据 */
    fp_sales = fopen(SALES_FILE, "rb");
    if (fp_sales != NULL) {
        while (fgets(line, sizeof(line), fp_sales) != NULL && sale_count < MAX_SALES) {
            size_t len = strlen(line);
            if (len > 0 && line[len - 1] == '\n') {
                line[len - 1] = '\0';
                if (len > 1 && line[len - 2] == '\r') {
                    line[len - 2] = '\0';
                }
            }
            if (strlen(line) == 0) continue;

            char *token = strtok(line, "|");
            if (token) {
                sales[sale_count].id = atoi(token);
                token = strtok(NULL, "|");
                if (token) sales[sale_count].product_id = atoi(token);
                token = strtok(NULL, "|");
                if (token) strcpy(sales[sale_count].product_name, token);
                token = strtok(NULL, "|");
                if (token) sales[sale_count].quantity = atoi(token);
                token = strtok(NULL, "|");
                if (token) sales[sale_count].unit_price = atof(token);
                token = strtok(NULL, "|");
                if (token) sales[sale_count].total_amount = atof(token);
                token = strtok(NULL, "|");
                if (token) strcpy(sales[sale_count].date, token);
                token = strtok(NULL, "|");
                if (token) sales[sale_count].seller_id = atoi(token);
                sale_count++;
            }
        }
        fclose(fp_sales);
    }
}

/* 保存数据 */
void save_data(void) {
    FILE *fp_users, *fp_products, *fp_sales;
    int i;

    /* 保存用户数据 */
    fp_users = fopen(USERS_FILE, "wb");
    if (fp_users != NULL) {
        for (i = 0; i < user_count; i++) {
            fprintf(fp_users, "%d|%s|%s|%d\r\n",
                    users[i].id,
                    users[i].username,
                    users[i].password,
                    users[i].role);
        }
        fclose(fp_users);
    }

    /* 保存商品数据 */
    fp_products = fopen(PRODUCTS_FILE, "wb");
    if (fp_products != NULL) {
        for (i = 0; i < product_count; i++) {
            fprintf(fp_products, "%d|%s|%.2f|%d\r\n",
                    products[i].id,
                    products[i].name,
                    products[i].price,
                    products[i].stock);
        }
        fclose(fp_products);
    }

    /* 保存销售数据 */
    fp_sales = fopen(SALES_FILE, "wb");
    if (fp_sales != NULL) {
        for (i = 0; i < sale_count; i++) {
            fprintf(fp_sales, "%d|%d|%s|%d|%.2f|%.2f|%s|%d\r\n",
                    sales[i].id,
                    sales[i].product_id,
                    sales[i].product_name,
                    sales[i].quantity,
                    sales[i].unit_price,
                    sales[i].total_amount,
                    sales[i].date,
                    sales[i].seller_id);
        }
        fclose(fp_sales);
    }
}

/* 显示主菜单 */
void show_menu(void) {
    const char *role_name;
    switch (current_role) {
        case 1: role_name = "管理员"; break;
        case 2: role_name = "店长"; break;
        case 3: role_name = "销售员"; break;
        default: role_name = "用户";
    }

    printf("========================================\n");
    printf("          销售系统 - %s\n", role_name);
    printf("========================================\n");
    printf("1. 修改密码\n");
    if (current_role == 1) {
        printf("2. 用户管理\n");
    }
    if (current_role == 1 || current_role == 2) {
        printf("3. 商品管理\n");
    }
    if (current_role == 3) {
        printf("3. 商品浏览\n");
        printf("4. 销售商品\n");
    } else {
        printf("4. 销售商品\n");
    }
    printf("5. 日报表\n");
    printf("6. 月报表\n");
    if (current_role == 1 || current_role == 2) {
        printf("7. 商品销售量报表\n");
        printf("8. 销售员业绩报表\n");
    }
    printf("0. 退出\n");
    printf("========================================\n");
}

/* 修改密码 */
void modify_password(void) {
    char old_password[MAX_PASSWORD_LEN];
    char new_password[MAX_PASSWORD_LEN];
    char confirm_password[MAX_PASSWORD_LEN];
    int i;

    printf("\n=== 修改密码 ===\n");

    /* 验证旧密码 */
    printf("请输入旧密码：");
    fgets(old_password, sizeof(old_password), stdin);
    old_password[strcspn(old_password, "\n")] = '\0';

    for (i = 0; i < user_count; i++) {
        if (users[i].id == current_user_id) {
            if (strcmp(users[i].password, old_password) != 0) {
                printf("\n旧密码错误！\n");
                pause_screen();
                return;
            }
            break;
        }
    }

    /* 输入新密码 */
    printf("请输入新密码：");
    fgets(new_password, sizeof(new_password), stdin);
    new_password[strcspn(new_password, "\n")] = '\0';

    printf("请确认新密码：");
    fgets(confirm_password, sizeof(confirm_password), stdin);
    confirm_password[strcspn(confirm_password, "\n")] = '\0';

    if (strcmp(new_password, confirm_password) != 0) {
        printf("\n两次密码不一致！\n");
        pause_screen();
        return;
    }

    /* 更新密码 */
    for (i = 0; i < user_count; i++) {
        if (users[i].id == current_user_id) {
            strcpy(users[i].password, new_password);
            break;
        }
    }

    save_data();
    printf("\n密码修改成功！\n");
    pause_screen();
}

/* 用户管理 */
void manage_users(void) {
    char choice;
    int i;

    while (1) {
        clear_screen();
        printf("========================================\n");
        printf("          用户管理\n");
        printf("========================================\n");
        printf("1. 添加用户\n");
        printf("2. 修改用户\n");
        printf("3. 查找用户\n");
        printf("4. 删除用户\n");
        printf("0. 返回\n");
        printf("========================================\n");

        printf("\n请选择功能（0-4）：");
        scanf("%c", &choice);
        getchar();

        switch (choice) {
            case '1': {
                /* 添加用户 */
                char username[MAX_NAME_LEN];
                char password[MAX_PASSWORD_LEN];
                int role;

                printf("\n=== 添加用户 ===\n");
                printf("请输入用户名：");
                fgets(username, sizeof(username), stdin);
                username[strcspn(username, "\n")] = '\0';

                printf("请输入密码：");
                fgets(password, sizeof(password), stdin);
                password[strcspn(password, "\n")] = '\0';

                printf("请输入角色（1-管理员, 2-店长, 3-销售员）：");
                scanf("%d", &role);
                getchar();

                if (role < 1 || role > 3) {
                    printf("\n角色无效！\n");
                    pause_screen();
                    break;
                }

                /* 查找最大用户ID */
                int max_id = 0;
                for (i = 0; i < user_count; i++) {
                    if (users[i].id > max_id) {
                        max_id = users[i].id;
                    }
                }

                users[user_count].id = max_id + 1;
                strcpy(users[user_count].username, username);
                strcpy(users[user_count].password, password);
                users[user_count].role = role;
                user_count++;

                save_data();
                printf("\n用户添加成功！用户ID: %d\n", max_id + 1);
                pause_screen();
                break;
            }
            case '2': {
                /* 修改用户 */
                int user_id;
                printf("\n=== 修改用户 ===\n");
                printf("请输入用户ID：");
                scanf("%d", &user_id);
                getchar();

                for (i = 0; i < user_count; i++) {
                    if (users[i].id == user_id) {
                        char username[MAX_NAME_LEN];
                        char password[MAX_PASSWORD_LEN];
                        int role;

                        printf("当前用户名：%s\n", users[i].username);
                        printf("请输入新用户名（直接回车保持原值）：");
                        fgets(username, sizeof(username), stdin);
                        username[strcspn(username, "\n")] = '\0';
                        if (strlen(username) > 0) {
                            strcpy(users[i].username, username);
                        }

                        printf("请输入新密码（直接回车保持原值）：");
                        fgets(password, sizeof(password), stdin);
                        password[strcspn(password, "\n")] = '\0';
                        if (strlen(password) > 0) {
                            strcpy(users[i].password, password);
                        }

                        printf("当前角色：%d\n", users[i].role);
                        printf("请输入新角色（1-管理员, 2-店长, 3-销售员，直接回车保持原值）：");
                        char role_str[10];
                        fgets(role_str, sizeof(role_str), stdin);
                        if (strlen(role_str) > 0) {
                            role = atoi(role_str);
                            if (role >= 1 && role <= 3) {
                                users[i].role = role;
                            }
                        }

                        save_data();
                        printf("\n用户修改成功！\n");
                        pause_screen();
                        break;
                    }
                }
                if (i >= user_count) {
                    printf("\n未找到该用户！\n");
                    pause_screen();
                }
                break;
            }
            case '3': {
                /* 查找用户 */
                char username[MAX_NAME_LEN];
                printf("\n=== 查找用户 ===\n");
                printf("请输入用户名：");
                fgets(username, sizeof(username), stdin);
                username[strcspn(username, "\n")] = '\0';

                printf("\n查找结果：\n");
                printf("ID\t用户名\t\t角色\n");
                print_separator();
                int found = 0;
                for (i = 0; i < user_count; i++) {
                    if (strstr(users[i].username, username) != NULL) {
                        const char *role_name;
                        switch (users[i].role) {
                            case 1: role_name = "管理员"; break;
                            case 2: role_name = "店长"; break;
                            case 3: role_name = "销售员"; break;
                            default: role_name = "未知";
                        }
                        printf("%d\t%s\t\t%s\n", users[i].id, users[i].username, role_name);
                        found = 1;
                    }
                }
                if (!found) {
                    printf("未找到匹配的用户！\n");
                }
                pause_screen();
                break;
            }
            case '4': {
                /* 删除用户 */
                int user_id;
                printf("\n=== 删除用户 ===\n");
                printf("请输入用户ID：");
                scanf("%d", &user_id);
                getchar();

                for (i = 0; i < user_count; i++) {
                    if (users[i].id == user_id) {
                        /* 移动后续数据 */
                        for (int j = i; j < user_count - 1; j++) {
                            users[j] = users[j + 1];
                        }
                        user_count--;

                        save_data();
                        printf("\n用户删除成功！\n");
                        pause_screen();
                        break;
                    }
                }
                if (i >= user_count) {
                    printf("\n未找到该用户！\n");
                    pause_screen();
                }
                break;
            }
            case '0':
                return;
            default:
                printf("\n无效的选择，请重新输入！\n");
                pause_screen();
        }
    }
}

/* 商品管理 */
void manage_products(void) {
    char choice;
    int i;

    while (1) {
        clear_screen();
        printf("========================================\n");
        printf("          商品管理\n");
        printf("========================================\n");
        printf("1. 添加商品\n");
        printf("2. 修改商品\n");
        printf("3. 查找商品\n");
        printf("4. 删除商品\n");
        printf("5. 显示所有商品\n");
        printf("0. 返回\n");
        printf("========================================\n");

        printf("\n请选择功能（0-5）：");
        scanf("%c", &choice);
        getchar();

        switch (choice) {
            case '1': {
                char name[MAX_NAME_LEN];
                double price;
                int stock;

                printf("\n=== 添加商品 ===\n");
                printf("请输入商品名称：");
                fgets(name, sizeof(name), stdin);
                name[strcspn(name, "\n")] = '\0';

                printf("请输入单价：");
                scanf("%lf", &price);
                getchar();

                printf("请输入库存量：");
                scanf("%d", &stock);
                getchar();

                int max_id = 1000;
                for (i = 0; i < product_count; i++) {
                    if (products[i].id > max_id) {
                        max_id = products[i].id;
                    }
                }

                products[product_count].id = max_id + 1;
                strcpy(products[product_count].name, name);
                products[product_count].price = price;
                products[product_count].stock = stock;
                product_count++;

                save_data();
                printf("\n商品添加成功！商品ID: %d\n", max_id + 1);
                pause_screen();
                break;
            }
            case '2': {
                int product_id;
                printf("\n=== 修改商品 ===\n");
                printf("请输入商品ID：");
                scanf("%d", &product_id);
                getchar();

                for (i = 0; i < product_count; i++) {
                    if (products[i].id == product_id) {
                        char name[MAX_NAME_LEN];
                        double price;
                        int stock;

                        printf("当前商品名称：%s\n", products[i].name);
                        printf("请输入新商品名称（直接回车保持原值）：");
                        fgets(name, sizeof(name), stdin);
                        name[strcspn(name, "\n")] = '\0';
                        if (strlen(name) > 0) {
                            strcpy(products[i].name, name);
                        }

                        printf("当前单价：%.2f\n", products[i].price);
                        printf("请输入新单价（直接回车保持原值）：");
                        char price_str[20];
                        fgets(price_str, sizeof(price_str), stdin);
                        if (strlen(price_str) > 0) {
                            price = atof(price_str);
                            if (price > 0) {
                                products[i].price = price;
                            }
                        }

                        printf("当前库存量：%d\n", products[i].stock);
                        printf("请输入新库存量（直接回车保持原值）：");
                        char stock_str[20];
                        fgets(stock_str, sizeof(stock_str), stdin);
                        if (strlen(stock_str) > 0) {
                            stock = atoi(stock_str);
                            if (stock >= 0) {
                                products[i].stock = stock;
                            }
                        }

                        save_data();
                        printf("\n商品修改成功！\n");
                        pause_screen();
                        break;
                    }
                }
                if (i >= product_count) {
                    printf("\n未找到该商品！\n");
                    pause_screen();
                }
                break;
            }
            case '3': {
                char name[MAX_NAME_LEN];
                printf("\n=== 查找商品 ===\n");
                printf("请输入商品名称：");
                fgets(name, sizeof(name), stdin);
                name[strcspn(name, "\n")] = '\0';

                printf("\n查找结果：\n");
                printf("ID\t商品名称\t\t单价\t\t库存\n");
                print_separator();
                int found = 0;
                for (i = 0; i < product_count; i++) {
                    if (strstr(products[i].name, name) != NULL) {
                        printf("%d\t%s\t\t%.2f\t\t%d\n",
                               products[i].id,
                               products[i].name,
                               products[i].price,
                               products[i].stock);
                        found = 1;
                    }
                }
                if (!found) {
                    printf("未找到匹配的商品！\n");
                }
                pause_screen();
                break;
            }
            case '4': {
                int product_id;
                printf("\n=== 删除商品 ===\n");
                printf("请输入商品ID：");
                scanf("%d", &product_id);
                getchar();

                for (i = 0; i < product_count; i++) {
                    if (products[i].id == product_id) {
                        for (int j = i; j < product_count - 1; j++) {
                            products[j] = products[j + 1];
                        }
                        product_count--;

                        save_data();
                        printf("\n商品删除成功！\n");
                        pause_screen();
                        break;
                    }
                }
                if (i >= product_count) {
                    printf("\n未找到该商品！\n");
                    pause_screen();
                }
                break;
            }
            case '5': {
                printf("\n=== 所有商品 ===\n");
                printf("ID\t商品名称\t\t单价\t\t库存\n");
                print_separator();
                for (i = 0; i < product_count; i++) {
                    printf("%d\t%s\t\t%.2f\t\t%d\n",
                           products[i].id,
                           products[i].name,
                           products[i].price,
                           products[i].stock);
                }
                pause_screen();
                break;
            }
            case '0':
                return;
            default:
                printf("\n无效的选择，请重新输入！\n");
                pause_screen();
        }
    }
}

/* 商品浏览 */
void browse_products(void) {
    int i;
    printf("\n=== 商品浏览 ===\n");
    printf("ID\t商品名称\t\t单价\t\t库存\n");
    print_separator();
    for (i = 0; i < product_count; i++) {
        printf("%d\t%s\t\t%.2f\t\t%d\n",
               products[i].id,
               products[i].name,
               products[i].price,
               products[i].stock);
    }
    pause_screen();
}

/* 销售商品 */
void sell_product(void) {
    int product_id, quantity, i;

    browse_products();

    printf("\n=== 销售商品 ===\n");
    printf("请输入商品ID：");
    scanf("%d", &product_id);
    getchar();

    for (i = 0; i < product_count; i++) {
        if (products[i].id == product_id) {
            printf("商品名称：%s\n", products[i].name);
            printf("单价：%.2f\n", products[i].price);
            printf("库存量：%d\n", products[i].stock);

            printf("请输入销售数量：");
            scanf("%d", &quantity);
            getchar();

            if (quantity <= 0) {
                printf("\n销售数量无效！\n");
                pause_screen();
                return;
            }

            if (quantity > products[i].stock) {
                printf("\n库存不足！\n");
                pause_screen();
                return;
            }

            products[i].stock -= quantity;

            sales[sale_count].id = sale_count + 1;
            sales[sale_count].product_id = product_id;
            strcpy(sales[sale_count].product_name, products[i].name);
            sales[sale_count].quantity = quantity;
            sales[sale_count].unit_price = products[i].price;
            sales[sale_count].total_amount = quantity * products[i].price;

            printf("请输入销售日期（YYYY-MM-DD）：");
            fgets(sales[sale_count].date, sizeof(sales[sale_count].date), stdin);
            sales[sale_count].date[strcspn(sales[sale_count].date, "\n")] = '\0';

            sales[sale_count].seller_id = current_user_id;
            sale_count++;

            save_data();
            printf("\n销售成功！总金额：%.2f\n", quantity * products[i].price);
            pause_screen();
            return;
        }
    }

    printf("\n未找到该商品！\n");
    pause_screen();
}

/* 日报表 */
void show_daily_report(void) {
    char date[MAX_DATE_LEN];
    int i;

    printf("\n=== 销售日报表 ===\n");
    printf("请输入日期（YYYY-MM-DD，直接回车使用今天）：");
    fgets(date, sizeof(date), stdin);
    date[strcspn(date, "\n")] = '\0';

    if (strlen(date) == 0) {
        /* 获取当天日期 */
        time_t t = time(NULL);
        struct tm *tm_info = localtime(&t);
        strftime(date, sizeof(date), "%Y-%m-%d", tm_info);
        printf("使用今天的日期: %s\n", date);
    }

    printf("\n日期：%s\n", date);
    printf("ID\t商品名称\t\t数量\t单价\t总金额\t销售员\n");
    print_separator();

    double total_amount = 0;
    for (i = 0; i < sale_count; i++) {
        if (strcmp(sales[i].date, date) == 0) {
            /* 角色权限检查 */
            if (current_role == 3 && sales[i].seller_id != current_user_id) {
                continue;
            }

            const char *seller_name = "未知";
            for (int j = 0; j < user_count; j++) {
                if (users[j].id == sales[i].seller_id) {
                    seller_name = users[j].username;
                    break;
                }
            }

            printf("%d\t%s\t\t%d\t%.2f\t%.2f\t%s\n",
                   sales[i].id,
                   sales[i].product_name,
                   sales[i].quantity,
                   sales[i].unit_price,
                   sales[i].total_amount,
                   seller_name);
            total_amount += sales[i].total_amount;
        }
    }

    print_separator();
    printf("当日总金额：%.2f\n", total_amount);
    pause_screen();
}

/* 月报表 */
void show_monthly_report(void) {
    char month[8];
    int i;

    printf("\n=== 销售月报表 ===\n");
    printf("请输入月份（YYYY-MM，如 2024-01）：");
    fgets(month, sizeof(month), stdin);
    month[strcspn(month, "\n")] = '\0';

    printf("\n月份：%s\n", month);
    printf("ID\t商品名称\t\t数量\t单价\t总金额\t销售日期\t销售员\n");
    print_separator();

    double total_amount = 0;
    for (i = 0; i < sale_count; i++) {
        if (strncmp(sales[i].date, month, 7) == 0) {
            if (current_role == 3 && sales[i].seller_id != current_user_id) {
                continue;
            }

            const char *seller_name = "未知";
            for (int j = 0; j < user_count; j++) {
                if (users[j].id == sales[i].seller_id) {
                    seller_name = users[j].username;
                    break;
                }
            }

            printf("%d\t%s\t\t%d\t%.2f\t%.2f\t%s\t%s\n",
                   sales[i].id,
                   sales[i].product_name,
                   sales[i].quantity,
                   sales[i].unit_price,
                   sales[i].total_amount,
                   sales[i].date,
                   seller_name);
            total_amount += sales[i].total_amount;
        }
    }

    print_separator();
    printf("当月总金额：%.2f\n", total_amount);
    pause_screen();
}

/* 商品销售量报表 */
void show_product_sales_report(void) {
    int i, j;
    int stats[MAX_PRODUCTS][2];  /* [销售数量, 是否已统计] */

    printf("\n=== 商品销售量报表 ===\n");

    /* 初始化统计数据 */
    for (i = 0; i < product_count; i++) {
        stats[i][0] = 0;
        stats[i][1] = 0;
    }

    /* 统计销售数量 */
    for (i = 0; i < sale_count; i++) {
        for (j = 0; j < product_count; j++) {
            if (products[j].id == sales[i].product_id) {
                stats[j][0] += sales[i].quantity;
                stats[j][1] = 1;
                break;
            }
        }
    }

    printf("商品ID\t商品名称\t\t销售数量\t销售金额\n");
    print_separator();

    for (i = 0; i < product_count; i++) {
        if (stats[i][1] == 1) {
            double amount = stats[i][0] * products[i].price;
            printf("%d\t%s\t\t%d\t\t%.2f\n",
                   products[i].id,
                   products[i].name,
                   stats[i][0],
                   amount);
        }
    }

    pause_screen();
}

/* 销售员业绩报表 */
void show_seller_performance_report(void) {
    int i, j;
    double stats[MAX_USERS][2];  /* [销售金额, 销售单数] */

    printf("\n=== 销售员业绩报表 ===\n");

    /* 初始化统计数据 */
    for (i = 0; i < user_count; i++) {
        stats[i][0] = 0.0;
        stats[i][1] = 0.0;
    }

    /* 统计销售员业绩 */
    for (i = 0; i < sale_count; i++) {
        for (j = 0; j < user_count; j++) {
            if (users[j].id == sales[i].seller_id && users[j].role == 3) {
                stats[j][0] += sales[i].total_amount;
                stats[j][1] += 1.0;
                break;
            }
        }
    }

    printf("销售员ID\t销售员姓名\t销售单数\t销售金额\n");
    print_separator();

    for (i = 0; i < user_count; i++) {
        if (users[i].role == 3 && stats[i][1] > 0) {
            printf("%d\t\t%s\t\t%.0f\t\t%.2f\n",
                   users[i].id,
                   users[i].username,
                   stats[i][1],
                   stats[i][0]);
        }
    }

    pause_screen();
}