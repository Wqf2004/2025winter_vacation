#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_STUDENTS 30
#define MAX_Grades 100
#define FILENAME_A "../dataset/a.txt" // ѧ����Ϣ�洢��ַ
#define FILENAME_B "../dataset/b.txt"  // �ɼ���Ϣ�洢��ַ

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
    char courseName[80]; // �γ�����
    float credits;         // ѧ��
    float usualScore;    // ƽʱ�ɼ�
    float labScore;      // ʵ��ɼ�
    float examScore;     // ����ɼ�
    float totalScore;    // �����ɼ�
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

// ��ʾ���˵�
void showMenu() {
    printf("\n===== ѧ����Ϣ����ϵͳ(SMMS) =====\n");
    printf("L. ѧ���ɼ�����¼��\n");
    printf("A. ѧ��������Ϣ��ѯ\n");
    printf("B. ѧ���ɼ���Ϣ��ѯ\n");
    printf("D. ѧ����Ϣɾ��\n");
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

// ��ʾɾ���Ӳ˵�
void deleteStudentMenU(){
    printf("\n--- ѧ����Ϣɾ�� ---\n");
    printf("0. ������һ��\n");
    printf("1. ��ѧ��ɾ��ĳ��ѧ����ȫ����Ϣ\n");
    printf("��ѡ�������");
}

// ��ʾ�����Ӳ˵�
void showSortMenu() {
    printf("\n--- ѧ���ɼ����� ---");
    printf("\n1. ���ۺϳɼ���������");
    printf("\n2. ���ۺϳɼ���������");
    printf("\n3. ���γ�ѧ����������");
    printf("\n4. ���γ�ѧ�ֽ�������");
    printf("\n5. ������һ��");
    printf("\n��ѡ�������");
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
                        {  // case��ǩ��������Ҳ��Ҫ�ŵ���������
                            printStudent();
                            Student *pStu = (Student *)malloc(MAX_Grades * sizeof(Student));
                            if (pStu == NULL) {
                                printf("�ڴ���侹Ȼʧ�ܣ���\n");
                                goto MAIN_MENU; // ǿ�Ʒ�����һ��
                            }
                            addGradesRecord(FILENAME_A, FILENAME_B, pStu); // ¼��ѧ���ɼ�
                            free(pStu); // �ͷ��ڴ�
                            break;
                        }
                        case '0':
                            goto MAIN_MENU;
                        default:
                            printf("��Чѡ������������\n");
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
                            printf("��Чѡ������������\n");
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
                            printf("��Чѡ������������\n");
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
                            printf("��Чѡ������������\n");
                            getchar();getchar();getchar();
                    }
                }
                
            case 'Q':
            case 'q':
                printf("��лʹ�ã��ټ���\n");
                return 0;
                
            default:
                printf("��Чѡ������������\n");
                getchar();getchar();getchar();
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
    printf("ѧ����ѧ�ż�������Ϣ��\n");
	fclose(fp);

	int sum = i;
	return sum;
}

/*��ӡ��ѧ������Ϣ*/
void printStudent()
{
    // ��ȡѧ������
    Student students[MAX_STUDENTS];
    int sum = readStudentsFromFile(FILENAME_A, students);
    int i;
    for (i = 0; i < sum; i++)
	{
		printf("%s %s\t", students[i].id, students[i].name);
	}
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

// ����ѧ����Ϣ����ѧ������
char* returnStudentName(Student students[], int count, const char *id)
{
    for (int i = 0; i < count; i++) {
        if (strcmp(students[i].id, id) == 0) {
            return students[i].name; 
        }
    }
    return ""; 
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
    printf("\n");
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
        fprintf(file, "ѧ�� �γ̱�� �γ����� ѧ�� ƽʱ�ɼ� ʵ��ɼ� ����ɼ� �ۺϳɼ�");
        fprintf(file, "\n");
    }

    while (1) {
        fseek(file, 0, SEEK_END);
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
        
        // ���������ɼ�
        grades.totalScore = calculateTotalScore(grades.usualScore, grades.labScore, grades.examScore);
        
        if (file == NULL) {
            printf("�޷����ļ� %s\n", FileName_B);
            return;
        }
        
        fprintf(file, "%s %s %s %.1f %.1f %.1f %.1f %.1f\n",
                grades.id, grades.courseId, grades.courseName, 
                calculateCredits(grades.credits,grades.totalScore), grades.usualScore, grades.labScore,
                grades.examScore, grades.totalScore);
        
        printf("�ɼ���¼��ӳɹ���\n");
    }
    fclose(file);
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
            printf("------------------------\n");
            printf("ѧ�ţ�%s\n", students[i].id);
            printf("������%s\n", students[i].name);
            printf("�Ա�%s\n", students[i].sex);
            printf("����ţ�%s\n", students[i].room);
            printf("�绰���룺%s\n", students[i].phone);
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
    // ��ȡѧ����Ϣ
    Student students[MAX_STUDENTS];
    int studentCount = readStudentsFromFile(FILENAME_A, students);
    char *name = returnStudentName(students, studentCount, id);

    // ��ѯ����ʾ�ɼ�
    int found = 0;
    float allCredit = 0;
    for (int i = 0; i < scoreCount; i++) {
        if (strcmp(scores[i].id, id) == 0) {
            printf("ѧ�ţ�%s ", id);
            printf("������%s ", name);
            printf("�γ̱�ţ�%s ", scores[i].courseId);
            printf("�γ����ƣ�%s ", scores[i].courseName);
            printf("�ۺϳɼ���%.1f ", scores[i].totalScore);
            printf("ʵ��ѧ�֣�%.2f\n", scores[i].credits);
            printf("------------------------\n");
            found++;
            allCredit = allCredit + scores[i].credits;
        }
    }
    
    if (found) {
        printf("���ޣ�%d�ƣ�ʵ����ѧ��Ϊ��%.2f", found, allCredit);
    }
    else{
        printf("δ�ҵ���ѧ���ĳɼ���¼\n");
    }
}


// ɾ��ѧ������ɼ���Ϣ
void deleteStudent() 
{
    char id[20];
    printf("������Ҫɾ����ѧ��ѧ�ţ�");
    scanf("%s", id);

    // ��ȡѧ���ļ�
    Student students[MAX_STUDENTS];
    int count = readStudentsFromFile(FILENAME_A,students);
    if (count == 0) {
        printf("û��ѧ����Ϣ��ɾ��\n");
        return;
    }

    // ����ѧ��
    int found = 0;
    for (int i = 0; i < count; i++) {
        if (strcmp(students[i].id, id) == 0) {
            found = 1;
            break;
        }
    }

    if (!found) {
        printf("δ�ҵ�ѧ��Ϊ %s ��ѧ��\n", id);
        return;
    }

    // ȷ��ɾ��
    char confirm;
    printf("ȷ��Ҫɾ��ѧ��Ϊ %s ��ѧ���������гɼ���(y/n) ", id);
    scanf(" %c", &confirm);
    if (confirm != 'y' && confirm != 'Y') {
        printf("��ȡ��ɾ������\n");
        return;
    }

    // 1. ��a.txt��ɾ��ѧ��
    FILE *tempFile = fopen("temp_a.txt", "w");
    if (tempFile == NULL) {
        printf("�޷�������ʱ�ļ�\n");
        return;
    }

    for (int i = 0; i < count; i++) {
        if (strcmp(students[i].id, id) != 0) {
            // д���Ҫɾ��ѧ��������м�¼
            fprintf(tempFile, "%s %s %s %s %s\n",
                    students[i].id,
                    students[i].name,
                    students[i].sex,
                    students[i].room,
                    students[i].phone);
        }
    }
    fclose(tempFile);

    // �滻ԭ�ļ�
    remove(FILENAME_A);
    rename("temp_a.txt", FILENAME_A);

    // 2. ��b.txt��ɾ����Ӧ�ɼ�
    Grades scores[MAX_Grades];
    int scoreCount = readGradesFromFile(FILENAME_B, scores);
    
    tempFile = fopen("temp_b.txt", "w");
    if (tempFile == NULL) {
        printf("�޷�������ʱ�ļ�\n");
        return;
    }

    // д���ͷ
    fprintf(tempFile, "ѧ�� �γ̱�� �γ����� ѧ�� ƽʱ�ɼ� ʵ��ɼ� ����ɼ� �ۺϳɼ�\n");

    for (int i = 0; i < scoreCount; i++) {
        if (strcmp(scores[i].id, id) != 0) {
            // д���Ҫɾ��ѧ��������гɼ���¼
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

    // �滻ԭ�ļ�
    remove(FILENAME_B);
    rename("temp_b.txt", FILENAME_B);

    printf("ѧ��Ϊ %s ��ѧ���������гɼ��ѳɹ�ɾ��\n", id);
}


// ���ۺϳɼ�����
int compareTotalScoreAsc(const void *a, const void *b) {
    Grades *scoreA = (Grades *)a;
    Grades *scoreB = (Grades *)b;
    return (scoreA->totalScore - scoreB->totalScore) * 100; // ����100���⸡�������
}

// ���ۺϳɼ�����
int compareTotalScoreDesc(const void *a, const void *b) {
    return compareTotalScoreAsc(b, a); // ��ת����˳��ʵ�ֽ���
}

// ��ѧ������
int compareCreditsAsc(const void *a, const void *b) {
    Grades *scoreA = (Grades *)a;
    Grades *scoreB = (Grades *)b;
    return scoreA->credits - scoreB->credits;
}

// ��ѧ�ֽ���
int compareCreditsDesc(const void *a, const void *b) {
    return compareCreditsAsc(b, a); // ��ת����˳��ʵ�ֽ���
}


