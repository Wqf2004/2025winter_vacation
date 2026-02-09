#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <conio.h>
#include <windows.h>
#include <time.h>

#define MAX_EMPLOYEES 500
#define FILENAME_EMP "../dataset/EmpBasic.txt"
#define FILENAME_ATT "../dataset/Attendance.txt"
#define FILENAME_PUNCH "../dataset/punchIn.txt"
#define FILENAME_MONTH "../dataset/MonthPunchIn.txt"
#define FILENAME_PWD "../dataset/password.txt"

// 职工基本信息结构体
typedef struct Employee {
    char id[20];
    char name[20];
    char sex[10];
    char birth_date[12];
    char level[20];
    char department[30];
} Employee;

// 职工月出勤情况结构体
typedef struct Attendance {
    char id[20];
    int late_count;
    int leave_days;
    int absent_days;
} Attendance;

// 当日出勤记录结构体
typedef struct PunchRecord {
    char id[20];
    int hour;
    int minute;
    int second;
} PunchRecord;

// 函数声明
int readEmployees(Employee *employees);
int readAttendance(Attendance *attendances);
int readPunchRecords(PunchRecord *records);
void saveAttendance(Attendance *attendances, int count);
void saveToMonthPunchIn(PunchRecord *records, int count);
void showMainMenu();
void showQueryMenu();
void showLeaveMenu();
void showStatisticsMenu();
void showSortMenu();
int login();
void printMenuHeader(const char *title);
void printMenuFooter();
void processPunchRecords(Employee *employees, int emp_count, Attendance *attendances, int att_count);
void queryEmployeeInfo(Employee *employees, int emp_count, Attendance *attendances, int att_count, PunchRecord *records, int record_count);
void listPerfectAttendance(Employee *employees, int emp_count, Attendance *attendances, int att_count);
void listExcessiveLeave(Employee *employees, int emp_count, Attendance *attendances, int att_count);
void listAbsentEmployees(Employee *employees, int emp_count, Attendance *attendances, int att_count);
void manageLeave(Employee *employees, int emp_count, Attendance *attendances, int att_count);
void showStatistics(Employee *employees, int emp_count, Attendance *attendances, int att_count, PunchRecord *records, int record_count);
void showSortFunctions(Employee *employees, int emp_count, PunchRecord *records, int record_count);
int calculateAge(const char *birth_date);
int getAllowedLeaveDays(Employee *employee);
int validateBirthDate(const char *date);
int getBirthMonth(const char *birth_date);
int getCurrentMonth();

// 主函数
int main() {
    if (!login()) {
        return 0;
    }

    Employee employees[MAX_EMPLOYEES];
    Attendance attendances[MAX_EMPLOYEES];
    PunchRecord records[MAX_EMPLOYEES];

    int emp_count = readEmployees(employees);
    int att_count = readAttendance(attendances);
    int record_count = readPunchRecords(records);

    char choice;
    char sub_choice;

    while (1) {
        showMainMenu();
        choice = getch();

        switch (choice) {
            case '1':
                printf("\n正在读取当日打卡记录...\n");
                processPunchRecords(employees, emp_count, attendances, att_count);
                saveAttendance(attendances, att_count);
                saveToMonthPunchIn(records, record_count);
                printf("\n打卡记录处理完成！已更新月出勤情况文件。\n");
                printf("\n按任意键继续...");
                getch();
                break;
            case '2':
                while (1) {
                    showQueryMenu();
                    sub_choice = getch();
                    printf("%c\n", sub_choice);

                    switch (sub_choice) {
                        case '1':
                            queryEmployeeInfo(employees, emp_count, attendances, att_count, records, record_count);
                            break;
                        case '2':
                            listPerfectAttendance(employees, emp_count, attendances, att_count);
                            break;
                        case '3':
                            listExcessiveLeave(employees, emp_count, attendances, att_count);
                            break;
                        case '4':
                            listAbsentEmployees(employees, emp_count, attendances, att_count);
                            break;
                        case '0':
                            goto exit_query;
                        default:
                            printf("无效选择，请重新输入！\n");
                    }
                    printf("\n按任意键继续...");
                    getch();
                }
            exit_query:
                break;
            case '3':
                manageLeave(employees, emp_count, attendances, att_count);
                saveAttendance(attendances, att_count);
                break;
            case '4':
                showStatistics(employees, emp_count, attendances, att_count, records, record_count);
                break;
            case '5':
                showSortFunctions(employees, emp_count, records, record_count);
                break;
            case '0':
                printf("\n感谢使用出勤管理系统，再见！\n");
                return 0;
            default:
                printf("\n无效选择，请重新输入！\n");
                Sleep(1000);
        }
    }

    return 0;
}

// 登录函数
int login() {
    char password[50];
    char stored_password[50];

    FILE *fp = fopen(FILENAME_PWD, "r");
    if (!fp) {
        printf("错误：无法读取密码文件！\n");
        return 0;
    }
    fscanf(fp, "%s", stored_password);
    fclose(fp);

    printf("========================================\n");
    printf("       出勤管理系统\n");
    printf("========================================\n\n");

    int attempts = 3;
    while (attempts > 0) {
        printf("请输入密码（剩余尝试次数：%d）：", attempts);
        scanf("%s", password);

        if (strcmp(password, stored_password) == 0) {
            printf("\n登录成功！\n");
            Sleep(1000);
            return 1;
        } else {
            printf("密码错误！\n\n");
            attempts--;
        }
    }

    printf("登录失败，系统退出。\n");
    return 0;
}

// 显示主菜单
void showMainMenu() {
    system("cls");
    printMenuHeader("出勤管理系统");
    printf("  1 - 读取当日打卡记录\n");
    printf("  2 - 查询功能\n");
    printf("  3 - 请假管理\n");
    printf("  4 - 统计功能\n");
    printf("  5 - 排序功能\n");
    printf("  0 - 退出系统\n");
    printMenuFooter();
    printf("  请选择操作：");
}

// 显示查询菜单
void showQueryMenu() {
    system("cls");
    printMenuHeader("查询功能");
    printf("  1 - 按职工编号查询\n");
    printf("  2 - 列出所有全勤职工\n");
    printf("  3 - 列出请假天数超过5天的职工\n");
    printf("  4 - 列出有旷工行为的职工\n");
    printf("  0 - 返回主菜单\n");
    printMenuFooter();
    printf("  请选择操作：");
}

// 显示请假管理菜单
void showLeaveMenu() {
    system("cls");
    printMenuHeader("请假管理");
    printf("  0 - 返回主菜单\n");
    printf("  1 - 录入请假信息\n");
    printMenuFooter();
    printf("  请选择操作：");
}

// 显示统计菜单
void showStatisticsMenu() {
    system("cls");
    printMenuHeader("统计功能");
    printf("  0 - 返回主菜单\n");
    printf("  1 - 显示所有统计信息\n");
    printMenuFooter();
    printf("  请选择操作：");
}

// 显示排序菜单
void showSortMenu() {
    system("cls");
    printMenuHeader("排序功能");
    printf("  0 - 返回主菜单\n");
    printf("  1 - 最早到厂的职工\n");
    printf("  2 - 按出生日期升序输出全体职工\n");
    printf("  3 - 按出生日期降序列出全体女职工\n");
    printMenuFooter();
    printf("  请选择操作：");
}

// 打印菜单头部
void printMenuHeader(const char *title) {
    printf("========================================\n");
    printf("       %s\n", title);
    printf("========================================\n");
}

// 打印菜单底部
void printMenuFooter() {
    printf("----------------------------------------\n");
}

// 读取职工信息
int readEmployees(Employee *employees) {
    FILE *fp = fopen(FILENAME_EMP, "r");
    if (!fp) {
        printf("错误：无法读取职工信息文件！\n");
        return 0;
    }

    int count = 0;
    while (fscanf(fp, "%s %s %s %s %s %s",
                  employees[count].id,
                  employees[count].name,
                  employees[count].sex,
                  employees[count].birth_date,
                  employees[count].level,
                  employees[count].department) == 6) {
        count++;
    }

    fclose(fp);
    return count;
}

// 读取出勤信息
int readAttendance(Attendance *attendances) {
    FILE *fp = fopen(FILENAME_ATT, "r");
    if (!fp) {
        printf("错误：无法读取出勤信息文件！\n");
        return 0;
    }

    int count = 0;
    while (fscanf(fp, "%s %d %d %d",
                  attendances[count].id,
                  &attendances[count].late_count,
                  &attendances[count].leave_days,
                  &attendances[count].absent_days) == 4) {
        count++;
    }

    fclose(fp);
    return count;
}

// 读取打卡记录
int readPunchRecords(PunchRecord *records) {
    FILE *fp = fopen(FILENAME_PUNCH, "r");
    if (!fp) {
        printf("错误：无法读取打卡记录文件！\n");
        return 0;
    }

    int count = 0;
    while (fscanf(fp, "%s %d %d %d",
                  records[count].id,
                  &records[count].hour,
                  &records[count].minute,
                  &records[count].second) == 4) {
        count++;
    }

    fclose(fp);
    return count;
}

// 保存出勤信息
void saveAttendance(Attendance *attendances, int count) {
    FILE *fp = fopen(FILENAME_ATT, "w");
    if (!fp) {
        printf("错误：无法保存出勤信息！\n");
        return;
    }

    for (int i = 0; i < count; i++) {
        fprintf(fp, "%s %d %d %d\n",
                attendances[i].id,
                attendances[i].late_count,
                attendances[i].leave_days,
                attendances[i].absent_days);
    }

    fclose(fp);
}

// 保存到月打卡记录
void saveToMonthPunchIn(PunchRecord *records, int count) {
    FILE *fp = fopen(FILENAME_MONTH, "a");
    if (!fp) {
        printf("错误：无法保存月打卡记录！\n");
        return;
    }

    for (int i = 0; i < count; i++) {
        fprintf(fp, "%s %d %d %d\n",
                records[i].id,
                records[i].hour,
                records[i].minute,
                records[i].second);
    }

    fclose(fp);
}

// 处理打卡记录
void processPunchRecords(Employee *employees, int emp_count, Attendance *attendances, int att_count) {
    PunchRecord records[MAX_EMPLOYEES];
    int record_count = readPunchRecords(records);

    for (int i = 0; i < emp_count; i++) {
        int punched = 0;
        int late_time = 0;

        for (int j = 0; j < record_count; j++) {
            if (strcmp(employees[i].id, records[j].id) == 0) {
                punched = 1;

                int arrival_time = records[j].hour * 3600 + records[j].minute * 60 + records[j].second;
                int standard_time = 8 * 3600;

                if (arrival_time > standard_time) {
                    late_time = arrival_time - standard_time;
                }

                break;
            }
        }

        int att_index = -1;
        for (int k = 0; k < att_count; k++) {
            if (strcmp(attendances[k].id, employees[i].id) == 0) {
                att_index = k;
                break;
            }
        }

        if (att_index != -1) {
            if (!punched || late_time >= 3600) {
                attendances[att_index].absent_days++;
            } else if (late_time > 0) {
                int late_minutes = late_time / 60;
                int late_count = (late_minutes + 9) / 10;
                attendances[att_index].late_count += late_count;
            }
        }
    }
}

// 查询职工信息
void queryEmployeeInfo(Employee *employees, int emp_count, Attendance *attendances, int att_count, PunchRecord *records, int record_count) {
    char id[20];
    printf("\n请输入职工编号：");
    scanf("%s", id);

    for (int i = 0; i < emp_count; i++) {
        if (strcmp(employees[i].id, id) == 0) {
            printf("\n职工信息：\n");
            printf("  编号：%s\n", employees[i].id);
            printf("  姓名：%s\n", employees[i].name);
            printf("  性别：%s\n", employees[i].sex);
            printf("  出生日期：%s\n", employees[i].birth_date);
            printf("  职务级别：%s\n", employees[i].level);
            printf("  所在部门：%s\n", employees[i].department);

            int found = 0;
            for (int j = 0; j < record_count; j++) {
                if (strcmp(records[j].id, id) == 0) {
                    printf("\n当日到厂时间：%02d:%02d:%02d\n", records[j].hour, records[j].minute, records[j].second);
                    found = 1;
                    break;
                }
            }
            if (!found) {
                printf("\n当日未打卡\n");
            }

            for (int j = 0; j < att_count; j++) {
                if (strcmp(attendances[j].id, id) == 0) {
                    printf("\n当月出勤情况：\n");
                    printf("  迟到次数：%d\n", attendances[j].late_count);
                    printf("  请假天数：%d\n", attendances[j].leave_days);
                    printf("  旷工天数：%d\n", attendances[j].absent_days);
                    break;
                }
            }
            return;
        }
    }

    printf("\n未找到该职工！\n");
}

// 列出所有全勤职工
void listPerfectAttendance(Employee *employees, int emp_count, Attendance *attendances, int att_count) {
    printf("\n全勤职工清单：\n");
    printf("----------------------------------------\n");
    printf("编号    姓名    性别    出生日期\n");

    int count = 0;
    for (int i = 0; i < emp_count; i++) {
        for (int j = 0; j < att_count; j++) {
            if (strcmp(employees[i].id, attendances[j].id) == 0) {
                if (attendances[j].late_count == 0 && attendances[j].leave_days == 0 && attendances[j].absent_days == 0) {
                    printf("%-8s%-8s%-8s%s\n", employees[i].id, employees[i].name, employees[i].sex, employees[i].birth_date);
                    count++;
                }
                break;
            }
        }
    }

    if (count == 0) {
        printf("\n暂无全勤职工\n");
    } else {
        printf("\n共 %d 名全勤职工\n", count);
    }
}

// 列出请假天数超过5天的职工
void listExcessiveLeave(Employee *employees, int emp_count, Attendance *attendances, int att_count) {
    printf("\n请假天数超过5天的职工（扣除允许请假天数后）：\n");
    printf("------------------------------------------------------------\n");
    printf("编号    姓名    性别    出生日期    允许请假天数    实际请假天数    超出天数\n");

    int count = 0;
    for (int i = 0; i < emp_count; i++) {
        for (int j = 0; j < att_count; j++) {
            if (strcmp(employees[i].id, attendances[j].id) == 0) {
                int allowed = getAllowedLeaveDays(&employees[i]);
                int exceeded = attendances[j].leave_days - allowed;

                if (exceeded > 5) {
                    printf("%-8s%-8s%-8s%-12s%-16d%-16d%d\n",
                           employees[i].id,
                           employees[i].name,
                           employees[i].sex,
                           employees[i].birth_date,
                           allowed,
                           attendances[j].leave_days,
                           exceeded);
                    count++;
                }
                break;
            }
        }
    }

    if (count == 0) {
        printf("\n暂无请假天数超过5天的职工\n");
    } else {
        printf("\n共 %d 名职工请假天数超过5天\n", count);
    }
}

// 列出有旷工行为的职工
void listAbsentEmployees(Employee *employees, int emp_count, Attendance *attendances, int att_count) {
    printf("\n有旷工行为的职工：\n");
    printf("------------------------------------------------------------\n");
    printf("编号    姓名    性别    出生日期    迟到次数    请假天数    旷工天数\n");

    int count = 0;
    for (int i = 0; i < emp_count; i++) {
        for (int j = 0; j < att_count; j++) {
            if (strcmp(employees[i].id, attendances[j].id) == 0) {
                if (attendances[j].absent_days > 0) {
                    printf("%-8s%-8s%-8s%-12s%-12d%-12d%d\n",
                           employees[i].id,
                           employees[i].name,
                           employees[i].sex,
                           employees[i].birth_date,
                           attendances[j].late_count,
                           attendances[j].leave_days,
                           attendances[j].absent_days);
                    count++;
                }
                break;
            }
        }
    }

    if (count == 0) {
        printf("\n暂无旷工记录\n");
    } else {
        printf("\n共 %d 名职工有旷工行为\n", count);
    }
}

// 请假管理
void manageLeave(Employee *employees, int emp_count, Attendance *attendances, int att_count) {
    char choice;

    while (1) {
        showLeaveMenu();
        choice = getch();
        printf("%c\n", choice);

        if (choice == '0') {
            break;
        }

        if (choice == '1') {
            char id[20];
            printf("\n请输入请假职工的编号：");
            scanf("%s", id);

            int found = 0;
            for (int i = 0; i < emp_count; i++) {
                if (strcmp(employees[i].id, id) == 0) {
                    found = 1;
                    printf("\n职工信息：\n");
                    printf("  编号：%s\n", employees[i].id);
                    printf("  姓名：%s\n", employees[i].name);
                    break;
                }
            }

            if (!found) {
                printf("\n未找到该职工！\n");
                printf("\n按任意键继续...");
                getch();
                continue;
            }

            for (int j = 0; j < att_count; j++) {
                if (strcmp(attendances[j].id, id) == 0) {
                    attendances[j].leave_days++;
                    if (attendances[j].absent_days > 0) {
                        attendances[j].absent_days--;
                    }
                    printf("\n请假信息已更新：\n");
                    printf("  请假天数：%d\n", attendances[j].leave_days);
                    printf("  旷工天数：%d\n", attendances[j].absent_days);
                    break;
                }
            }
        } else {
            printf("无效选择！\n");
        }

        printf("\n按任意键继续...");
        getch();
    }
}

// 统计功能
void showStatistics(Employee *employees, int emp_count, Attendance *attendances, int att_count, PunchRecord *records, int record_count) {
    char choice;

    while (1) {
        showStatisticsMenu();
        choice = getch();
        printf("%c\n", choice);

        if (choice == '0') {
            break;
        }

        if (choice == '1') {
            printf("\n========== 统计信息 ==========\n");

            int total_employees = emp_count;
            int perfect_count = 0;
            int max_late_minutes = 0;
            int max_leave_days = 0;
            int max_late_count = 0;
            int max_absent_days = 0;
            int late_today_count = 0;

            for (int i = 0; i < emp_count; i++) {
                for (int j = 0; j < att_count; j++) {
                    if (strcmp(employees[i].id, attendances[j].id) == 0) {
                        if (attendances[j].late_count == 0 && attendances[j].leave_days == 0 && attendances[j].absent_days == 0) {
                            perfect_count++;
                        }
                        if (attendances[j].leave_days > max_leave_days) {
                            max_leave_days = attendances[j].leave_days;
                        }
                        if (attendances[j].late_count > max_late_count) {
                            max_late_count = attendances[j].late_count;
                        }
                        if (attendances[j].absent_days > max_absent_days) {
                            max_absent_days = attendances[j].absent_days;
                        }
                        break;
                    }
                }
            }

            for (int i = 0; i < record_count; i++) {
                int arrival_time = records[i].hour * 3600 + records[i].minute * 60 + records[i].second;
                int standard_time = 8 * 3600;

                if (arrival_time > standard_time) {
                    int late_time = arrival_time - standard_time;
                    if (late_time > max_late_minutes) {
                        max_late_minutes = late_time;
                    }
                    late_today_count++;
                }
            }

            float perfect_rate = (float)perfect_count / total_employees * 100;
            float late_today_rate = (float)late_today_count / total_employees * 100;

            printf("\n[基本统计]\n");
            printf("  当前职工总数：%d\n", total_employees);
            printf("  当月全勤职工总数：%d\n", perfect_count);
            printf("  全勤率：%.2f%%\n", perfect_rate);

            printf("\n[当日统计]\n");
            printf("  当日最长迟到时间：%d分钟\n", max_late_minutes / 60);
            printf("  当日迟到职工总数：%d\n", late_today_count);
            printf("  当日迟到率：%.2f%%\n", late_today_rate);

            printf("\n[当月统计]\n");
            printf("  当月最大请假天数：%d天\n", max_leave_days);
            printf("  当月最大迟到次数：%d次\n", max_late_count);
            printf("  当月最大旷工天数：%d天\n", max_absent_days);
        } else {
            printf("无效选择！\n");
        }

        printf("\n按任意键继续...");
        getch();
    }
}

// 排序功能
void showSortFunctions(Employee *employees, int emp_count, PunchRecord *records, int record_count) {
    char choice;

    while (1) {
        showSortMenu();
        choice = getch();
        printf("%c\n", choice);

        if (choice == '0') {
            break;
        }

        if (choice == '1') {
            int earliest_time = 24 * 3600;
            char earliest_id[20] = {0};
            int earliest_hour = 0, earliest_minute = 0, earliest_second = 0;

            for (int i = 0; i < record_count; i++) {
                int arrival_time = records[i].hour * 3600 + records[i].minute * 60 + records[i].second;
                if (arrival_time < earliest_time) {
                    earliest_time = arrival_time;
                    strcpy(earliest_id, records[i].id);
                    earliest_hour = records[i].hour;
                    earliest_minute = records[i].minute;
                    earliest_second = records[i].second;
                }
            }

            if (earliest_time < 24 * 3600) {
                for (int i = 0; i < emp_count; i++) {
                    if (strcmp(employees[i].id, earliest_id) == 0) {
                        printf("\n最早到厂的职工：\n");
                        printf("  编号：%s\n", employees[i].id);
                        printf("  姓名：%s\n", employees[i].name);
                        printf("  到厂时间：%02d:%02d:%02d\n", earliest_hour, earliest_minute, earliest_second);
                        break;
                    }
                }
            } else {
                printf("\n今日无打卡记录\n");
            }
        } else if (choice == '2') {
            printf("\n按出生日期升序输出全体职工基本信息：\n");
            printf("------------------------------------------------------------\n");
            printf("编号    姓名    性别    出生日期    职务级别    所在部门\n");

            int sorted_indices[MAX_EMPLOYEES];
            for (int i = 0; i < emp_count; i++) {
                sorted_indices[i] = i;
            }

            for (int i = 0; i < emp_count - 1; i++) {
                for (int j = 0; j < emp_count - 1 - i; j++) {
                    if (strcmp(employees[sorted_indices[j]].birth_date, employees[sorted_indices[j + 1]].birth_date) > 0) {
                        int temp = sorted_indices[j];
                        sorted_indices[j] = sorted_indices[j + 1];
                        sorted_indices[j + 1] = temp;
                    }
                }
            }

            for (int i = 0; i < emp_count; i++) {
                int idx = sorted_indices[i];
                printf("%-8s%-8s%-8s%-12s%-12s%s\n",
                       employees[idx].id,
                       employees[idx].name,
                       employees[idx].sex,
                       employees[idx].birth_date,
                       employees[idx].level,
                       employees[idx].department);
            }
        } else if (choice == '3') {
            printf("\n按出生日期降序列出全体女职工基本信息：\n");
            printf("------------------------------------------------------------\n");
            printf("编号    姓名    性别    出生日期    职务级别    所在部门\n");

            int female_indices[MAX_EMPLOYEES];
            int female_count = 0;
            for (int i = 0; i < emp_count; i++) {
                if (strcmp(employees[i].sex, "女") == 0) {
                    female_indices[female_count++] = i;
                }
            }

            for (int i = 0; i < female_count - 1; i++) {
                for (int j = 0; j < female_count - 1 - i; j++) {
                    if (strcmp(employees[female_indices[j]].birth_date, employees[female_indices[j + 1]].birth_date) < 0) {
                        int temp = female_indices[j];
                        female_indices[j] = female_indices[j + 1];
                        female_indices[j + 1] = temp;
                    }
                }
            }

            for (int i = 0; i < female_count; i++) {
                int idx = female_indices[i];
                printf("%-8s%-8s%-8s%-12s%-12s%s\n",
                       employees[idx].id,
                       employees[idx].name,
                       employees[idx].sex,
                       employees[idx].birth_date,
                       employees[idx].level,
                       employees[idx].department);
            }
        } else {
            printf("无效选择！\n");
        }

        printf("\n按任意键继续...");
        getch();
    }
}

// 计算年龄
int calculateAge(const char *birth_date) {
    time_t t = time(NULL);
    struct tm *tm = localtime(&t);
    int current_year = tm->tm_year + 1900;
    int current_month = tm->tm_mon + 1;
    int current_day = tm->tm_mday;

    int birth_year = atoi(birth_date);
    int birth_month = atoi(birth_date + 4);
    int birth_day = atoi(birth_date + 6);

    int age = current_year - birth_year;

    if (current_month < birth_month || (current_month == birth_month && current_day < birth_day)) {
        age--;
    }

    return age;
}

// 获取允许请假天数
int getAllowedLeaveDays(Employee *employee) {
    int allowed = 0;
    int age = calculateAge(employee->birth_date);

    if (strcmp(employee->sex, "女") == 0) {
        allowed += 3;
    }

    if (strcmp(employee->sex, "男") == 0 && age >= 55) {
        allowed += 2;
    }

    int current_month = getCurrentMonth();
    int birth_month = getBirthMonth(employee->birth_date);

    if (current_month == birth_month) {
        allowed += 1;
    }

    return allowed;
}

// 获取生日月份
int getBirthMonth(const char *birth_date) {
    return atoi(birth_date + 4);
}

// 获取当前月份
int getCurrentMonth() {
    time_t t = time(NULL);
    struct tm *tm = localtime(&t);
    return tm->tm_mon + 1;
}

// 验证出生日期格式
int validateBirthDate(const char *date) {
    if (strlen(date) != 8) {
        return 0;
    }

    for (int i = 0; i < 8; i++) {
        if (!isdigit(date[i])) {
            return 0;
        }
    }

    return 1;
}
