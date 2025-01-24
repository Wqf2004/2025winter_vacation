/* 数据结构（C语言）课后习题：
1、给定一个排序数组和一个目标值，在数组中找到目标值，并返回其索引。
如果目标值不存在于数组中，返回它将会被按顺序插入的位置。并计算时间复杂度。
（请先写出算法思想和实现步骤，再写代码）

算法思想：
1. 使用二分查找算法在排序数组中查找目标值。
2. 如果找到目标值，返回其索引。
3. 如果未找到目标值，返回它将会被按顺序插入的位置。

实现步骤：
1. 初始化两个指针，left和right，分别指向数组的起始和结束位置。
2. 在while循环中，计算中间位置mid。
3. 比较nums[mid]和target：
   - 如果nums[mid]等于target，返回mid。
   - 如果nums[mid]小于target，移动left指针到mid+1。
   - 如果nums[mid]大于target，移动right指针到mid-1。
4. 循环结束后，left指针的位置就是目标值应该插入的位置。
5. 返回left。

时间复杂度：
    O(log n)，其中n是数组的长度。每次循环都将搜索范围缩小一半，因此时间复杂度是对数级别的。
*/

#include <stdio.h>

int searchInsert(int* nums, int numsSize, int target) {
    int left = 0, right = numsSize - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) {
            return mid;
        } else if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return left;
}


int main() {
    int nums[] = {1, 3, 5, 6, 7};
    int target = 0;
    int numsSize = sizeof(nums) / sizeof(nums[0]);
    
    int result = searchInsert(nums, numsSize, target);
    
    if (result < numsSize && nums[result] == target) {
        printf("目标值 %d 在数组中的位置是: %d\n", target, result + 1);
    } else {
        printf("目标值 %d 的插入位置是: %d\n", target, result + 1);
    }
    // 计算时间复杂度
    // O(log n)
    printf("时间复杂度: O(log n)\n");
    return 0;
}
