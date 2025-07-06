#include <stdio.h>
#include <stdlib.h>

#define MAX_STUDENTS 30

typedef struct
{
	char id[10];
	char name[10];
	char sex[8];
	char room[8];
	char phone[20];
}Student;
void ReadFile(char *FileName, Student *pStu);


int main()
{
    Student *pStu = (Student *)malloc(MAX_STUDENTS * sizeof(Student));
    if (pStu == NULL) {
        printf("Memory allocation failed.\n");
        return 1;
    }
    printf("Reading file...\n");
	char filename[] = "../dataset/a.txt"; // 文件名
	ReadFile(filename, pStu); // 调用函数读取文件
    free(pStu); // 释放动态分配的内存
	return 0;
}

void ReadFile(char* FileName, Student* pStu)
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

	/*输出数据*/
	int sum = i;
	for (i = 0; i < sum; i++)
	{
		printf("%s %s %s %s %s\n", pStu[i].id, pStu[i].name, pStu[i].sex, pStu[i].room, pStu[i].phone);
	}
}