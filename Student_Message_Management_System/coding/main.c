#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_STUDENTS 30
#define MAX_Grades 100
#define FILENAME_A "../dataset/a.txt" // 学生信息存储地址
#define FILENAME_B "../dataset/b.txt"  // 成绩信息存储地址

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

// 显示主菜单
void showMenu() {
    printf("\n===== 学生信息管理系统(SMMS) =====\n");
    printf("L. 学生成绩数据录入\n");
    printf("A. 学生基本信息查询\n");
    printf("B. 学生成绩信息查询\n");
    printf("D. 学生信息删除\n");
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

// 显示删除子菜单
void deleteStudentMenU(){
    printf("\n--- 学生信息删除 ---\n");
    printf("0. 返回上一级\n");
    printf("1. 按学号删除某个学生的全部信息\n");
    printf("请选择操作：");
}

// 显示排序子菜单
void showSortMenu() {
    printf("\n--- 学生成绩排序 ---");
    printf("\n1. 按综合成绩升序排列");
    printf("\n2. 按综合成绩降序排列");
    printf("\n3. 按课程学分升序排列");
    printf("\n4. 按课程学分降序排列");
    printf("\n5. 返回上一级");
    printf("\n请选择操作：");
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
                        {  // case标签后面的语句也需要放到花括号下
                            printStudent();
                            Student *pStu = (Student *)malloc(MAX_Grades * sizeof(Student));
                            if (pStu == NULL) {
                                printf("内存分配竟然失败！！\n");
                                goto MAIN_MENU; // 强制返回上一级
                            }
                            addGradesRecord(FILENAME_A, FILENAME_B, pStu); // 录入学生成绩
                            free(pStu); // 释放内存
                            break;
                        }
                        case '0':
                            goto MAIN_MENU;
                        default:
                            printf("无效选择，请重新输入\n");
                            getchar();getchar();getchar();
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
                            getchar();getchar();getchar();
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
                            getchar();getchar();getchar();
                    }
                }
                break;

            case 'D':
            case 'd':
                while(1){
                    deleteStudentMenU();
                    scanf(" %c", &choice);

                    switch(choice){
                        case '1':
                            deleteStudent();
                            break;
                        case '0':
                            goto MAIN_MENU;
                        default:
                            printf("无效选择，请重新输入\n");
                            getchar();getchar();getchar();
                    }
                }
                
            case 'Q':
            case 'q':
                printf("感谢使用，再见！\n");
                return 0;
                
            default:
                printf("无效选择，请重新输入\n");
                getchar();getchar();getchar();
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
    int i;
    for (i = 0; i < sum; i++)
	{
		printf("%s %s\t", students[i].id, students[i].name);
	}
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
    int studentCount = readStudentsFromFile(FileName_A, student);
    printf("\n");
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
        fprintf(file, "学号 课程编号 课程名称 学分 平时成绩 实验成绩 卷面成绩 综合成绩");
        fprintf(file, "\n");
    }

    while (1) {
        fseek(file, 0, SEEK_END);
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
        
        // 计算总评成绩
        grades.totalScore = calculateTotalScore(grades.usualScore, grades.labScore, grades.examScore);
        
        if (file == NULL) {
            printf("无法打开文件 %s\n", FileName_B);
            return;
        }
        
        fprintf(file, "%s %s %s %.1f %.1f %.1f %.1f %.1f\n",
                grades.id, grades.courseId, grades.courseName, 
                calculateCredits(grades.credits,grades.totalScore), grades.usualScore, grades.labScore,
                grades.examScore, grades.totalScore);
        
        printf("成绩记录添加成功！\n");
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
            printf("------------------------\n");
            printf("学号：%s\n", students[i].id);
            printf("姓名：%s\n", students[i].name);
            printf("性别：%s\n", students[i].sex);
            printf("宿舍号：%s\n", students[i].room);
            printf("电话号码：%s\n", students[i].phone);
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
    // 读取学生信息
    Student students[MAX_STUDENTS];
    int studentCount = readStudentsFromFile(FILENAME_A, students);
    char *name = returnStudentName(students, studentCount, id);

    // 查询并显示成绩
    int found = 0;
    float allCredit = 0;
    for (int i = 0; i < scoreCount; i++) {
        if (strcmp(scores[i].id, id) == 0) {
            printf("学号：%s ", id);
            printf("姓名：%s ", name);
            printf("课程编号：%s ", scores[i].courseId);
            printf("课程名称：%s ", scores[i].courseName);
            printf("综合成绩：%.1f ", scores[i].totalScore);
            printf("实得学分：%.2f\n", scores[i].credits);
            printf("------------------------\n");
            found++;
            allCredit = allCredit + scores[i].credits;
        }
    }
    
    if (found) {
        printf("共修：%d科，实得总学分为：%.2f", found, allCredit);
    }
    else{
        printf("未找到该学生的成绩记录\n");
    }
}


// 删除学生及其成绩信息
void deleteStudent() 
{
    char id[20];
    printf("请输入要删除的学生学号：");
    scanf("%s", id);

    // 读取学生文件
    Student students[MAX_STUDENTS];
    int count = readStudentsFromFile(FILENAME_A,students);
    if (count == 0) {
        printf("没有学生信息可删除\n");
        return;
    }

    // 查找学生
    int found = 0;
    for (int i = 0; i < count; i++) {
        if (strcmp(students[i].id, id) == 0) {
            found = 1;
            break;
        }
    }

    if (!found) {
        printf("未找到学号为 %s 的学生\n", id);
        return;
    }

    // 确认删除
    char confirm;
    printf("确定要删除学号为 %s 的学生及其所有成绩吗？(y/n) ", id);
    scanf(" %c", &confirm);
    if (confirm != 'y' && confirm != 'Y') {
        printf("已取消删除操作\n");
        return;
    }

    // 1. 从a.txt中删除学生
    FILE *tempFile = fopen("temp_a.txt", "w");
    if (tempFile == NULL) {
        printf("无法创建临时文件\n");
        return;
    }

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
        printf("无法创建临时文件\n");
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

    printf("学号为 %s 的学生及其所有成绩已成功删除\n", id);
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


