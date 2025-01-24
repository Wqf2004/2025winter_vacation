#include <stdio.h>
#include <stdlib.h>
// 带监视哨的顺序查找
int sequentialSearch(int arr[], int size, int target) {
    int last = arr[size - 1];
    arr[size - 1] = target; // 让数组的最后一个值等于目标值，使得while循环可以不加额外的判断就停止
    int i = 0;
    while (arr[i] != target) {
        i++;
    }
    if(i < size -1 || last == target)
    {
        return i;
    }
    else{
        return -1; // 表示没有找到
    }
}
// 二分查找：使用二分查找要求数组为递增数组
int binarySearch(int arr[], int size, int target) {
    int left = 0;
    int right = size - 1;
    int mid;
    while (left <= right) {
        mid = left + (right - left) / 2;
        if (arr[mid] == target) {
            return mid; // 找到了
        }
        if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1; // 表示没有找到
}

// 主函数调用
int main() {
    int arr[] = {1,6,8,9,10,29,78};
    int size = sizeof(arr) / sizeof(arr[0]);
    int target = 29;
    // 顺序查找
    int indexResult = sequentialSearch(arr, size, target);
    if(indexResult >= 0)
    {
        printf("顺序查找结果为:%d",indexResult);
    }
    else{
        printf("表中没有该元素");
    }

    // 二分查找
    indexResult = binarySearch(arr, size, target);
    if(indexResult >= 0)
    {
        printf("二分查找结果为:%d",indexResult);
    }
    else{
        printf("表中没有该元素");
    }
    return 0;
}