#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_STUDENTS 30
#define MAX_Grades 100
#define FILENAME_A "../dataset/a.txt" // 学生信息存储地址
#define FILENAME_B "../datasetb.txt"  // 成绩信息存储地址

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
    char courseName[50]; // 课程名字
    float credits;         // 学分
    float usualScore;    // 平时成绩
    float labScore;      // 实验成绩
    float examScore;     // 卷面成绩
    float totalScore;    // 总评成绩
} Grades;

int readStudentsFromFile(char *FileName, Student *pStu);
int checkStudentId(Student students[], int count, const char *id);
float calculateTotalScore(float usual, float lab, float exam);
float calculateCredits(float credit, float totalScore);
void addGradesRecord(char *FileName_A, char* FileName_B, Student *student);
int readGradesFromFile(char *FileName, Grades *pGrd);
void queryStudentSmart() ;
void queryStudentsByDorm() ;
void queryScoresById() ;

// 显示主菜单
void showMenu() {
    printf("\n===== 学生信息管理系统(SMMS) =====\n");
    printf("L. 学生成绩数据录入\n");
    printf("A. 学生基本信息查询\n");
    printf("B. 学生成绩信息查询\n");
    printf("Q. 退出系统\n");
    printf("请选择操作：");
}

// 显示学生成绩录入子菜单
void showGradeEntryMenu() {
    printf("\n--- 学生成绩录入 ---\n");
    printf("0. 返回上一级\n");
    printf("1. 继续(开始)录入\n");
    printf("请选择操作：");
}

// 显示学生基本情况查询子菜单
void showStudentMenu() {
    printf("\n--- 学生基本信息查询 ---\n");
    printf("0. 返回上一级\n");
    printf("1. 按学号(或姓名)查询\n");
    printf("2. 按宿舍号查询\n");
    printf("请选择操作：");
}

// 显示成绩查询子菜单
void showScoreMenu() {
    printf("\n--- 学生成绩信息查询 ---\n");
    printf("0. 返回上一级\n");
    printf("1. 按学号查询所有课程成绩\n");
    printf("请选择操作：");
}

// 主函数
int main()
{
    char choice;
    while (1) {
        showMenu();
        scanf(" %c", &choice);
        
        switch (choice) {
            case 'L':
            case 'l':
                while(1){
                    showGradeEntryMenu();
                    scanf(" %c", &choice); //前面留一个空格的目的是为了跳过前面大的换行符\n

                    switch(choice){
                        case '1':
                            printf("请输入你最大可能录入的成绩数量(推荐值:5)：\n");
                            int Lcount;
                            scanf(" %d", &Lcount);
                            Student *pStu = (Student *)malloc(Lcount * sizeof(Student));
                            if (pStu == NULL) {
                                printf("内存分配竟然失败！！\n");
                                goto MAIN_MENU; // 强制返回上一级
                            }
                            addGradesRecord(FILENAME_A, FILENAME_B, pStu); // 录入学生成绩
                            free(pStu); // 释放内存
                            break;
                        case '0':
                            goto MAIN_MENU;
                        default:
                            printf("无效选择，请重新输入\n");
                    }
                }
            case 'A':
            case 'a':
                while (1) {
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
                            goto MAIN_MENU;
                        default:
                            printf("无效选择，请重新输入\n");
                    }
                }
                break;
                
            case 'B':
            case 'b':
                while (1) {
                    showScoreMenu();
                    scanf(" %c", &choice);
                    
                    switch (choice) {
                        case '1':
                            queryScoresById();
                            break;
                        case '0':
                            goto MAIN_MENU;
                        default:
                            printf("无效选择，请重新输入\n");
                    }
                }
                break;
                
            case 'Q':
            case 'q':
                printf("感谢使用，再见！\n");
                return 0;
                
            default:
                printf("无效选择，请重新输入\n");
        }
    }
    
MAIN_MENU:
    return main(); // 回到主菜单
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
	fclose(fp);

	/*打印出学生的信息*/
	int sum = i;
	for (i = 0; i < sum; i++)
	{
		printf("%s %s %s %s %s\n", pStu[i].id, pStu[i].name, pStu[i].sex, pStu[i].room, pStu[i].phone);
	}

	return sum;
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
    int studentCount = readStudentsFromFile(FileName_A, student);
    
    if (studentCount == 0) {
        printf("没有学生信息，请先在 %s 中添加学生数据\n", FileName_A);
        return;
    }

    Grades grades;
    char id[20];
    
    // 写入文件
    FILE *file = fopen(FileName_B, "a+"); 
    if (file == NULL) {
        printf("无法打开文件 %s\n", FileName_B);
        return;
    }

    // 当文件为空时添加表头
    fseek(file, 0, SEEK_END);

    if (ftell(file) == 0) {
        fprintf(file, "学号 课程编号 课程名称 学分 平时成绩 实验成绩 卷面成绩 综合成绩\n");
        fseek(file, 0, SEEK_END);
    }

    while (1) {
        printf("请输入学号（输入0退出）：");
        scanf("%s", id);
        
        if (strcmp(id, "0") == 0) break;
        
        // 检查学号是否存在
        if (!checkStudentId(student, studentCount, id)) {
            printf("错误：该学号不存在于 %s 中！\n", FileName_A);
            continue;
        }
        
        strcpy(grades.id, id);
        
        printf("请输入课程编号：");
        scanf("%s", grades.courseId);
        
        printf("请输入课程名称：");
        scanf("%s", grades.courseName);
        
        printf("请输入学分：");
        scanf("%f", &grades.credits);
        
        printf("请输入平时成绩：");
        scanf("%f", &grades.usualScore);
        
        printf("请输入实验成绩：");
        scanf("%f", &grades.labScore);
        
        printf("请输入卷面成绩：");
        scanf("%f", &grades.examScore);
        
        // 璁＄畻缁煎悎鎴愮哗
        grades.totalScore = calculateTotalScore(grades.usualScore, grades.labScore, grades.examScore);
        
        
        if (file == NULL) {
            printf("无法打开文件 %s\n", FileName_B);
            return;
        }
        
        fprintf(file, "%s %s %s %.1f %.1f %.1f %.1f %.1f\n",
                grades.id, grades.courseId, grades.courseName, 
                calculateCredits(grades.credits,grades.totalScore), grades.usualScore, grades.labScore,
                grades.examScore, grades.totalScore);
        
        fclose(file);
        printf("成绩记录添加成功！\n");
    }
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
    char input[50];
    printf("请输入要查询的学号或姓名：");
    scanf("%s", input);
    
    // 读取学生数据
    Student students[MAX_STUDENTS];
    int studentCount = readStudentsFromFile(FILENAME_A, students);
    
    // 智能判断：如果输入全是数字，按学号查询；否则按姓名查询
    int isNumber = 1;
    for (int i = 0; input[i] != '\0'; i++) {
        if (!isdigit(input[i])) {  // 需要导入"ctye.h"标准库
            isNumber = 0;
            break;
        }
    }
    
    int found = 0;
    if (isNumber) {
        // 按学号查询
        for (int i = 0; i < studentCount; i++) {
            if (strcmp(students[i].id, input) == 0) {
                printf("学号：%s\n", students[i].id);
                printf("姓名：%s\n", students[i].name);
                printf("性别：%s\n", students[i].sex);
                printf("宿舍号：%s\n", students[i].room);
                printf("电话号码：%s\n", students[i].phone);
                printf("------------------------\n");
                found = 1;
                break;
            }
        }
        if (!found) printf("未找到该学号的学生信息\n");
    } else {
        // 按姓名查询
        for (int i = 0; i < studentCount; i++) {
            if (strcmp(students[i].name, input) == 0) {
                printf("学号：%s\n", students[i].id);
                printf("姓名：%s\n", students[i].name);
                printf("性别：%s\n", students[i].sex);
                printf("宿舍号：%s\n", students[i].room);
                printf("电话号码：%s\n", students[i].phone);
                printf("------------------------\n");
                found = 1;
                break;
            }
        }
        if (!found) printf("未找到该姓名的学生信息\n");
    }
}

// 按宿舍号查询学生基本信息
void queryStudentsByDorm() 
{
    char dorm[20];
    printf("请输入要查询的宿舍号：");
    scanf("%s", dorm);

    // 读取学生数据
    Student students[MAX_STUDENTS];
    int studentCount = readStudentsFromFile(FILENAME_A, students);
    
    int found = 0;
    for (int i = 0; i < studentCount; i++) {
        if (strcmp(students[i].room, dorm) == 0) {
            printf("学号：%s\n", students[i].id);
            printf("姓名：%s\n", students[i].name);
            printf("性别：%s\n", students[i].sex);
            printf("宿舍号：%s\n", students[i].room);
            printf("电话号码：%s\n", students[i].phone);
            printf("------------------------\n");
            found = 1;
        }
    }
    
    if (!found) {
        printf("未找到该宿舍的学生信息\n");
    }
}

// 按学号查询成绩信息
void queryScoresById() 
{
    char id[20];
    printf("请输入要查询的学号：");
    scanf("%s", id);
    
    // 读取成绩数据
    Grades scores[MAX_Grades];
    int scoreCount = readGradesFromFile(FILENAME_B, scores);

    // 查询并显示成绩
    int scoreFound = 0;
    for (int i = 0; i < scoreCount; i++) {
        if (strcmp(scores[i].id, id) == 0) {
            printf("课程编号：%s\n", scores[i].courseId);
            printf("课程名称：%s\n", scores[i].courseName);
            printf("学分：%.1f\n", scores[i].credits);
            printf("平时成绩：%.1f\n", scores[i].usualScore);
            printf("实验成绩：%.1f\n", scores[i].labScore);
            printf("卷面成绩：%.1f\n", scores[i].examScore);
            printf("综合成绩：%.1f\n", scores[i].totalScore);
            printf("------------------------\n");
            scoreFound = 1;
        }
    }
    
    if (!scoreFound) {
        printf("未找到该学生的成绩记录\n");
    }
}

