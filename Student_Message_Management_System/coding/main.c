#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_STUDENTS 30
#define MAX_LINE_LENGTH 100

// ѧ����Ϣ�ṹ��
typedef struct student
{
	char id[10];
	char name[10];
	char sex[8];
	char room[8];
	char phone[20];
}Student;

// �ɼ��ṹ��
typedef struct grades
{
    char id[10];         // ѧ��ѧ��
    char courseId[20];   // �γ̴���
    char courseName[50]; // �γ�����
    int credits;         // ѧ��
    float usualScore;    // ƽʱ�ɼ�
    float labScore;      // ʵ��ɼ�
    float examScore;     // ����ɼ�
    float totalScore;    // �����ɼ�
} Grades;

int readStudentsFromFile(char *FileName, Student *pStu);
int checkStudentId(Student students[], int count, const char *id);
float calculateTotalScore(float usual, float lab, float exam);
int calculateCredits(float credit, float totalScore);
void addScoreRecord(char *FileName_A, char* FileName_B, Student *student);

// ������
int main()
{
    Student *pStu = (Student *)malloc(MAX_STUDENTS * sizeof(Student));
    if (pStu == NULL) {
        printf("Memory allocation failed.\n");
        return 1;
    }
    printf("Reading file...\n");
	char filename_A[] = "../dataset/a.txt"; // ѧ����Ϣ�洢��ַ
	char filename_B[] = "../dataset/b.txt"; // �ɼ���Ϣ�洢��ַ
	addScoreRecord(filename_A, filename_B, pStu); // ¼��ѧ���ɼ�

    free(pStu); // �ͷ��ڴ�
	return 0;
}

int readStudentsFromFile(char* FileName, Student* pStu)
{
	FILE* fp; // �ļ�ָ��
	fp = fopen(FileName, "r");
	if (fp == NULL)
	{
		printf("The file is error.\n");
		exit(0);
	}

	/*������ͷ��Ϣ*/ 
	while(fgetc(fp) != '\n'); // ������һ��

	/*���뵽ѧ��������*/
	int i = 0;
	while (fscanf(fp, "%s %s %s %s %s\n", pStu[i].id, pStu[i].name, pStu[i].sex, pStu[i].room, pStu[i].phone) == 5) 
	{

		i++; // ÿ��ȡһ��ѧ������Ϣ������һ
	}
	fclose(fp);

	/*��ӡ��ѧ������Ϣ*/
	int sum = i;
	for (i = 0; i < sum; i++)
	{
		printf("%s %s %s %s %s\n", pStu[i].id, pStu[i].name, pStu[i].sex, pStu[i].room, pStu[i].phone);
	}

	return sum;
}

// ���ѧ����Ϣ�Ƿ������ѧ����Ϣ����
int checkStudentId(Student students[], int count, const char *id) 
{
    for (int i = 0; i < count; i++) {
        if (strcmp(students[i].id, id) == 0) {
            return 1; // ����
        }
    }
    return 0; // ������
}

// �����ۺϳɼ�
float calculateTotalScore(float usual, float lab, float exam) 
{
	if(lab != -1) 
	{
		return usual * 0.15 + lab * 0.15 + exam * 0.7;
	}
    return usual * 0.3 + exam * 0.7;
}

// ���õȼ�ѧ����
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

// ¼��
void addScoreRecord(char *FileName_A, char* FileName_B, Student *student) 
{
    int studentCount = readStudentsFromFile(FileName_A, student);
    
    if (studentCount == 0) {
        printf("û��ѧ����Ϣ�������� %s �����ѧ������\n", FileName_A);
        return;
    }

    Grades grades;
    char id[20];
    
    // д���ļ�
    FILE *file = fopen(FileName_B, "a+"); 
    if (file == NULL) {
        printf("�޷����ļ� %s\n", FileName_B);
        return;
    }

    // ���ļ�Ϊ��ʱ��ӱ�ͷ
    fseek(file, 0, SEEK_END);

    if (ftell(file) == 0) {
        fprintf(file, "ѧ�� �γ̱�� �γ����� ѧ�� ƽʱ�ɼ� ʵ��ɼ� ����ɼ� �ۺϳɼ�\n");
        fseek(file, 0, SEEK_END);
    }

    while (1) {
        printf("������ѧ�ţ�����0�˳�����");
        scanf("%s", id);
        
        if (strcmp(id, "0") == 0) break;
        
        // ���ѧ���Ƿ����
        if (!checkStudentId(student, studentCount, id)) {
            printf("���󣺸�ѧ�Ų������� %s �У�\n", FileName_A);
            continue;
        }
        
        strcpy(grades.id, id);
        
        printf("������γ̱�ţ�");
        scanf("%s", grades.courseId);
        
        printf("������γ����ƣ�");
        scanf("%s", grades.courseName);
        
        printf("������ѧ�֣�");
        scanf("%d", &grades.credits);
        
        printf("������ƽʱ�ɼ���");
        scanf("%f", &grades.usualScore);
        
        printf("������ʵ��ɼ���");
        scanf("%f", &grades.labScore);
        
        printf("���������ɼ���");
        scanf("%f", &grades.examScore);
        
        // 计算综合成绩
        grades.totalScore = calculateTotalScore(grades.usualScore, grades.labScore, grades.examScore);
        
        
        if (file == NULL) {
            printf("�޷����ļ� %s\n", FileName_B);
            return;
        }
        
        fprintf(file, "%s %s %s %d %.1f %.1f %.1f %.1f\n",
                grades.id, grades.courseId, grades.courseName, 
                calculateCredits(grades.credits,grades.totalScore), grades.usualScore, grades.labScore,
                grades.examScore, grades.totalScore);
        
        fclose(file);
        printf("�ɼ���¼��ӳɹ���\n");
    }
}