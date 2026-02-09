/**
 * 期末成绩管理系统 - C语言控制台版
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_STUDENTS 100
#define ID_LEN 20
#define NAME_LEN 20
#define DATE_LEN 9

// 文件路径定义
#define FILENAME_BASIC "../dataset/StudentBasic.txt"
#define FILENAME_GRADE "../dataset/StudentGrade.txt"
#define FILENAME_PASSWORD "../dataset/password.txt"

// 学生基本情况结构体
typedef struct {
    char id[ID_LEN];
    char name[NAME_LEN];
    char sex[4];
    char birth_date[DATE_LEN];
    char enroll_date[DATE_LEN];
    int award_count;
    int makeup_count;
    int retain_count;
} StudentBasic;

// 学生成绩结构体
typedef struct {
    char id[ID_LEN];
    float computer_score;
    float math_score;
    float english_score;
    float pe_score;
    float average_score;
} StudentGrade;

// 全局变量
StudentBasic basics[MAX_STUDENTS];
StudentGrade grades[MAX_STUDENTS];
int student_count = 0;
char password[50] = "admin123";

/**
 * 从文件加载学生基本情况
 */
int load_student_basics() {
    FILE *fp = fopen(FILENAME_BASIC, "r");
    if (fp == NULL) {
        printf("无法打开学生基本情况文件！\n");
        return 0;
    }

    student_count = 0;
    while (fscanf(fp, "%s %s %s %s %s %d %d %d",
                 basics[student_count].id,
                 basics[student_count].name,
                 basics[student_count].sex,
                 basics[student_count].birth_date,
                 basics[student_count].enroll_date,
                 &basics[student_count].award_count,
                 &basics[student_count].makeup_count,
                 &basics[student_count].retain_count) == 8) {
        student_count++;
        if (student_count >= MAX_STUDENTS) {
            break;
        }
    }

    fclose(fp);
    return student_count;
}

/**
 * 从文件加载学生成绩
 */
int load_student_grades() {
    FILE *fp = fopen(FILENAME_GRADE, "r");
    if (fp == NULL) {
        printf("无法打开学生成绩文件！\n");
        return 0;
    }

    int grade_count = 0;
    while (fscanf(fp, "%s %f %f %f %f %f",
                 grades[grade_count].id,
                 &grades[grade_count].computer_score,
                 &grades[grade_count].math_score,
                 &grades[grade_count].english_score,
                 &grades[grade_count].pe_score,
                 &grades[grade_count].average_score) == 6) {
        grade_count++;
        if (grade_count >= MAX_STUDENTS) {
            break;
        }
    }

    fclose(fp);
    return grade_count;
}

/**
 * 验证密码
 */
int verify_password() {
    printf("请输入密码：");
    char input[50];
    scanf("%s", input);
    return strcmp(input, password) == 0;
}

/**
 * 验证手机号码格式
 */
int validate_phone(const char *phone) {
    if (strlen(phone) != 11) {
        return 0;
    }
    for (int i = 0; i < 11; i++) {
        if (!isdigit(phone[i])) {
            return 0;
        }
    }
    return 1;
}

/**
 * 验证出生日期格式（YYYYMMDD）
 */
int validate_birth_date(const char *date) {
    if (strlen(date) != 8) {
        return 0;
    }
    for (int i = 0; i < 8; i++) {
        if (!isdigit(date[i])) {
            return 0;
        }
    }

    // 验证月份
    int month = atoi(date + 4);
    if (month < 1 || month > 12) {
        return 0;
    }

    // 验证日期
    int day = atoi(date + 6);
    if (day < 1 || day > 31) {
        return 0;
    }

    return 1;
}

/**
 * 按学号查询学生基本情况
 */
void query_student_basic() {
    char id[ID_LEN];
    printf("\n请输入学号：");
    scanf("%s", id);

    for (int i = 0; i < student_count; i++) {
        if (strcmp(basics[i].id, id) == 0) {
            printf("\n=== 学生基本信息 ===\n");
            printf("学号：%s\n", basics[i].id);
            printf("姓名：%s\n", basics[i].name);
            printf("性别：%s\n", basics[i].sex);
            printf("出生日期：%s\n", basics[i].birth_date);
            printf("入学日期：%s\n", basics[i].enroll_date);
            printf("受奖次数：%d\n", basics[i].award_count);
            printf("补考次数：%d\n", basics[i].makeup_count);
            printf("留级次数：%d\n", basics[i].retain_count);
            return;
        }
    }
    printf("未找到该学生！\n");
}

/**
 * 按学号查询学生成绩
 */
void query_student_grade() {
    char id[ID_LEN];
    printf("\n请输入学号：");
    scanf("%s", id);

    for (int i = 0; i < student_count; i++) {
        if (strcmp(grades[i].id, id) == 0) {
            printf("\n=== 学生成绩 ===\n");
            printf("学号：%s\n", grades[i].id);
            printf("计算机成绩：%.2f\n", grades[i].computer_score);
            printf("高等数学成绩：%.2f\n", grades[i].math_score);
            printf("外语成绩：%.2f\n", grades[i].english_score);
            printf("体育成绩：%.2f\n", grades[i].pe_score);
            printf("平均成绩：%.2f\n", grades[i].average_score);
            return;
        }
    }
    printf("未找到该学生！\n");
}

/**
 * 显示所有学生成绩一览表
 */
void show_all_grades() {
    printf("\n=== 期末成绩一览表 ===\n");
    printf("%-8s %-10s %-8s %-8s %-8s %-8s %-8s\n",
           "学号", "姓名", "计算机", "高等数学", "外语", "体育", "平均分");

    for (int i = 0; i < student_count; i++) {
        for (int j = 0; j < student_count; j++) {
            if (strcmp(basics[j].id, grades[i].id) == 0) {
                printf("%-8s %-10s %-8.2f %-8.2f %-8.2f %-8.2f %-8.2f\n",
                       grades[i].id,
                       basics[j].name,
                       grades[i].computer_score,
                       grades[i].math_score,
                       grades[i].english_score,
                       grades[i].pe_score,
                       grades[i].average_score);
                break;
            }
        }
    }
}

/**
 * 显示受奖情况
 */
void show_awards() {
    printf("\n=== 受奖情况 ===\n");
    printf("%-8s %-10s %-8s %-8s %-8s %-8s %-8s %-10s\n",
           "学号", "姓名", "计算机", "高等数学", "外语", "体育", "平均分", "奖励金额");

    for (int i = 0; i < student_count; i++) {
        float avg = grades[i].average_score;
        int award = 0;
        char award_str[20] = "无";

        if (avg >= 95) {
            award = 1200;
            strcpy(award_str, "1200元");
        } else if (avg >= 90) {
            award = 800;
            strcpy(award_str, "800元");
        } else if (avg >= 85) {
            award = 400;
            strcpy(award_str, "400元");
        }

        if (award > 0) {
            for (int j = 0; j < student_count; j++) {
                if (strcmp(basics[j].id, grades[i].id) == 0) {
                    printf("%-8s %-10s %-8.2f %-8.2f %-8.2f %-8.2f %-8.2f %-10s\n",
                           grades[i].id,
                           basics[j].name,
                           grades[i].computer_score,
                           grades[i].math_score,
                           grades[i].english_score,
                           grades[i].pe_score,
                           grades[i].average_score,
                           award_str);
                    break;
                }
            }
        }
    }
}

/**
 * 比较函数，用于排序
 */
int compare_average(const void *a, const void *b) {
    StudentGrade *ga = (StudentGrade *)a;
    StudentGrade *gb = (StudentGrade *)b;
    if (ga->average_score > gb->average_score) return -1;
    if (ga->average_score < gb->average_score) return 1;
    return 0;
}

/**
 * 按平均成绩从高到低排序
 */
void sort_by_average() {
    qsort(grades, student_count, sizeof(StudentGrade), compare_average);

    printf("\n=== 按平均成绩从高到低排序 ===\n");
    printf("%-8s %-10s %-8s %-8s %-8s %-8s %-8s\n",
           "学号", "姓名", "计算机", "高等数学", "外语", "体育", "平均分");

    for (int i = 0; i < student_count; i++) {
        for (int j = 0; j < student_count; j++) {
            if (strcmp(basics[j].id, grades[i].id) == 0) {
                printf("%-8s %-10s %-8.2f %-8.2f %-8.2f %-8.2f %-8.2f\n",
                       grades[i].id,
                       basics[j].name,
                       grades[i].computer_score,
                       grades[i].math_score,
                       grades[i].english_score,
                       grades[i].pe_score,
                       grades[i].average_score);
                break;
            }
        }
    }
}

/**
 * 统计各科平均分
 */
void statistics_average() {
    float sum_computer = 0, sum_math = 0, sum_english = 0, sum_pe = 0;

    for (int i = 0; i < student_count; i++) {
        sum_computer += grades[i].computer_score;
        sum_math += grades[i].math_score;
        sum_english += grades[i].english_score;
        sum_pe += grades[i].pe_score;
    }

    printf("\n=== 各科平均分 ===\n");
    printf("计算机平均分：%.2f\n", sum_computer / student_count);
    printf("高等数学平均分：%.2f\n", sum_math / student_count);
    printf("外语平均分：%.2f\n", sum_english / student_count);
    printf("体育平均分：%.2f\n", sum_pe / student_count);
}

/**
 * 统计各科最高分和最低分
 */
void statistics_max_min() {
    float max_computer = grades[0].computer_score;
    float min_computer = grades[0].computer_score;
    float max_math = grades[0].math_score;
    float min_math = grades[0].math_score;
    float max_english = grades[0].english_score;
    float min_english = grades[0].english_score;
    float max_pe = grades[0].pe_score;
    float min_pe = grades[0].pe_score;

    for (int i = 1; i < student_count; i++) {
        if (grades[i].computer_score > max_computer) max_computer = grades[i].computer_score;
        if (grades[i].computer_score < min_computer) min_computer = grades[i].computer_score;
        if (grades[i].math_score > max_math) max_math = grades[i].math_score;
        if (grades[i].math_score < min_math) min_math = grades[i].math_score;
        if (grades[i].english_score > max_english) max_english = grades[i].english_score;
        if (grades[i].english_score < min_english) min_english = grades[i].english_score;
        if (grades[i].pe_score > max_pe) max_pe = grades[i].pe_score;
        if (grades[i].pe_score < min_pe) min_pe = grades[i].pe_score;
    }

    printf("\n=== 各科最高分和最低分 ===\n");
    printf("计算机：最高分%.2f，最低分%.2f\n", max_computer, min_computer);
    printf("高等数学：最高分%.2f，最低分%.2f\n", max_math, min_math);
    printf("外语：最高分%.2f，最低分%.2f\n", max_english, min_english);
    printf("体育：最高分%.2f，最低分%.2f\n", max_pe, min_pe);
}

/**
 * 统计各科各级别人数
 */
void statistics_grades() {
    int computer[5] = {0}, math[5] = {0}, english[5] = {0}, pe[5] = {0};
    char *levels[] = {"优(90+)", "良(80-89)", "中(70-79)", "及格(60-69)", "不及格(<60)"};

    for (int i = 0; i < student_count; i++) {
        // 计算机
        if (grades[i].computer_score >= 90) computer[0]++;
        else if (grades[i].computer_score >= 80) computer[1]++;
        else if (grades[i].computer_score >= 70) computer[2]++;
        else if (grades[i].computer_score >= 60) computer[3]++;
        else computer[4]++;

        // 高等数学
        if (grades[i].math_score >= 90) math[0]++;
        else if (grades[i].math_score >= 80) math[1]++;
        else if (grades[i].math_score >= 70) math[2]++;
        else if (grades[i].math_score >= 60) math[3]++;
        else math[4]++;

        // 外语
        if (grades[i].english_score >= 90) english[0]++;
        else if (grades[i].english_score >= 80) english[1]++;
        else if (grades[i].english_score >= 70) english[2]++;
        else if (grades[i].english_score >= 60) english[3]++;
        else english[4]++;

        // 体育
        if (grades[i].pe_score >= 90) pe[0]++;
        else if (grades[i].pe_score >= 80) pe[1]++;
        else if (grades[i].pe_score >= 70) pe[2]++;
        else if (grades[i].pe_score >= 60) pe[3]++;
        else pe[4]++;
    }

    printf("\n=== 各科各级别人数 ===\n");
    printf("%-12s %-8s %-8s %-8s %-8s\n", "等级", "计算机", "高等数学", "外语", "体育");
    for (int i = 0; i < 5; i++) {
        printf("%-12s %-8d %-8d %-8d %-8d\n", levels[i], computer[i], math[i], english[i], pe[i]);
    }
}

/**
 * 统计留级和退学人数
 */
void statistics_retain_drop() {
    int retain_count = 0;
    int makeup_count = 0;
    int drop_count = 0;

    for (int i = 0; i < student_count; i++) {
        if (basics[i].retain_count > 0) retain_count++;
        if (basics[i].makeup_count > 0) makeup_count++;
        if (basics[i].retain_count >= 2 || basics[i].makeup_count >= 8) {
            drop_count++;
        }
    }

    printf("\n=== 留级与退学统计 ===\n");
    printf("留级人数：%d\n", retain_count);
    printf("补考人数：%d\n", makeup_count);
    printf("退学人数：%d\n", drop_count);
}

/**
 * 判断是否需要补考或留级
 */
void check_failures() {
    printf("\n=== 补考与留级判断 ===\n");

    for (int i = 0; i < student_count; i++) {
        int fail_computer = grades[i].computer_score < 60;
        int fail_math = grades[i].math_score < 60;
        int fail_english = grades[i].english_score < 60;
        int fail_pe = grades[i].pe_score < 60;

        for (int j = 0; j < student_count; j++) {
            if (strcmp(basics[j].id, grades[i].id) == 0) {
                printf("学号：%s，姓名：%s\n", grades[i].id, basics[j].name);

                if (fail_computer || fail_math || fail_english || fail_pe) {
                    printf("  需要补考：");
                    if (fail_computer) printf("计算机 ");
                    if (fail_math) printf("高等数学 ");
                    if (fail_english) printf("外语 ");
                    if (fail_pe) printf("体育 ");
                    printf("\n");

                    if (fail_computer && fail_math && fail_english) {
                        printf("  警告：三门主科均不及格，需留级！\n");
                    }
                } else {
                    printf("  全科及格\n");
                }

                if (basics[j].retain_count >= 2) {
                    printf("  警告：留级次数已达%d次，需退学！\n", basics[j].retain_count);
                }
                if (basics[j].makeup_count >= 8) {
                    printf("  警告：补考次数已达%d次，需退学！\n", basics[j].makeup_count);
                }

                printf("\n");
                break;
            }
        }
    }
}

/**
 * 录入学生成绩
 */
void input_grade() {
    char id[ID_LEN];
    float computer, math, english, pe, average;

    printf("\n请输入学号：");
    scanf("%s", id);

    // 检查学生是否存在
    int found = 0;
    for (int i = 0; i < student_count; i++) {
        if (strcmp(basics[i].id, id) == 0) {
            found = 1;
            break;
        }
    }

    if (!found) {
        printf("该学生不存在！\n");
        return;
    }

    printf("请输入计算机成绩：");
    scanf("%f", &computer);
    printf("请输入高等数学成绩：");
    scanf("%f", &math);
    printf("请输入外语成绩：");
    scanf("%f", &english);
    printf("请输入体育成绩：");
    scanf("%f", &pe);

    average = (computer + math + english + pe) / 4;

    // 查找并更新或添加成绩
    int grade_index = -1;
    for (int i = 0; i < student_count; i++) {
        if (strcmp(grades[i].id, id) == 0) {
            grade_index = i;
            break;
        }
    }

    if (grade_index >= 0) {
        grades[grade_index].computer_score = computer;
        grades[grade_index].math_score = math;
        grades[grade_index].english_score = english;
        grades[grade_index].pe_score = pe;
        grades[grade_index].average_score = average;
        printf("成绩已更新！\n");
    } else if (student_count < MAX_STUDENTS) {
        strcpy(grades[student_count].id, id);
        grades[student_count].computer_score = computer;
        grades[student_count].math_score = math;
        grades[student_count].english_score = english;
        grades[student_count].pe_score = pe;
        grades[student_count].average_score = average;
        student_count++;
        printf("成绩已录入！\n");
    } else {
        printf("学生人数已达上限！\n");
    }

    // 保存到文件
    FILE *fp = fopen(FILENAME_GRADE, "w");
    if (fp != NULL) {
        for (int i = 0; i < student_count; i++) {
            fprintf(fp, "%s %.2f %.2f %.2f %.2f %.2f\n",
                    grades[i].id,
                    grades[i].computer_score,
                    grades[i].math_score,
                    grades[i].english_score,
                    grades[i].pe_score,
                    grades[i].average_score);
        }
        fclose(fp);
    }
}

/**
 * 显示主菜单
 */
void show_menu() {
    printf("\n");
    printf("========================================\n");
    printf("       期末成绩管理系统\n");
    printf("========================================\n");
    printf("1. 录入学生成绩\n");
    printf("2. 查询学生基本情况\n");
    printf("3. 查询学生成绩\n");
    printf("4. 显示所有成绩一览表\n");
    printf("5. 显示受奖情况\n");
    printf("6. 按平均成绩排序\n");
    printf("7. 统计各科平均分\n");
    printf("8. 统计各科最高最低分\n");
    printf("9. 统计各科各级别人数\n");
    printf("10. 统计留级退学人数\n");
    printf("11. 判断补考与留级\n");
    printf("0. 退出系统\n");
    printf("========================================\n");
    printf("请选择功能（0-11）：");
}

/**
 * 主函数
 */
int main() {
    // 登录验证
    printf("========================================\n");
    printf("       期末成绩管理系统\n");
    printf("========================================\n");
    if (!verify_password()) {
        printf("密码错误，系统退出！\n");
        return 1;
    }
    printf("登录成功！\n");

    // 加载数据
    load_student_basics();
    load_student_grades();

    // 主循环
    int choice;
    while (1) {
        show_menu();
        scanf("%d", &choice);

        switch (choice) {
            case 0:
                printf("感谢使用，再见！\n");
                return 0;
            case 1:
                input_grade();
                break;
            case 2:
                query_student_basic();
                break;
            case 3:
                query_student_grade();
                break;
            case 4:
                show_all_grades();
                break;
            case 5:
                show_awards();
                break;
            case 6:
                sort_by_average();
                break;
            case 7:
                statistics_average();
                break;
            case 8:
                statistics_max_min();
                break;
            case 9:
                statistics_grades();
                break;
            case 10:
                statistics_retain_drop();
                break;
            case 11:
                check_failures();
                break;
            default:
                printf("无效的选择！\n");
        }
    }

    return 0;
}
