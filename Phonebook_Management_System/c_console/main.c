/*
 * 电话簿管理系统 - C语言控制台版
 * 功能：联系人的增删改查、排序、搜索、文件存储
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

#define MAX_CONTACTS 1000
#define MAX_NAME_LEN 50
#define MAX_WORK_LEN 100
#define MAX_PHONE_LEN 20
#define MAX_EMAIL_LEN 100
#define MAX_PASSWORD_LEN 50

/* 文件路径 */
#define PASSWORD_FILE "../dataset/password.txt"
#define CONTACTS_FILE "../dataset/contacts.txt"

/* 联系人结构体 */
typedef struct {
    int id;
    char name[MAX_NAME_LEN];
    char work_unit[MAX_WORK_LEN];
    char phone[MAX_PHONE_LEN];
    char email[MAX_EMAIL_LEN];
} Contact;

/* 全局变量 */
Contact contacts[MAX_CONTACTS];
int contact_count = 0;

/* 函数声明 */
void clear_screen(void);
void pause_screen(void);
void print_separator(void);
int verify_password(void);
void load_data(void);
void save_data(void);

void show_menu(void);
void add_contact(void);
void delete_contact(void);
void display_all_contacts(void);
void modify_contact(void);
void sort_contacts(void);
void search_contacts(void);
void save_to_file(void);
void load_from_file(void);

/* 输入验证函数 */
int is_valid_phone(const char *phone);
int is_valid_email(const char *email);
int is_alpha(const char *str);
void trim_space(char *str);

/* 排序比较函数 */
int compare_by_name(const void *a, const void *b);
int compare_by_phone(const void *a, const void *b);

/* 头文件 */
#ifdef _WIN32
#include <conio.h>
#else
#include <termios.h>
#include <unistd.h>
#endif

/* 密码加密 */
void encrypt_password(const char *password, char *encrypted);
int verify_encrypted_password(const char *input, const char *encrypted);
void modify_system_password(void);

#ifdef _WIN32
#define getch _getch
#else
/* Linux/Mac下的getch实现 */
static char getch(void) {
    char buf = 0;
    struct termios old = {0};
    if (tcgetattr(0, &old) < 0)
        perror("tcsetattr()");
    old.c_lflag &= ~ICANON;
    old.c_lflag &= ~ECHO;
    old.c_cc[VMIN] = 1;
    old.c_cc[VTIME] = 0;
    if (tcsetattr(0, TCSANOW, &old) < 0)
        perror("tcsetattr ICANON");
    if (read(0, &buf, 1) < 0)
        perror("read()");
    old.c_lflag |= ICANON;
    old.c_lflag |= ECHO;
    if (tcsetattr(0, TCSADRAIN, &old) < 0)
        perror("tcsetattr ~ICANON");
    return (buf);
}
#endif

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
        printf("\n请选择功能（0-10）：");
        scanf("%s", input);

        if (strlen(input) != 1 || !isdigit(input[0])) {
            printf("\n输入无效，请输入0-10之间的数字！\n");
            pause_screen();
            continue;
        }

        switch (input[0]) {
            case '1':
                add_contact();
                break;
            case '2':
                delete_contact();
                break;
            case '3':
                display_all_contacts();
                break;
            case '4':
                modify_contact();
                break;
            case '5':
                sort_contacts();
                break;
            case '6':
                search_contacts();
                break;
            case '7':
                save_to_file();
                break;
            case '8':
                load_from_file();
                break;
            case '9':
                /* 修改密码功能 */
                modify_system_password();
                break;
            case '0':
                printf("\n感谢使用电话簿管理系统，再见！\n");
                pause_screen();
                return 0;
            default:
                printf("\n无效选择，请重新输入！\n");
                pause_screen();
        }
    }

    return 0;
}

/* 清屏 */
void clear_screen(void) {
    system("cls || clear");
}

/* 暂停屏幕 */
void pause_screen(void) {
    printf("\n按任意键继续...");
    getchar();
    getchar();
}

/* 打印分隔线 */
void print_separator(void) {
    printf("========================================\n");
}

/* 密码验证 */
int verify_password(void) {
    FILE *fp;
    char stored_password[MAX_PASSWORD_LEN];
    char input_password[MAX_PASSWORD_LEN];
    char encrypted_input[MAX_PASSWORD_LEN];
    char c;
    int i = 0;

    fp = fopen(PASSWORD_FILE, "r");
    if (fp == NULL) {
        /* 文件不存在，创建默认密码（加密存储） */
        fp = fopen(PASSWORD_FILE, "w");
        if (fp == NULL) {
            printf("无法创建密码文件！\n");
            return 0;
        }
        encrypt_password("admin123", stored_password);
        fprintf(fp, "%s", stored_password);
        fclose(fp);
    } else {
        fscanf(fp, "%s", stored_password);
        fclose(fp);
    }

    printf("\n");
    print_separator();
    printf("          电话簿管理系统\n");
    print_separator();

    printf("\n请输入密码：");

    /* 密码隐藏输入 */
    while ((c = getch()) != '\r' && i < MAX_PASSWORD_LEN - 1) {
        if (c == '\b') {
            if (i > 0) {
                i--;
                printf("\b \b");
            }
        } else {
            input_password[i++] = c;
            printf("*");
        }
    }
    input_password[i] = '\0';
    printf("\n");

    /* 验证密码 - 先尝试加密后比较，如果失败再尝试明文比较（兼容旧密码文件） */
    encrypt_password(input_password, encrypted_input);
    if (strcmp(encrypted_input, stored_password) == 0) {
        return 1;
    }
    /* 兼容明文密码文件 */
    if (strcmp(input_password, stored_password) == 0) {
        /* 如果是明文密码，自动升级为加密密码 */
        char encrypted[MAX_PASSWORD_LEN];
        encrypt_password(input_password, encrypted);
        fp = fopen(PASSWORD_FILE, "w");
        if (fp != NULL) {
            fprintf(fp, "%s", encrypted);
            fclose(fp);
        }
        return 1;
    }
    return 0;
}

/* 修改系统密码 */
void modify_system_password(void) {
    FILE *fp;
    char old_password[MAX_PASSWORD_LEN];
    char new_password[MAX_PASSWORD_LEN];
    char confirm_password[MAX_PASSWORD_LEN];
    char stored_password[MAX_PASSWORD_LEN];
    char c;
    int i;

    fp = fopen(PASSWORD_FILE, "r");
    if (fp != NULL) {
        fscanf(fp, "%s", stored_password);
        fclose(fp);
    } else {
        strcpy(stored_password, "admin123");
    }

    printf("\n");
    print_separator();
    printf("          修改系统密码\n");
    print_separator();

    /* 输入旧密码 */
    printf("\n请输入旧密码：");
    i = 0;
    while ((c = getch()) != '\r' && i < MAX_PASSWORD_LEN - 1) {
        if (c == '\b') {
            if (i > 0) {
                i--;
                printf("\b \b");
            }
        } else {
            old_password[i++] = c;
            printf("*");
        }
    }
    old_password[i] = '\0';
    printf("\n");

    /* 验证旧密码 */
    {
        char encrypted_old[MAX_PASSWORD_LEN];
        encrypt_password(old_password, encrypted_old);
        if (strcmp(encrypted_old, stored_password) != 0) {
            printf("\n旧密码错误！\n");
            pause_screen();
            return;
        }
    }

    /* 输入新密码 */
    printf("请输入新密码：");
    i = 0;
    while ((c = getch()) != '\r' && i < MAX_PASSWORD_LEN - 1) {
        if (c == '\b') {
            if (i > 0) {
                i--;
                printf("\b \b");
            }
        } else {
            new_password[i++] = c;
            printf("*");
        }
    }
    new_password[i] = '\0';
    printf("\n");

    /* 确认新密码 */
    printf("请确认新密码：");
    i = 0;
    while ((c = getch()) != '\r' && i < MAX_PASSWORD_LEN - 1) {
        if (c == '\b') {
            if (i > 0) {
                i--;
                printf("\b \b");
            }
        } else {
            confirm_password[i++] = c;
            printf("*");
        }
    }
    confirm_password[i] = '\0';
    printf("\n");

    if (strcmp(new_password, confirm_password) != 0) {
        printf("\n两次输入的密码不一致！\n");
        pause_screen();
        return;
    }

    /* 保存新密码 */
    fp = fopen(PASSWORD_FILE, "w");
    if (fp == NULL) {
        printf("\n无法保存密码文件！\n");
        pause_screen();
        return;
    }

    {
        char encrypted_new[MAX_PASSWORD_LEN];
        encrypt_password(new_password, encrypted_new);
        fprintf(fp, "%s", encrypted_new);
    }
    fclose(fp);

    printf("\n密码修改成功！\n");
    pause_screen();
}

/* 加载数据 */
void load_data(void) {
    FILE *fp;
    char line[500];

    fp = fopen(CONTACTS_FILE, "r");
    if (fp == NULL) {
        return;
    }

    while (fgets(line, sizeof(line), fp) != NULL) {
        char *token;
        int id;
        char name[MAX_NAME_LEN];
        char work[MAX_WORK_LEN];
        char phone[MAX_PHONE_LEN];
        char email[MAX_EMAIL_LEN];

        /* 跳过空行和注释 */
        if (strlen(line) <= 1 || line[0] == '#') {
            continue;
        }

        /* 解析行 */
        token = strtok(line, "|");
        if (token == NULL) continue;
        id = atoi(token);

        token = strtok(NULL, "|");
        if (token == NULL) continue;
        strcpy(name, token);
        trim_space(name);

        token = strtok(NULL, "|");
        if (token == NULL) continue;
        strcpy(work, token);
        trim_space(work);

        token = strtok(NULL, "|");
        if (token == NULL) continue;
        strcpy(phone, token);
        trim_space(phone);

        token = strtok(NULL, "|");
        if (token == NULL) continue;
        strcpy(email, token);
        trim_space(email);

        if (contact_count < MAX_CONTACTS) {
            contacts[contact_count].id = id;
            strcpy(contacts[contact_count].name, name);
            strcpy(contacts[contact_count].work_unit, work);
            strcpy(contacts[contact_count].phone, phone);
            strcpy(contacts[contact_count].email, email);
            contact_count++;
        }
    }

    fclose(fp);
}

/* 保存数据 */
void save_data(void) {
    FILE *fp;
    int i;

    fp = fopen(CONTACTS_FILE, "w");
    if (fp == NULL) {
        printf("无法保存数据文件！\n");
        return;
    }

    for (i = 0; i < contact_count; i++) {
        fprintf(fp, "%d|%s|%s|%s|%s\n",
                contacts[i].id,
                contacts[i].name,
                contacts[i].work_unit,
                contacts[i].phone,
                contacts[i].email);
    }

    fclose(fp);
}

/* 显示菜单 */
void show_menu(void) {
    printf("\n");
    print_separator();
    printf("          电话簿管理系统\n");
    print_separator();
    printf("  1. 添加联系人\n");
    printf("  2. 删除联系人\n");
    printf("  3. 显示所有联系人\n");
    printf("  4. 修改联系人\n");
    printf("  5. 排序联系人\n");
    printf("  6. 查询联系人\n");
    printf("  7. 保存信息到文件\n");
    printf("  8. 从文件读取信息\n");
    printf("  9. 修改系统密码\n");
    printf("  0. 退出系统\n");
    print_separator();
}

/* 添加联系人 */
void add_contact(void) {
    Contact new_contact;
    char phone[MAX_PHONE_LEN];
    char email[MAX_EMAIL_LEN];
    int max_id = 0, i;

    printf("\n");
    print_separator();
    printf("          添加联系人\n");
    print_separator();

    /* 生成新ID */
    for (i = 0; i < contact_count; i++) {
        if (contacts[i].id > max_id) {
            max_id = contacts[i].id;
        }
    }
    new_contact.id = max_id + 1;

    /* 输入姓名 */
    printf("\n请输入姓名：");
    scanf("%s", new_contact.name);

    /* 输入工作单位 */
    printf("请输入工作单位：");
    getchar();
    fgets(new_contact.work_unit, MAX_WORK_LEN, stdin);
    trim_space(new_contact.work_unit);

    /* 输入电话号码 */
    while (1) {
        printf("请输入电话号码：");
        scanf("%s", phone);
        trim_space(phone);

        if (!is_valid_phone(phone)) {
            printf("电话号码格式错误！请重新输入。\n");
            continue;
        }

        /* 检查是否重复 */
        for (i = 0; i < contact_count; i++) {
            if (strcmp(contacts[i].phone, phone) == 0) {
                printf("该电话号码已存在！请重新输入。\n");
                break;
            }
        }

        if (i == contact_count) {
            strcpy(new_contact.phone, phone);
            break;
        }
    }

    /* 输入E-mail地址 */
    while (1) {
        printf("请输入E-mail地址：");
        scanf("%s", email);
        trim_space(email);

        if (!is_valid_email(email)) {
            printf("E-mail地址格式错误！请重新输入。\n");
            continue;
        }

        strcpy(new_contact.email, email);
        break;
    }

    /* 添加到数组 */
    if (contact_count < MAX_CONTACTS) {
        contacts[contact_count++] = new_contact;
        printf("\n联系人添加成功！\n");
    } else {
        printf("\n联系人数量已达上限，无法添加！\n");
    }

    pause_screen();
}

/* 删除联系人 */
void delete_contact(void) {
    char name[MAX_NAME_LEN];
    int i, found = 0;
    char choice;

    printf("\n");
    print_separator();
    printf("          删除联系人\n");
    print_separator();

    printf("\n请输入要删除的联系人姓名：");
    scanf("%s", name);

    /* 查找并显示匹配的联系人 */
    printf("\n查找结果：\n");
    for (i = 0; i < contact_count; i++) {
        if (strcmp(contacts[i].name, name) == 0) {
            printf("ID: %d, 姓名: %s, 电话: %s, 工作单位: %s, Email: %s\n",
                   contacts[i].id, contacts[i].name, contacts[i].phone,
                   contacts[i].work_unit, contacts[i].email);
            found = 1;
        }
    }

    if (!found) {
        printf("\n未找到该联系人！\n");
        pause_screen();
        return;
    }

    /* 确认删除 */
    printf("\n确认删除？(Y/N): ");
    scanf(" %c", &choice);

    if (choice == 'Y' || choice == 'y') {
        /* 删除所有匹配的联系人 */
        for (i = 0; i < contact_count; ) {
            if (strcmp(contacts[i].name, name) == 0) {
                /* 移动数组元素 */
                int j;
                for (j = i; j < contact_count - 1; j++) {
                    contacts[j] = contacts[j + 1];
                }
                contact_count--;
            } else {
                i++;
            }
        }
        printf("\n联系人删除成功！\n");
    } else {
        printf("\n取消删除！\n");
    }

    pause_screen();
}

/* 显示所有联系人 */
void display_all_contacts(void) {
    int i;

    printf("\n");
    print_separator();
    printf("          所有联系人列表\n");
    print_separator();

    if (contact_count == 0) {
        printf("\n电话簿为空！\n");
        pause_screen();
        return;
    }

    printf("\n%-6s %-15s %-20s %-15s %-25s\n",
           "ID", "姓名", "工作单位", "电话号码", "E-mail地址");
    printf("-----------------------------------------------------------------------------\n");

    for (i = 0; i < contact_count; i++) {
        printf("%-6d %-15s %-20s %-15s %-25s\n",
               contacts[i].id, contacts[i].name, contacts[i].work_unit,
               contacts[i].phone, contacts[i].email);
    }

    printf("\n共 %d 位联系人\n", contact_count);
    pause_screen();
}

/* 修改联系人 */
void modify_contact(void) {
    char name[MAX_NAME_LEN];
    int i, found = 0;
    int choice;
    char new_data[100];

    printf("\n");
    print_separator();
    printf("          修改联系人\n");
    print_separator();

    printf("\n请输入要修改的联系人姓名：");
    scanf("%s", name);

    /* 查找联系人 */
    for (i = 0; i < contact_count; i++) {
        if (strcmp(contacts[i].name, name) == 0) {
            printf("\n找到联系人：\n");
            printf("ID: %d, 姓名: %s, 电话: %s, 工作单位: %s, Email: %s\n",
                   contacts[i].id, contacts[i].name, contacts[i].phone,
                   contacts[i].work_unit, contacts[i].email);
            found = 1;
            break;
        }
    }

    if (!found) {
        printf("\n未找到该联系人！\n");
        pause_screen();
        return;
    }

    printf("\n选择要修改的项目：\n");
    printf("1. 姓名\n");
    printf("2. 工作单位\n");
    printf("3. 电话号码\n");
    printf("4. E-mail地址\n");
    printf("请选择（1-4）：");
    scanf("%d", &choice);

    switch (choice) {
        case 1:
            printf("请输入新的姓名：");
            scanf("%s", new_data);
            strcpy(contacts[i].name, new_data);
            break;
        case 2:
            printf("请输入新的工作单位：");
            getchar();
            fgets(new_data, MAX_WORK_LEN, stdin);
            trim_space(new_data);
            strcpy(contacts[i].work_unit, new_data);
            break;
        case 3:
            while (1) {
                printf("请输入新的电话号码：");
                scanf("%s", new_data);
                trim_space(new_data);

                if (!is_valid_phone(new_data)) {
                    printf("电话号码格式错误！请重新输入。\n");
                    continue;
                }

                /* 检查是否与其他联系人重复 */
                int j;
                for (j = 0; j < contact_count; j++) {
                    if (j != i && strcmp(contacts[j].phone, new_data) == 0) {
                        printf("该电话号码已存在！请重新输入。\n");
                        break;
                    }
                }

                if (j == contact_count) {
                    strcpy(contacts[i].phone, new_data);
                    break;
                }
            }
            break;
        case 4:
            while (1) {
                printf("请输入新的E-mail地址：");
                scanf("%s", new_data);
                trim_space(new_data);

                if (!is_valid_email(new_data)) {
                    printf("E-mail地址格式错误！请重新输入。\n");
                    continue;
                }

                strcpy(contacts[i].email, new_data);
                break;
            }
            break;
        default:
            printf("无效选择！\n");
            pause_screen();
            return;
    }

    printf("\n联系人信息修改成功！\n");
    pause_screen();
}

/* 排序联系人 */
void sort_contacts(void) {
    int choice;

    if (contact_count == 0) {
        printf("\n电话簿为空，无需排序！\n");
        pause_screen();
        return;
    }

    printf("\n");
    print_separator();
    printf("          排序联系人\n");
    print_separator();

    printf("\n请选择排序方式：\n");
    printf("1. 按姓名字母序排序\n");
    printf("2. 按电话号码排序\n");
    printf("请选择（1-2）：");
    scanf("%d", &choice);

    switch (choice) {
        case 1:
            qsort(contacts, contact_count, sizeof(Contact), compare_by_name);
            printf("\n已按姓名排序！\n");
            break;
        case 2:
            qsort(contacts, contact_count, sizeof(Contact), compare_by_phone);
            printf("\n已按电话号码排序！\n");
            break;
        default:
            printf("无效选择！\n");
            pause_screen();
            return;
    }

    /* 显示排序结果 */
    display_all_contacts();
}

/* 查询联系人 */
void search_contacts(void) {
    int choice;
    char keyword[100];
    int i, found = 0;

    printf("\n");
    print_separator();
    printf("          查询联系人\n");
    print_separator();

    printf("\n请选择查询方式：\n");
    printf("1. 按姓名查询\n");
    printf("2. 按电话号码查询\n");
    printf("请选择（1-2）：");
    scanf("%d", &choice);

    switch (choice) {
        case 1:
            printf("\n请输入姓名关键词：");
            scanf("%s", keyword);

            printf("\n查询结果：\n");
            printf("-----------------------------------------------------------------------------\n");

            for (i = 0; i < contact_count; i++) {
                if (strstr(contacts[i].name, keyword) != NULL) {
                    printf("%-6d %-15s %-20s %-15s %-25s\n",
                           contacts[i].id, contacts[i].name, contacts[i].work_unit,
                           contacts[i].phone, contacts[i].email);
                    found = 1;
                }
            }
            break;

        case 2:
            printf("\n请输入电话号码关键词：");
            scanf("%s", keyword);

            printf("\n查询结果：\n");
            printf("-----------------------------------------------------------------------------\n");

            for (i = 0; i < contact_count; i++) {
                if (strstr(contacts[i].phone, keyword) != NULL) {
                    printf("%-6d %-15s %-20s %-15s %-25s\n",
                           contacts[i].id, contacts[i].name, contacts[i].work_unit,
                           contacts[i].phone, contacts[i].email);
                    found = 1;
                }
            }
            break;

        default:
            printf("无效选择！\n");
            pause_screen();
            return;
    }

    if (!found) {
        printf("\n未找到匹配的联系人！\n");
    } else {
        printf("\n共找到 %d 位联系人\n", found);
    }

    pause_screen();
}

/* 保存到文件 */
void save_to_file(void) {
    save_data();
    printf("\n联系人信息已保存到文件！\n");
    pause_screen();
}

/* 从文件读取 */
void load_from_file(void) {
    load_data();
    printf("\n已从文件加载 %d 位联系人！\n", contact_count);
    pause_screen();
}

/* 按姓名比较 */
int compare_by_name(const void *a, const void *b) {
    Contact *contact_a = (Contact *)a;
    Contact *contact_b = (Contact *)b;
    return strcmp(contact_a->name, contact_b->name);
}

/* 按电话号码比较 */
int compare_by_phone(const void *a, const void *b) {
    Contact *contact_a = (Contact *)a;
    Contact *contact_b = (Contact *)b;
    return strcmp(contact_a->phone, contact_b->phone);
}

/* 验证电话号码 */
int is_valid_phone(const char *phone) {
    int len = strlen(phone);
    int i;

    if (len < 7 || len > 15) {
        return 0;
    }

    for (i = 0; i < len; i++) {
        if (!isdigit(phone[i]) && phone[i] != '-' && phone[i] != ' ') {
            return 0;
        }
    }

    return 1;
}

/* 验证E-mail */
int is_valid_email(const char *email) {
    int len = strlen(email);
    int i;
    int at_count = 0;
    int dot_after_at = 0;

    if (len < 5 || len > MAX_EMAIL_LEN - 1) {
        return 0;
    }

    for (i = 0; i < len; i++) {
        if (email[i] == '@') {
            at_count++;
            if (i == 0 || i == len - 1) {
                return 0;
            }
        } else if (email[i] == '.' && at_count > 0) {
            dot_after_at = 1;
        }
    }

    if (at_count != 1 || !dot_after_at) {
        return 0;
    }

    return 1;
}

/* 去除空格 */
void trim_space(char *str) {
    int i = 0, j = 0;
    int len = strlen(str);

    /* 去除前导空格 */
    while (str[i] == ' ' || str[i] == '\t') {
        i++;
    }

    /* 去除尾部空格和换行符 */
    j = len - 1;
    while (j >= 0 && (str[j] == ' ' || str[j] == '\t' || str[j] == '\n' || str[j] == '\r')) {
        j--;
    }

    /* 移动字符 */
    for (len = 0; i <= j; i++, len++) {
        str[len] = str[i];
    }

    str[len] = '\0';
}

/* 密码加密（简单的异或加密） */
void encrypt_password(const char *password, char *encrypted) {
    int i;
    int len = strlen(password);

    for (i = 0; i < len; i++) {
        encrypted[i] = password[i] ^ 0x55; /* 异或加密 */
    }
    encrypted[len] = '\0';
}

/* 验证加密密码 */
int verify_encrypted_password(const char *input, const char *encrypted) {
    char encrypted_input[MAX_PASSWORD_LEN];
    encrypt_password(input, encrypted_input);
    return (strcmp(encrypted_input, encrypted) == 0);
}
