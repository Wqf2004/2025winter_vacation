//c语言常用包
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <stdbool.h>

//搜索顺序数组中的某个值返回其下标，当找不到时输出0
// 如有重复，返回第一个值对应的下标
int search(int arr[], int n, int x)
{
    int i;
    for (i = 0; i < n; i++)
    {
        if (arr[i] == x)
        {
            return i+1;
        }
    }
    return 0;
}

int main()
{
    int arr[] = {1, 3, 3, 4, 5, 8, 11};
    int n = sizeof(arr) / sizeof(arr[0]);
    int x;
    printf("Enter the value to search: ");
    scanf("%d", &x);
    int index = search(arr, n, x);
    if (index)
    {
        printf("Value %d found at index %d\n", x, index);
    }
    else
    {
        printf("Value %d not found in the array\n", x);
    }
    return 0;
}
