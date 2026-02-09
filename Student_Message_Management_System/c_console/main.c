#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <conio.h>
#include <windows.h>

#define MAX_STUDENTS 30
#define MAX_Grades 100
#define FILENAME_A "../dataset/a.txt" // 学生信息存储地址
#define FILENAME_B "../dataset/b.txt"  // 成绩信息存储地址
#define PASSWORD_FILE "../dataset/password.txt" // 密码文件

// 学生信息结构体
typedef struct student
{
	char id[10];
	char name[10];
	char sex[8];
	char room[8];
	char phone[20];
}Student;

// 成绩结构体
typedef struct grades
{
    char id[10];         // 学生学号
    char courseId[20];   // 课程代码
    char courseName[80]; // 课程名字
    float credits;         // 学分
    float usualScore;    // 平时成绩
    float labScore;      // 实验成绩
    float examScore;     // 卷面成绩
    float totalScore;    // 总评成绩
} Grades;

int readStudentsFromFile(char *FileName, Student *pStu);
void printStudent();
int checkStudentId(Student students[], int count, const char *id);
char* returnStudentName(Student students[], int count, const char *id);
float calculateTotalScore(float usual, float lab, float exam);
float calculateCredits(float credit, float totalScore);
void addGradesRecord(char *FileName_A, char* FileName_B, Student *student);
int readGradesFromFile(char *FileName, Grades *pGrd);
void queryStudentSmart();
void queryStudentsByDorm();
void queryScoresById();
void deleteStudent();
void sortGrades(int option);
int validatePhoneNumber(const char *phone);
int login();
void printMenuHeader(const char *title);
void printMenuFooter();
int compareTotalScoreAsc(const void *a, const void *b);
int compareTotalScoreDesc(const void *a, const void *b);
int compareCreditsAsc(const void *a, const void *b);
int compareCreditsDesc(const void *a, const void *b);

// 显示主菜单
void showMenu() {
    printMenuHeader("学生信息管理系统(SMMS)");
    printf("  L - 学生成绩数据录入\n");
    printf("  S - 学生成绩排序\n");
    printf("  A - 学生基本信息查询\n");
    printf("  B - 学生成绩信息查询\n");
    printf("  D - 学生信息删除\n");
    printf("  Q - 退出系统\n");
    printMenuFooter();
    printf("  请选择操作：");
}

// 显示学生成绩录入子菜单
void showGradeEntryMenu() {
    printMenuHeader("学生成绩录入");
    printf("  0 - 返回上一级\n");
    printf("  1 - 继续(开始)录入\n");
    printMenuFooter();
    printf("  请选择操作：");
}

// 显示学生基本情况查询子菜单
void showStudentMenu() {
    printMenuHeader("学生基本信息查询");
    printf("  0 - 返回上一级\n");
    printf("  1 - 按学号(或姓名)查询\n");
    printf("  2 - 按宿舍号查询\n");
    printMenuFooter();
    printf("  请选择操作：");
}

// 显示成绩查询子菜单
void showScoreMenu() {
    printMenuHeader("学生成绩信息查询");
    printf("  0 - 返回上一级\n");
    printf("  1 - 按学号查询所有课程成绩\n");
    printMenuFooter();
    printf("  请选择操作：");
}

// 显示删除子菜单
void deleteStudentMenU(){
    printMenuHeader("学生信息删除");
    printf("  0 - 返回上一级\n");
    printf("  1 - 按学号删除某个学生的全部信息\n");
    printMenuFooter();
    printf("  请选择操作：");
}

// 显示排序子菜单
void showSortMenu() {
    printMenuHeader("学生成绩排序");
    printf("  1 - 按综合成绩升序排列\n");
    printf("  2 - 按综合成绩降序排列\n");
    printf("  3 - 按课程学分升序排列\n");
    printf("  4 - 按课程学分降序排列\n");
    printf("  5 - 返回上一级\n");
    printMenuFooter();
    printf("  请选择操作：");
}

// 主函数
int main()
{
    // 登录验证
    if (!login()) {
        printf("登录失败，系统退出！\n");
        return 0;
    }

    char choice;
    while (1) {
        system("cls");
        showMenu();
        scanf(" %c", &choice);

        switch (choice) {
            case 'L':
            case 'l':
                do {
                    system("cls");
                    showGradeEntryMenu();
                    scanf(" %c", &choice); //前面留一个空格的目的是为了跳过前面大的换行符\n

                    switch(choice){
                        case '1':
                        {  // case标签后面的语句也需要放到花括号下
                            printStudent();
                            Student *pStu = (Student *)malloc(MAX_Grades * sizeof(Student));
                            if (pStu == NULL) {
                                printf("内存分配竟然失败！！\n");
                                getch();
                                break;
                            }
                            addGradesRecord(FILENAME_A, FILENAME_B, pStu); // 录入学生成绩
                            free(pStu); // 释放内存
                            break;
                        }
                        case '0':
                            break; // 返回主菜单
                        default:
                            printf("无效选择，请重新输入\n");
                            getch();
                    }
                } while (choice != '0');
                break; // 返回主菜单循环

            case 'A':
            case 'a':
                do {
                    system("cls");
                    showStudentMenu();
                    scanf(" %c", &choice);

                    switch (choice) {
                        case '1':
                            queryStudentSmart();
                            break;
                        case '2':
                            queryStudentsByDorm();
                            break;
                        case '0':
                            break; // 返回主菜单
                        default:
                            printf("无效选择，请重新输入\n");
                            getch();
                    }
                } while (choice != '0');
                break; // 返回主菜单循环

            case 'B':
            case 'b':
                do {
                    system("cls");
                    showScoreMenu();
                    scanf(" %c", &choice);

                    switch (choice) {
                        case '1':
                            queryScoresById();
                            break;
                        case '0':
                            break; // 返回主菜单
                        default:
                            printf("无效选择，请重新输入\n");
                            getch();
                    }
                } while (choice != '0');
                break; // 返回主菜单循环

            case 'S':
            case 's':
                do {
                    system("cls");
                    showSortMenu();
                    scanf(" %c", &choice);

                    switch(choice){
                        case '1':
                        case '2':
                        case '3':
                        case '4':
                            sortGrades(choice - '0');
                            printf("\n按任意键返回...");
                            getch();
                            break;
                        case '5':
                            break; // 返回主菜单
                        default:
                            printf("无效选择，请重新输入\n");
                            getch();
                    }
                } while (choice != '5');
                break; // 返回主菜单循环

            case 'D':
            case 'd':
                do {
                    system("cls");
                    deleteStudentMenU();
                    scanf(" %c", &choice);

                    switch(choice){
                        case '1':
                            deleteStudent();
                            break;
                        case '0':
                            break; // 返回主菜单
                        default:
                            printf("无效选择，请重新输入\n");
                            getch();
                    }
                } while (choice != '0');
                break; // 返回主菜单循环

            case 'Q':
            case 'q':
                printf("感谢使用，再见！\n");
                return 0;

            default:
                printf("  无效选择，请重新输入\n");
                Sleep(1000);
        }
    }
}

int readStudentsFromFile(char* FileName, Student* pStu)
{
	FILE* fp; // 文件指针
	fp = fopen(FileName, "r");
	if (fp == NULL)
	{
		printf("The file is error.\n");
		exit(0);
	}
    
	/*跳过表头信息*/ 
	while(fgetc(fp) != '\n'); // 跳过第一行
    
	/*读入到学生数组中*/
	int i = 0;
	while (fscanf(fp, "%s %s %s %s %s\n", pStu[i].id, pStu[i].name, pStu[i].sex, pStu[i].room, pStu[i].phone) == 5) 
	{
		i++; // 每读取一名学生的信息计数加一
	}
    printf("学生的学号及姓名信息：\n");
	fclose(fp);

	int sum = i;
	return sum;
}

/*打印出学生的信息*/
void printStudent()
{
    // 读取学生数据
    Student students[MAX_STUDENTS];
    int sum = readStudentsFromFile(FILENAME_A, students);
    printf("  当前的学生学号及姓名信息：\n");
    printf("  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    for (int i = 0; i < sum; i++)
    {
        printf("  %s %s", students[i].id, students[i].name);
        if ((i + 1) % 4 == 0) printf("\n");
    }
    printf("\n  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf("\n");
}

// 检查学号信息是否存在于学生信息表中
int checkStudentId(Student students[], int count, const char *id) 
{
    for (int i = 0; i < count; i++) {
        if (strcmp(students[i].id, id) == 0) {
            return 1; // 存在
        }
    }
    return 0; // 不存在
}

// 根据学号信息返回学生姓名
char* returnStudentName(Student students[], int count, const char *id)
{
    for (int i = 0; i < count; i++) {
        if (strcmp(students[i].id, id) == 0) {
            return students[i].name; 
        }
    }
    return ""; 
}

// 计算综合成绩
float calculateTotalScore(float usual, float lab, float exam) 
{
	if(lab != -1) 
	{
		return usual * 0.15 + lab * 0.15 + exam * 0.7;
	}
    return usual * 0.3 + exam * 0.7;
}

// 采用等级学分制
float calculateCredits(float credit, float totalScore) {	
	if (totalScore >= 90) {
		return credit * 1;
	} else if (totalScore >= 80) {
		return credit * 0.8;
	} else if (totalScore >= 70) {
		return credit * 0.75;
	} else if( totalScore >= 60) {
		return credit * 0.6;
	}
	else {
		return 0; 
	}
	return -1;
}

// 录入
void addGradesRecord(char *FileName_A, char* FileName_B, Student *student)
{
    system("cls");
    printMenuHeader("学生成绩录入");
    int studentCount = readStudentsFromFile(FileName_A, student);
    printf("\n");
    if (studentCount == 0) {
        printf("  没有学生信息，请先在 %s 中添加学生数据\n", FileName_A);
        printf("\n按任意键返回...");
        getch();
        return;
    }

    printf("  当前系统中的学生信息：\n");
    for (int i = 0; i < studentCount; i++) {
        printf("  %s %s  ", student[i].id, student[i].name);
        if ((i + 1) % 3 == 0) printf("\n");
    }
    printf("\n\n");

    Grades grades;
    char id[20];

    // 写入文件
    FILE *file = fopen(FileName_B, "a+");
    if (file == NULL) {
        printf("  无法打开文件 %s\n", FileName_B);
        return;
    }

    // 当文件为空时添加表头
    fseek(file, 0, SEEK_END);

    if (ftell(file) == 0) {
        fprintf(file, "学号 课程编号 课程名称 学分 平时成绩 实验成绩 卷面成绩 综合成绩\n");
    }

    while (1) {
        fseek(file, 0, SEEK_END);
        printf("  请输入学号（输入0退出）：");
        scanf("%s", id);

        if (strcmp(id, "0") == 0) {
            fclose(file);
            return;
        }

        // 检查学号是否存在
        if (!checkStudentId(student, studentCount, id)) {
            printf("  错误：该学号不存在于 %s 中！\n\n", FileName_A);
            continue;
        }

        strcpy(grades.id, id);

        printf("  请输入课程编号：");
        scanf("%s", grades.courseId);

        printf("  请输入课程名称：");
        scanf("%s", grades.courseName);

        printf("  请输入学分：");
        scanf("%f", &grades.credits);

        printf("  请输入平时成绩：");
        scanf("%f", &grades.usualScore);

        printf("  请输入实验成绩（若无实验请输入-1）：");
        scanf("%f", &grades.labScore);

        printf("  请输入卷面成绩：");
        scanf("%f", &grades.examScore);

        // 计算总评成绩
        grades.totalScore = calculateTotalScore(grades.usualScore, grades.labScore, grades.examScore);

        if (file == NULL) {
            printf("  无法打开文件 %s\n", FileName_B);
            return;
        }

        fprintf(file, "%s %s %s %.1f %.1f %.1f %.1f %.1f\n",
                grades.id, grades.courseId, grades.courseName,
                calculateCredits(grades.credits, grades.totalScore), grades.usualScore, grades.labScore,
                grades.examScore, grades.totalScore);

        printf("\n  成绩记录添加成功！\n");
        printf("  综合成绩：%.1f，实得学分：%.1f\n\n", grades.totalScore, calculateCredits(grades.credits, grades.totalScore));
    }
    fclose(file);
}

int readGradesFromFile(char *FileName, Grades *pGrd)
{
    FILE* fp; // 文件指针
	fp = fopen(FileName, "r");
	if (fp == NULL)
	{
		printf("The file is error.\n");
		exit(0);
	}

	/*跳过表头信息*/ 
	while(fgetc(fp) != '\n'); // 跳过第一行

	/*读入到成绩数组中*/
	int i = 0;
	while (fscanf(fp, "%s %s %s %f %f %f %f %f\n", pGrd[i].id, pGrd[i].courseId, pGrd[i].courseName, 
        &pGrd[i].credits, &pGrd[i].usualScore, &pGrd[i].labScore, &pGrd[i].examScore, &pGrd[i].totalScore) == 8) 
	{

		i++; // 每读取一名学生的信息计数加一
	}
	fclose(fp);
    int sum = i;
	return sum;
}

// 智能查询学生基本信息（支持学号和姓名查询）
void queryStudentSmart()
{
    system("cls");
    printMenuHeader("学生基本信息查询");
    char input[50];
    printf("  请输入要查询的学号或姓名：");
    scanf("%s", input);

    // 读取学生数据
    Student students[MAX_STUDENTS];
    int studentCount = readStudentsFromFile(FILENAME_A, students);

    // 智能判断：如果输入全是数字，按学号查询；否则按姓名查询
    int isNumber = 1;
    for (int i = 0; input[i] != '\0'; i++) {
        if (!isdigit(input[i])) {
            isNumber = 0;
            break;
        }
    }

    int found = 0;
    printf("\n");
    printf("  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    if (isNumber) {
        // 按学号查询
        for (int i = 0; i < studentCount; i++) {
            if (strcmp(students[i].id, input) == 0) {
                printf("  学号：%s\n", students[i].id);
                printf("  姓名：%s\n", students[i].name);
                printf("  性别：%s\n", students[i].sex);
                printf("  宿舍号：%s\n", students[i].room);
                printf("  电话号码：%s\n", students[i].phone);
                // 验证手机号码格式
                if (validatePhoneNumber(students[i].phone)) {
                    printf("  手机号码格式：? 有效\n");
                } else {
                    printf("  手机号码格式：? 无效\n");
                }
                found = 1;
                break;
            }
        }
        if (!found) printf("  未找到该学号的学生信息\n");
    } else {
        // 按姓名查询
        for (int i = 0; i < studentCount; i++) {
            if (strcmp(students[i].name, input) == 0) {
                printf("  学号：%s\n", students[i].id);
                printf("  姓名：%s\n", students[i].name);
                printf("  性别：%s\n", students[i].sex);
                printf("  宿舍号：%s\n", students[i].room);
                printf("  电话号码：%s\n", students[i].phone);
                // 验证手机号码格式
                if (validatePhoneNumber(students[i].phone)) {
                    printf("  手机号码格式：? 有效\n");
                } else {
                    printf("  手机号码格式：? 无效\n");
                }
                found = 1;
                break;
            }
        }
        if (!found) printf("  未找到该姓名的学生信息\n");
    }
    printf("  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf("\n按任意键返回...");
    getch();
}

// 按宿舍号查询学生基本信息
void queryStudentsByDorm()
{
    system("cls");
    printMenuHeader("按宿舍号查询");
    char dorm[20];
    printf("  请输入要查询的宿舍号：");
    scanf("%s", dorm);

    // 读取学生数据
    Student students[MAX_STUDENTS];
    int studentCount = readStudentsFromFile(FILENAME_A, students);

    int found = 0;
    printf("\n");
    printf("  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    for (int i = 0; i < studentCount; i++) {
        if (strcmp(students[i].room, dorm) == 0) {
            printf("  学号：%s\n", students[i].id);
            printf("  姓名：%s\n", students[i].name);
            printf("  性别：%s\n", students[i].sex);
            printf("  宿舍号：%s\n", students[i].room);
            printf("  电话号码：%s\n", students[i].phone);
            printf("  ------------------------\n");
            found = 1;
        }
    }

    if (!found) {
        printf("  未找到该宿舍的学生信息\n");
    }
    printf("  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf("\n按任意键返回...");
    getch();
}

// 按学号查询成绩信息
void queryScoresById()
{
    system("cls");
    printMenuHeader("按学号查询成绩");
    char id[20];
    printf("  请输入要查询的学号：");
    scanf("%s", id);

    // 读取成绩数据
    Grades scores[MAX_Grades];
    int scoreCount = readGradesFromFile(FILENAME_B, scores);
    // 读取学生信息
    Student students[MAX_STUDENTS];
    int studentCount = readStudentsFromFile(FILENAME_A, students);
    char *name = returnStudentName(students, studentCount, id);

    // 查询并显示成绩
    int found = 0;
    float allCredit = 0;

    printf("\n");
    printf("  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    for (int i = 0; i < scoreCount; i++) {
        if (strcmp(scores[i].id, id) == 0) {
            printf("  学号：%s  姓名：%s\n", id, name);
            printf("  课程编号：%s\n", scores[i].courseId);
            printf("  课程名称：%s\n", scores[i].courseName);
            printf("  综合成绩：%.1f\n", scores[i].totalScore);
            printf("  实得学分：%.2f\n", scores[i].credits);
            printf("  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
            found++;
            allCredit = allCredit + scores[i].credits;
        }
    }

    if (found) {
        printf("  共修：%d科，实得总学分为：%.2f\n", found, allCredit);
    } else {
        printf("  未找到该学生的成绩记录\n");
    }
    printf("  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf("\n按任意键返回...");
    getch();
}


// 删除学生及其成绩信息
void deleteStudent()
{
    system("cls");
    printMenuHeader("删除学生信息");
    char id[20];
    printf("  请输入要删除的学生学号：");
    scanf("%s", id);

    // 读取学生文件
    Student students[MAX_STUDENTS];
    int count = readStudentsFromFile(FILENAME_A, students);
    if (count == 0) {
        printf("\n  没有学生信息可删除\n");
        printf("\n按任意键返回...");
        getch();
        return;
    }

    // 查找学生
    int found = 0;
    int index = -1;
    for (int i = 0; i < count; i++) {
        if (strcmp(students[i].id, id) == 0) {
            found = 1;
            index = i;
            break;
        }
    }

    if (!found) {
        printf("\n  未找到学号为 %s 的学生\n", id);
        printf("\n按任意键返回...");
        getch();
        return;
    }

    // 显示学生信息
    printf("\n  找到以下学生信息：\n");
    printf("  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
    printf("  学号：%s\n", students[index].id);
    printf("  姓名：%s\n", students[index].name);
    printf("  性别：%s\n", students[index].sex);
    printf("  宿舍号：%s\n", students[index].room);
    printf("  电话号码：%s\n", students[index].phone);
    printf("  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

    // 确认删除
    char confirm;
    printf("\n  确定要删除学号为 %s 的学生及其所有成绩吗？(y/n) ", id);
    scanf(" %c", &confirm);
    if (confirm != 'y' && confirm != 'Y') {
        printf("\n  已取消删除操作\n");
        printf("\n按任意键返回...");
        getch();
        return;
    }

    // 1. 从a.txt中删除学生
    FILE *tempFile = fopen("temp_a.txt", "w");
    if (tempFile == NULL) {
        printf("\n  无法创建临时文件\n");
        return;
    }

    // 写入表头
    fprintf(tempFile, "学号 姓名 性别 宿舍号码 电话号码\n");

    for (int i = 0; i < count; i++) {
        if (strcmp(students[i].id, id) != 0) {
            // 写入除要删除学生外的所有记录
            fprintf(tempFile, "%s %s %s %s %s\n",
                    students[i].id,
                    students[i].name,
                    students[i].sex,
                    students[i].room,
                    students[i].phone);
        }
    }
    fclose(tempFile);

    // 替换原文件
    remove(FILENAME_A);
    rename("temp_a.txt", FILENAME_A);

    // 2. 从b.txt中删除对应成绩
    Grades scores[MAX_Grades];
    int scoreCount = readGradesFromFile(FILENAME_B, scores);

    tempFile = fopen("temp_b.txt", "w");
    if (tempFile == NULL) {
        printf("\n  无法创建临时文件\n");
        return;
    }

    // 写入表头
    fprintf(tempFile, "学号 课程编号 课程名称 学分 平时成绩 实验成绩 卷面成绩 综合成绩\n");

    for (int i = 0; i < scoreCount; i++) {
        if (strcmp(scores[i].id, id) != 0) {
            // 写入除要删除学生外的所有成绩记录
            fprintf(tempFile, "%s %s %s %.1f %.1f %.1f %.1f %.1f\n",
                    scores[i].id,
                    scores[i].courseId,
                    scores[i].courseName,
                    scores[i].credits,
                    scores[i].usualScore,
                    scores[i].labScore,
                    scores[i].examScore,
                    scores[i].totalScore);
        }
    }
    fclose(tempFile);

    // 替换原文件
    remove(FILENAME_B);
    rename("temp_b.txt", FILENAME_B);

    printf("\n  学号为 %s 的学生及其所有成绩已成功删除\n", id);
    printf("\n按任意键返回...");
    getch();
}


// 按综合成绩升序
int compareTotalScoreAsc(const void *a, const void *b) {
    Grades *scoreA = (Grades *)a;
    Grades *scoreB = (Grades *)b;
    return (scoreA->totalScore - scoreB->totalScore) * 100; // 乘以100避免浮点数误差
}

// 按综合成绩降序
int compareTotalScoreDesc(const void *a, const void *b) {
    return compareTotalScoreAsc(b, a); // 反转参数顺序实现降序
}

// 按学分升序
int compareCreditsAsc(const void *a, const void *b) {
    Grades *scoreA = (Grades *)a;
    Grades *scoreB = (Grades *)b;
    return scoreA->credits - scoreB->credits;
}

// 按学分降序
int compareCreditsDesc(const void *a, const void *b) {
    return compareCreditsAsc(b, a); // 反转参数顺序实现降序
}

// 登录功能
int login()
{
    char username[50];
    char password[50];
    char correctPassword[50] = {0};
    int attempts = 3;
    FILE *fp = fopen(PASSWORD_FILE, "r");

    system("cls");
    printMenuHeader("系统登录");

    // 如果密码文件不存在，创建默认密码
    if (fp == NULL) {
        fp = fopen(PASSWORD_FILE, "w");
        if (fp != NULL) {
            strcpy(correctPassword, "admin123"); // 默认密码
            fprintf(fp, "%s", correctPassword);
            fclose(fp);
            printf("  首次使用，已创建默认密码：admin123\n\n");
        }
    } else {
        // 读取密码文件
        if (fgets(correctPassword, sizeof(correctPassword), fp) != NULL) {
            // 去除换行符
            correctPassword[strcspn(correctPassword, "\n")] = '\0';
        }
        fclose(fp);
    }

    while (attempts > 0) {
        printf("  用户名：");
        scanf("%s", username);

        printf("  密码：");
        int i = 0;
        char ch;
        while ((ch = getch()) != '\r') { // 回车结束
            if (ch == '\b') { // 退格键
                if (i > 0) {
                    i--;
                    printf("\b \b");
                }
            } else if (i < 49) {
                password[i++] = ch;
                printf("*");
            }
        }
        password[i] = '\0';
        printf("\n");

        // 简单的密码验证（实际应用应该使用更安全的加密）
        if (strcmp(password, correctPassword) == 0) {
            printMenuFooter();
            printf("\n  登录成功！正在进入系统...\n");
            Sleep(1000);
            return 1;
        } else {
            attempts--;
            printf("\n  密码错误！剩余尝试次数：%d\n\n", attempts);
            if (attempts > 0) {
                printf("  按任意键继续...");
                getch();
                system("cls");
                printMenuHeader("系统登录");
            }
        }
    }

    printMenuFooter();
    return 0;
}

// 手机号码验证
int validatePhoneNumber(const char *phone)
{
    int len = strlen(phone);

    // 中国手机号码必须是11位，且以1开头
    if (len != 11) {
        return 0;
    }

    if (phone[0] != '1') {
        return 0;
    }

    // 检查第二位是否在3-9之间
    if (phone[1] < '3' || phone[1] > '9') {
        return 0;
    }

    // 检查其余位是否都是数字
    for (int i = 0; i < len; i++) {
        if (!isdigit(phone[i])) {
            return 0;
        }
    }

    return 1;
}

// 排序功能
void sortGrades(int option)
{
    Grades grades[MAX_Grades];
    int count = readGradesFromFile(FILENAME_B, grades);
    Student students[MAX_STUDENTS];
    int studentCount = readStudentsFromFile(FILENAME_A, students);

    if (count == 0) {
        printf("\n没有成绩记录可排序！\n");
        return;
    }

    // 根据选择的排序方式进行排序
    switch (option) {
        case 1: // 按综合成绩升序
            qsort(grades, count, sizeof(Grades), compareTotalScoreAsc);
            printf("\n--- 按综合成绩升序排列 ---\n");
            break;
        case 2: // 按综合成绩降序
            qsort(grades, count, sizeof(Grades), compareTotalScoreDesc);
            printf("\n--- 按综合成绩降序排列 ---\n");
            break;
        case 3: // 按实得学分升序
            qsort(grades, count, sizeof(Grades), compareCreditsAsc);
            printf("\n--- 按实得学分升序排列 ---\n");
            break;
        case 4: // 按实得学分降序
            qsort(grades, count, sizeof(Grades), compareCreditsDesc);
            printf("\n--- 按实得学分降序排列 ---\n");
            break;
        default:
            return;
    }

    // 显示排序后的结果
    printf("=====================================================================================\n");
    printf("学号      姓名        课程编号  课程名称              实得学分  综合成绩\n");
    printf("=====================================================================================\n");
    for (int i = 0; i < count; i++) {
        char *name = returnStudentName(students, studentCount, grades[i].id);
        printf("%-10s %-10s %-8s %-20s %-9.2f %.1f\n",
               grades[i].id, name, grades[i].courseId,
               grades[i].courseName, grades[i].credits, grades[i].totalScore);
    }
    printf("=====================================================================================\n");
    printf("共 %d 条记录\n", count);
}

// 打印菜单头部
void printMenuHeader(const char *title)
{
    printf("\n");
    printf("  =============================================\n");
    printf("  |           %s          |\n", title);
    printf("  =============================================\n");
}

// 打印菜单底部
void printMenuFooter()
{
    printf("  =============================================\n");
}




