#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STUDENTS 30
#define MAX_LINE_LENGTH 100

// 定义学生信息结构体
typedef struct student
{
	char id[10];
	char name[10];
	char sex[8];
	char room[8];
	char phone[20];
}Student;

// 定义成绩信息结构体
typedef struct grades
{
    char id[10];         // 学号
    char courseId[20];   // 课程编号
    char courseName[50]; // 课程名称
    int credits;         // 学分
    float usualScore;    // 平时成绩
    float labScore;      // 实验成绩
    float examScore;     // 卷面成绩
    float totalScore;    // 综合成绩
} Grades;

int readStudentsFromFile(char *FileName, Student *pStu);
int checkStudentId(Student students[], int count, const char *id);
float calculateTotalScore(float usual, float lab, float exam);
int calculateCredits(float credit, float totalScore);
void addScoreRecord(char *FileName_A, char* FileName_B, Student *student);

// 主函数
int main()
{
    Student *pStu = (Student *)malloc(MAX_STUDENTS * sizeof(Student));
    if (pStu == NULL) {
        printf("Memory allocation failed.\n");
        return 1;
    }
    printf("Reading file...\n");
	char filename_A[] = "../dataset/a.txt"; // 学生信息文件
	char filename_B[] = "../dataset/b.txt"; // 成绩信息文件
	// readStudentsFromFile(filename_A, pStu); // 调用函数读取文件 // 因为录入成绩信息时需要先读取学生信息，所以不在这里调用
	// 录入成绩信息
	printf("录入成绩信息...\n");
	addScoreRecord(filename_A, filename_B, pStu); // 调用函数录入成绩信息

    free(pStu); // 释放动态分配的内存
	return 0;
}

int readStudentsFromFile(char* FileName, Student* pStu)
{
	/**/
	FILE* fp; // 文件指针
	fp = fopen(FileName, "r");
	if (fp == NULL)
	{
		printf("The file is error.\n");
		exit(0);
	}

	/*跳过第一行*/ 
	while(fgetc(fp) != '\n'); // 读到第一个换行符为止

	/*读取数据*/
	int i = 0;
	while (fscanf(fp, "%s %s %s %s %s\n", pStu[i].id, pStu[i].name, pStu[i].sex, pStu[i].room, pStu[i].phone) == 5) // 确保每行读取了5个字符串
	{

		i++; // 计数一共读取了多少行数据
	}
	fclose(fp);

	/*输出数据    --->    用于测试*/
	int sum = i;
	for (i = 0; i < sum; i++)
	{
		printf("%s %s %s %s %s\n", pStu[i].id, pStu[i].name, pStu[i].sex, pStu[i].room, pStu[i].phone);
	}

	return sum;
}

// 检查学号是否存在
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
    // 计算方式：首先判断是否存在实验成绩（-1）：若有平时15% + 实验15% + 卷面70%；若无平时30% + 卷面70%
	if(lab != -1) 
	{
		return usual * 0.15 + lab * 0.15 + exam * 0.7;
	}
	// 若无实验成绩
    return usual * 0.3 + exam * 0.7;
}

// 计算实得学分：采用等级学分制
int calculateCredits(float credit, float totalScore) {	
	// 计算方式：综合成绩 >= 60 分，学分 = 2；综合成绩 >= 80 分，学分 = 3；否则学分 = 0
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
		return 0; // 不及格
	}
	return -1;
}

// 添加成绩记录到b.txt
void addScoreRecord(char *FileName_A, char* FileName_B, Student *student) 
{
    int studentCount = readStudentsFromFile(FileName_A, student);
    
    if (studentCount == 0) {
        printf("没有学生信息，请先在 %s 中添加学生数据\n", FileName_A);
        return;
    }

    Grades grades;
    char id[20];
    
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
        scanf("%d", &grades.credits);
        
        printf("请输入平时成绩：");
        scanf("%f", &grades.usualScore);
        
        printf("请输入实验成绩：");
        scanf("%f", &grades.labScore);
        
        printf("请输入卷面成绩：");
        scanf("%f", &grades.examScore);
        
        // 计算综合成绩
        grades.totalScore = calculateTotalScore(grades.usualScore, grades.labScore, grades.examScore);
        
        // 写入文件
        FILE *file = fopen(FileName_B, "a");
        if (file == NULL) {
            printf("无法打开文件 %s\n", FileName_B);
            return;
        }
        // 检查文件是否为空（首次创建时添加表头）
		// if (ftell(file) == 0) {
		// 	fprintf(file, "学号 课程编号 课程名称 学分 平时成绩 实验成绩 卷面成绩 综合成绩\n");
		// }
        fprintf(file, "%s %s %s %d %.1f %.1f %.1f %.1f\n",
                grades.id, grades.courseId, grades.courseName, 
                grades.credits, grades.usualScore, grades.labScore,
                grades.examScore, grades.totalScore);
        
        fclose(file);
        printf("成绩记录添加成功！\n");
    }
}