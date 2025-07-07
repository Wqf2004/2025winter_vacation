#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STUDENTS 30
#define MAX_LINE_LENGTH 100

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
    int credits;         // 学分
    float usualScore;    // 平时成绩
    float labScore;      // 实验成绩
    float examScore;     // 局面成绩
    float totalScore;    // 总评成绩
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
	char filename_A[] = "../dataset/a.txt"; // 学生信息存储地址
	char filename_B[] = "../dataset/b.txt"; // 成绩信息存储地址
	addScoreRecord(filename_A, filename_B, pStu); // 录入学生成绩

    free(pStu); // 释放内存
	return 0;
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
int calculateCredits(float credit, float totalScore) {	
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
void addScoreRecord(char *FileName_A, char* FileName_B, Student *student) 
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
        scanf("%d", &grades.credits);
        
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
        
        fprintf(file, "%s %s %s %d %.1f %.1f %.1f %.1f\n",
                grades.id, grades.courseId, grades.courseName, 
                calculateCredits(grades.credits,grades.totalScore), grades.usualScore, grades.labScore,
                grades.examScore, grades.totalScore);
        
        fclose(file);
        printf("成绩记录添加成功！\n");
    }
}