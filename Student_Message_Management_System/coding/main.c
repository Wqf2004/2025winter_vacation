#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_STUDENTS 30
#define MAX_Grades 100
#define FILENAME_A "../dataset/a.txt" // ѧ����Ϣ�洢��ַ
#define FILENAME_B "../datasetb.txt"  // �ɼ���Ϣ�洢��ַ

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
    float credits;         // ѧ��
    float usualScore;    // ƽʱ�ɼ�
    float labScore;      // ʵ��ɼ�
    float examScore;     // ����ɼ�
    float totalScore;    // �����ɼ�
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

// ��ʾ���˵�
void showMenu() {
    printf("\n===== ѧ����Ϣ����ϵͳ(SMMS) =====\n");
    printf("L. ѧ���ɼ�����¼��\n");
    printf("A. ѧ��������Ϣ��ѯ\n");
    printf("B. ѧ���ɼ���Ϣ��ѯ\n");
    printf("Q. �˳�ϵͳ\n");
    printf("��ѡ�������");
}

// ��ʾѧ���ɼ�¼���Ӳ˵�
void showGradeEntryMenu() {
    printf("\n--- ѧ���ɼ�¼�� ---\n");
    printf("0. ������һ��\n");
    printf("1. ����(��ʼ)¼��\n");
    printf("��ѡ�������");
}

// ��ʾѧ�����������ѯ�Ӳ˵�
void showStudentMenu() {
    printf("\n--- ѧ��������Ϣ��ѯ ---\n");
    printf("0. ������һ��\n");
    printf("1. ��ѧ��(������)��ѯ\n");
    printf("2. ������Ų�ѯ\n");
    printf("��ѡ�������");
}

// ��ʾ�ɼ���ѯ�Ӳ˵�
void showScoreMenu() {
    printf("\n--- ѧ���ɼ���Ϣ��ѯ ---\n");
    printf("0. ������һ��\n");
    printf("1. ��ѧ�Ų�ѯ���пγ̳ɼ�\n");
    printf("��ѡ�������");
}

// ������
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
                    scanf(" %c", &choice); //ǰ����һ���ո��Ŀ����Ϊ������ǰ���Ļ��з�\n

                    switch(choice){
                        case '1':
                            printf("��������������¼��ĳɼ�����(�Ƽ�ֵ:5)��\n");
                            int Lcount;
                            scanf(" %d", &Lcount);
                            Student *pStu = (Student *)malloc(Lcount * sizeof(Student));
                            if (pStu == NULL) {
                                printf("�ڴ���侹Ȼʧ�ܣ���\n");
                                goto MAIN_MENU; // ǿ�Ʒ�����һ��
                            }
                            addGradesRecord(FILENAME_A, FILENAME_B, pStu); // ¼��ѧ���ɼ�
                            free(pStu); // �ͷ��ڴ�
                            break;
                        case '0':
                            goto MAIN_MENU;
                        default:
                            printf("��Чѡ������������\n");
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
                            printf("��Чѡ������������\n");
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
                            printf("��Чѡ������������\n");
                    }
                }
                break;
                
            case 'Q':
            case 'q':
                printf("��лʹ�ã��ټ���\n");
                return 0;
                
            default:
                printf("��Чѡ������������\n");
        }
    }
    
MAIN_MENU:
    return main(); // �ص����˵�
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

// ¼��
void addGradesRecord(char *FileName_A, char* FileName_B, Student *student) 
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
        scanf("%f", &grades.credits);
        
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
        
        fprintf(file, "%s %s %s %.1f %.1f %.1f %.1f %.1f\n",
                grades.id, grades.courseId, grades.courseName, 
                calculateCredits(grades.credits,grades.totalScore), grades.usualScore, grades.labScore,
                grades.examScore, grades.totalScore);
        
        fclose(file);
        printf("�ɼ���¼��ӳɹ���\n");
    }
}

int readGradesFromFile(char *FileName, Grades *pGrd)
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

	/*���뵽�ɼ�������*/
	int i = 0;
	while (fscanf(fp, "%s %s %s %f %f %f %f %f\n", pGrd[i].id, pGrd[i].courseId, pGrd[i].courseName, 
        &pGrd[i].credits, &pGrd[i].usualScore, &pGrd[i].labScore, &pGrd[i].examScore, &pGrd[i].totalScore) == 8) 
	{

		i++; // ÿ��ȡһ��ѧ������Ϣ������һ
	}
	fclose(fp);
    int sum = i;
	return sum;
}

// ���ܲ�ѯѧ��������Ϣ��֧��ѧ�ź�������ѯ��
void queryStudentSmart() 
{
    char input[50];
    printf("������Ҫ��ѯ��ѧ�Ż�������");
    scanf("%s", input);
    
    // ��ȡѧ������
    Student students[MAX_STUDENTS];
    int studentCount = readStudentsFromFile(FILENAME_A, students);
    
    // �����жϣ��������ȫ�����֣���ѧ�Ų�ѯ������������ѯ
    int isNumber = 1;
    for (int i = 0; input[i] != '\0'; i++) {
        if (!isdigit(input[i])) {  // ��Ҫ����"ctye.h"��׼��
            isNumber = 0;
            break;
        }
    }
    
    int found = 0;
    if (isNumber) {
        // ��ѧ�Ų�ѯ
        for (int i = 0; i < studentCount; i++) {
            if (strcmp(students[i].id, input) == 0) {
                printf("ѧ�ţ�%s\n", students[i].id);
                printf("������%s\n", students[i].name);
                printf("�Ա�%s\n", students[i].sex);
                printf("����ţ�%s\n", students[i].room);
                printf("�绰���룺%s\n", students[i].phone);
                printf("------------------------\n");
                found = 1;
                break;
            }
        }
        if (!found) printf("δ�ҵ���ѧ�ŵ�ѧ����Ϣ\n");
    } else {
        // ��������ѯ
        for (int i = 0; i < studentCount; i++) {
            if (strcmp(students[i].name, input) == 0) {
                printf("ѧ�ţ�%s\n", students[i].id);
                printf("������%s\n", students[i].name);
                printf("�Ա�%s\n", students[i].sex);
                printf("����ţ�%s\n", students[i].room);
                printf("�绰���룺%s\n", students[i].phone);
                printf("------------------------\n");
                found = 1;
                break;
            }
        }
        if (!found) printf("δ�ҵ���������ѧ����Ϣ\n");
    }
}

// ������Ų�ѯѧ��������Ϣ
void queryStudentsByDorm() 
{
    char dorm[20];
    printf("������Ҫ��ѯ������ţ�");
    scanf("%s", dorm);

    // ��ȡѧ������
    Student students[MAX_STUDENTS];
    int studentCount = readStudentsFromFile(FILENAME_A, students);
    
    int found = 0;
    for (int i = 0; i < studentCount; i++) {
        if (strcmp(students[i].room, dorm) == 0) {
            printf("ѧ�ţ�%s\n", students[i].id);
            printf("������%s\n", students[i].name);
            printf("�Ա�%s\n", students[i].sex);
            printf("����ţ�%s\n", students[i].room);
            printf("�绰���룺%s\n", students[i].phone);
            printf("------------------------\n");
            found = 1;
        }
    }
    
    if (!found) {
        printf("δ�ҵ��������ѧ����Ϣ\n");
    }
}

// ��ѧ�Ų�ѯ�ɼ���Ϣ
void queryScoresById() 
{
    char id[20];
    printf("������Ҫ��ѯ��ѧ�ţ�");
    scanf("%s", id);
    
    // ��ȡ�ɼ�����
    Grades scores[MAX_Grades];
    int scoreCount = readGradesFromFile(FILENAME_B, scores);

    // ��ѯ����ʾ�ɼ�
    int scoreFound = 0;
    for (int i = 0; i < scoreCount; i++) {
        if (strcmp(scores[i].id, id) == 0) {
            printf("�γ̱�ţ�%s\n", scores[i].courseId);
            printf("�γ����ƣ�%s\n", scores[i].courseName);
            printf("ѧ�֣�%.1f\n", scores[i].credits);
            printf("ƽʱ�ɼ���%.1f\n", scores[i].usualScore);
            printf("ʵ��ɼ���%.1f\n", scores[i].labScore);
            printf("����ɼ���%.1f\n", scores[i].examScore);
            printf("�ۺϳɼ���%.1f\n", scores[i].totalScore);
            printf("------------------------\n");
            scoreFound = 1;
        }
    }
    
    if (!scoreFound) {
        printf("δ�ҵ���ѧ���ĳɼ���¼\n");
    }
}

