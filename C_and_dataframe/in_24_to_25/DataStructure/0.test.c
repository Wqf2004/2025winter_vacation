#include<stdio.h>
#define N 1
int main()
{
    int i;
    int a[N];
    int b = scanf("%d",&a[0]) == 1;
    for(i = 1; i<N; i++) 
    {
        if(b)
        {
            b = (scanf("%d",&a[i])==1);
        }
        if(i >= N-1 || b == 0) break; 
    }
    printf("数组中的元素为：");
    for(int j = 0; j < i; j++){
        printf("%d ",a[j]);
    }

    /* output is 乱码
    char num[N];
    scanf("%c",&num[0]);
    int j = 0;
    while(num[j]!='\n' && j<N)
    {
        j++;
        scanf("%c",&num[j]);
    } 
    for(i=0;i<j;i++)
    {
        printf("%d",num[i]);
    }*/
    return 0;
}