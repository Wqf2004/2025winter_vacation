#include<stdio.h>
//#include<stdli
void swap(int*,int*);
int main()
{
    int a = 100;
    int b = 1;
    swap(&a,&b);
    printf("a = %d,b = %d",a,b);

}
void swap(int*p1,int*p2)
{
    int temp;
    temp = *p1;
    *p1 = *p2;
    *p2 = temp;
}