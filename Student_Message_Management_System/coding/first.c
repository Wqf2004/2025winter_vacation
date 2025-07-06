
#include<stdio.h>
#include<stdlib.h>

typedef struct
{
	char id[8];
	char name[10];
	char sex[8];
	char room[8];
	char phone[20];
}Student;

int main()
{
	Student a[100];
	FILE* fp;
	char filename[] = "a.txt";
	fp = fopen(filename, "r");
	if (fp == NULL)
	{
		printf("The file is error.\n");
		exit(0);
	}
	int i = 0;
	while (!feof(fp))
	{
		int b = fscanf(fp, "%s %s %s %s %s\n", &a[i].id, &a[i].name, &a[i].sex, &a[i].room, &a[i].phone);
		i++;
	}
	fclose(fp);
	int n = i;
	for (i = 0; i < n; i++)
	{
		printf("%s %s %s %s %s\n", a[i].id, a[i].name, a[i].sex, a[i].room, a[i].phone);
	}
	return 0;
}