//导入最常见的四个包
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>
#include <math.h>

int count = 0;//需要作为外部变量
//实现汉诺塔并计数
int move(int n, char a, char b, char c)
{
    //或者：static int count = 0//作为静态变量
    if (n == 1)
    {
        printf("%c-->%c\n", a, c);
        count++;
    }
    else
    {
        move(n - 1, a, c, b);
        printf("%c-->%c\n", a, c);
        count++;
        move(n - 1, b, a, c);
    }
    return count;
}

int main()
{
    //测试程序运行时间（初始化时间必须要放在主函数里）
    clock_t start, end;
    start = clock();
    int n, sum;
    printf("请输入汉诺塔的总数：");
    scanf("%d", &n);
    sum = move(n, 'A', 'B', 'C');
    printf("总共移动%d次\n", sum);
    end = clock();
    printf("程序运行时间为：%lf s\n", (double)(end - start) / CLOCKS_PER_SEC);
    return 0;
}

