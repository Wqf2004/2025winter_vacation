#include<stdio.h>
#include<malloc.h>
#include<stdlib.h>

/*创建单链表*/
typedef struct poly
{
	int coeff;
	int exp;
	struct poly *next;
}PNode, PLinklist;

/*链表初始化*/
int Init(PLinklist *head)
{
	head=(PLinklist*)malloc(sizeof(PNode));
    if(head)
    {
        head->next=NULL;
        return 1;
    }
    else
        return 0;
}

/*尾插法创建链表*/
int createFromTail(PLinklist *head)
{
	PLinklist *pTemp,*pHead;
	int n; /*存放系数*/
    int exp; /*存放指数*/
    int i = 1; /*计数器提示用户输入第几项*/
    pHead = head;
    while(1) /*循环输入多项式的系数和指数，直到输入系数为0时结束循环*/
    {
        pTemp =(PLinklist*)malloc(sizeof(PNode));
        if(pTemp)
        {
            printf("请输入第%d项的系数和指数：", i);
            scanf("%d, %d", &n, &exp);
            if(n==0) /*输入系数为0时结束循环*/
                break;
            i++;
            (pTemp->coeff)=n; /*接收系数*/
            (pTemp->exp)=exp; /*接收指数*/
            (pTemp->next)=NULL;
            (pHead->next)=pTemp;
            pHead=pTemp;            
        }
        else
            return 0;
    }
    return 1;
}

/*两个多项式相加，该方法中两个表都是按指数顺序增长*/
void Polyadd(PLinklist *LA,PLinklist *LB)
{
    /*对指数进行对比分三类情况：A<B时将A链到LA后，A==B时比较系数，A>B时将B链到表中*/
    PLinklist *p1,*p2;
    p1 = LA->next; /*用于在LA中移动*/
    p2 = LB->next; /*用于在LB中移动*/
    /*即LA和LB是p1,p2的前驱*/
    while(p1&&p2)
    {
        /*谁的指数小谁就跟在后面跑*/
        if(p1->exp < p2->exp)   
        {
            LA->next=p1;
            LA=p1;
            p1=p1->next;
        }
        else if(p1->exp > p2->exp)
        {
            LA->next=p2;
            LA=p2;
            p2=p2->next;
        }
        else
        {
            p1->coeff += p2->coeff;/*进行系数的加减运算*/
            if(p1->coeff!=0)
            {
                LA->next=p1;
                LA=p1;
            }
            p1=p1->next;
            p2=p2->next;
        }
    }
    if(p1)
        LA->next=p1;
    if(p2)
        LA->next=p2;
}

/*输出多项式*/
void printPoly(PLinklist *head)
{
    PLinklist *pTemp;
    pTemp=head->next;
    while(pTemp)
    {
        if(pTemp->exp)
            printf("%dx^%d", pTemp->coeff, pTemp->exp);
        else
            printf("%d", pTemp->coeff); 
        pTemp=pTemp->next;
        if(pTemp)
            printf(" + ");
    }
    printf("\n");
}

/*释放链表*/
void freePoly(PLinklist *head)
{
    PLinklist *pTemp;
    while(head)
    {
        pTemp=head;
        head=head->next;
        free(pTemp);
    }
}

/*主函数*/
void main()
{
	PLinklist LA, LB;
	Init(&LA);
	Init(&LB);
    printf("请按指数递增顺序输入多项式的系数和指数\n");
	printf("请输入第一个多项式：\n");
	createFromTail(&LA);
	printf("请输入第二个多项式：\n");
	createFromTail(&LB);
	printf("第一个多项式为：");
	printPoly(&LA);
	printf("第二个多项式为：");
	printPoly(&LB);
	Polyadd(&LA, &LB);
	printf("相加后的多项式为：");
	printPoly(&LA);
}   