#include <stdio.h>
#include <string.h>

struct student
{
    int num;
    char *name;
    float score[3];
};//结构体

void main()
{
    struct student stu;

    stu.num = 7;
    stu.name = "wenqipeak";
    stu.score[0]=99;
    stu.score[1]=95;
    stu.score[2]=89;

    printf("%d",stu.num);
}