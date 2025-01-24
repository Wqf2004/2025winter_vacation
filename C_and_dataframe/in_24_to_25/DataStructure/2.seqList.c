/* 第一次上机作业：
1）创建一个顺序表：从键盘读入一组整数，按输入顺序放入顺序表，并将创建好的顺序表元素依次输出到屏幕上。
2）在已创建好的顺序表中插入一个元素：从键盘读入需插入的元素值和插入位置，调用插入函数完成插入操作；
然后将顺序表元素依次输出到屏幕上。
3）在已创建好的顺序表中删除一个元素：从键盘读入欲删除的元素位置（序号），调用删除函数完成删除操作；
然后将顺序表元素依次输出到屏幕上。
4）统计顺序表中元素值为负数的元素个数，并对其进行删除，然后将顺序表元素依次输出到屏幕上。
*/
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#define SLEEP(x) Sleep(x * 1000)
// 定义顺序表的最大长度
#define MAXSIZE 100

// 给ElemType赋予int类型，或给int创建了一个别名ElemType
typedef int ElemType;
// 定义顺序表结构体变量
typedef struct
{
    ElemType data[MAXSIZE];
    int length; // 用于存储当前顺序表的长度 
} SqList;

//创建一个顺序表：从键盘读入一组整数，按输入顺序放入顺序表
void CreateList(SqList *L)
{
    int i;
    printf("请输入顺序表的长度：");
    scanf("%d", &L->length);
    printf("请输入顺序表的元素：");
    for (i = 0; i < L->length; i++)
    {
        scanf("%d", &L->data[i]);
    }
}
//将创建好的顺序表元素依次输出到屏幕上
void PrintList(SqList L)
{
    int i;
    for (i = 0; i < L.length; i++)
    {
        printf("%d ", L.data[i]);
    }
    printf("\n");
}
/*在已创建好的顺序表中插入一个元素：从键盘读入需插入的元素值和插入位置，
调用插入函数完成插入操作；然后将顺序表元素依次输出到屏幕上。*/
void InsertList(SqList *L, int i, ElemType e)
{
    int j;
    if (i < 1 || i > L->length + 1)
    {
        printf("插入位置不合法\n");
        return;
    }
    if (L->length >= MAXSIZE)
    {
        printf("顺序表已满\n");
        return;
    }
    for (j = L->length; j >= i; j--)
    {
        L->data[j] = L->data[j - 1];
    }
    L->data[i - 1] = e;
    L->length++;
}
//在已创建好的顺序表中删除一个元素：从键盘读入欲删除的元素位置（序号），调用删除函数完成删除操作；然后将顺序表元素依次输出到屏幕上。
void DeleteList(SqList *L, int i)
{
    int j;
    if (i < 1 || i > L->length)
    {
        printf("删除位置不合法\n");
        return;
    }
    if (L->length == 0)
    {
        printf("顺序表为空\n");
        return;
    }
    for (j = i; j < L->length; j++)
    {
        L->data[j - 1] = L->data[j];
    }
    L->length--;
}
//统计顺序表中元素值为负数的元素个数，并对其进行删除，然后将顺序表元素依次输出到屏幕上。
void DeleteMinus(SqList *L)
{
    int i, count = 0;
    for (i = 0; i < L->length; i++)
    {
        if (L->data[i] < 0)
        {
            count++;
        }
    }
    printf("负数个数为：%d\n", count);
    for (i = 0; i < L->length; i++)
    {
        if (L->data[i] < 0)
        {
            DeleteList(L, i + 1);
            i--;
        }
    }
}

int main()
{
    SqList L;
    CreateList(&L);
    PrintList(L);
    int i, e;
    printf("请输入要插入位置和插入的元素值：");
    scanf("%d %d", &i, &e);
    InsertList(&L, i, e);
    PrintList(L);
    printf("请输入要删除的元素位置：");
    scanf("%d", &i);
    DeleteList(&L, i);
    PrintList(L);
    SLEEP(2);
    DeleteMinus(&L);
    PrintList(L);
    return 0;
}