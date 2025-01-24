#include <stdio.h>
#include <stdlib.h>
// 带有监视哨的冒泡排序（目的是在合适的情况下终止排序）
void bubbleSort(int arr[], int size) {
    for(int i = 0; i < size - 1; i++)
    {
        int swapped = 1; // 设置一个监视哨用于判断是否进行交换
        for(int j = 0; j < size - i - 1; j++)
        { // 冒泡排序算法的主干
            if(arr[j] > arr[j+1])
            {
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
                swapped = 0;
            }
        }
        if(swapped)
        {
            break;
        }
    }
}
// 快速排序进行基准值位置调整的过程（一趟快排序）
int partition(int arr[], int low, int high)
{
    int pivot = arr[high]; // 找一个基准值这里选取的是最后一个（一般选择第一个）
    int j = low - 1; // 假设lowd=1，则我们将j看作是一个对arr中小于pivot的数的一个计数
    // 这里我们要注意我们始终操作的是一个数组，只是操作了数组的不同部分
    for(int i = low; i < high; i++)
    {
        if(arr[i] < pivot)
        {
            j++; // 计数的同时，将把low到high-1范围内的数大大小小分开
            int temp = arr[j];
            arr[j] = arr[i];
            arr[i] = temp;
        }
    }
    // 现在我们把arr中的j处的值与pivot进行交换，就实现了左边的数都小于pivot，右边的数大于等于pivot
    arr[high] = arr[j];
    arr[j] = pivot;
    return j;
}
// 快速排序的递归过程
void quikSort(int arr[], int low, int high)
{
    if(low < high) // 递归终止：low和high打照面的时候结束函数
    {
        int pivot = partition(arr, low, high);
        quickSort(arr, low, pivot - 1);
        quickSort(arr, pivot + 1, high);
    }

}
// 归并排序
void merge(int [],int,int,int);
void mergeSort(int arr[], int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

void merge(int arr[], int left, int mid, int right) {
    int i, j, k;
    int n1 = mid - left + 1;
    int n2 = right - mid;
    int L[n1], R[n2];
    for (i = 0; i < n1; i++)
        L[i] = arr[left + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[mid + 1 + j];

    i = 0; 
    j = 0; 
    k = left; 

    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}

// 主函数调用
int main() {
    int arr[] = {64, 34, 25, 12, 22, 11, 90}; // 示例数组
    int size = sizeof(arr) / sizeof(arr[0]); // 计算数组大小

    bubbleSort(arr, size); // 调用冒泡排序

    // 打印排序后的数组
    printf("排序后的数组: \n");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    return 0; // 返回成功
}