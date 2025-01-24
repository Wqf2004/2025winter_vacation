#include <stdio.h>
#include <stdlib.h>
typedef int ElemType;

// 链栈节点类型定义
typedef struct node
{
    ElemType data;
    struct node *next;
}SNode;

// 进栈函数(这是一个有头结点的栈)
void push(SNode *top, ElemType x)
{
    SNode *p;
    p = (SNode *)malloc(sizeof(SNode));
    p->data = x;
    p->next = top->next;
    top->next = p;
}

// 出栈函数
ElemType pop(SNode *top)
{
    SNode *p;
    ElemType x;
    if(top->next == NULL)
    {
        printf("链栈为空\n");
        return -1;
    }
    p = top->next;
    top->next = p->next;
    x = p->data;
    free(p);
    return x;
}

// min函数返回栈元素中的最小值
int min(SNode *top)
{
    SNode *p = top->next;
    int minVal = p->data;
    while(p != NULL)
    {
        if(p->data < minVal)
        {
            minVal = p->data;
        }
        p = p->next;
    }
    return minVal;
}


// 主函数
int main()
{
    SNode *top;
    ElemType x;
    top = (SNode *)malloc(sizeof(SNode));
    top->next = NULL;
    printf("请输入数据元素，输入0结束：\n");
    scanf("%d", &x);
    while(x != 0)
    {
        push(top, x);
        scanf("%d", &x);
    }
    // 输出进栈后的数据元素
    printf("进栈后的数据元素为（输出的第一个元素为栈顶元素）：\n");
    SNode *p = top->next;
    while(p != NULL)
    {
        printf("%d ", p->data);
        p = p->next;
    }
    // 输出最小值
    printf("\n最小值为：%d\n", min(top));
    // 调用两次出栈函数
    pop(top);
    pop(top);
    // 输出两次出栈后的数据元素
    printf("\n两次出栈后的数据元素为（第一个为两次出栈后的栈顶元素）：\n");
    p = top->next;
    while(p != NULL)
    {
        printf("%d ", p->data);
        p = p->next;
    }
    printf("\n");
    return 0;
}