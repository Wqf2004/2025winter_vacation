#include<stdio.h>
#include<stdlib.h>
#define N 5
// malloc()生成的是一个指针变量，可在其内部得到一个数组，遍历即可
void check(int*);
void main()
{
    int*pt,i;
    pt = malloc(N*sizeof(int));
  for(i=0;i<N;i++){
        scanf("%d",pt+i);//已经是一个地址变量了
    }
    check(pt);  
}
void check(int*p)
{
    printf("They are fail:");
    for(int i = 0;i<N;i++){
        if(*(p+i)<60){
            printf("%d ",*(p+i));//p[i]
        }
    }
    printf("\n");
}