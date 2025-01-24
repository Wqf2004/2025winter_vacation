/* 数据结构（C语言）课后习题：
4、有6个数字，其入栈顺序为123456, 在各种可能的出栈顺序中，
第一个出栈元素为3且第二个出栈元素为4的出栈序列有哪些?

主要函数的思想和步骤：
checkAndPrintSequence：检查并打印有效序列
上面这个函数的步骤是什么：
1. 初始化一个栈，用于模拟入栈和出栈操作。
2. 遍历入栈序列，将元素依次入栈。
3. 当栈顶元素与出栈序列的当前元素相等时，将栈顶元素出栈，并移动出栈序列的指针。
4. 重复步骤2和3，直到入栈序列遍历完毕。
5. 检查栈是否为空，如果为空，则说明所有元素都已按顺序出栈。
6. 如果栈不为空，则继续遍历入栈序列，将剩余元素入栈。
7. 重复步骤3和4，直到栈为空。
generatePermutations：生成所有可能的排列
1. 初始化一个数组，用于存储入栈序列。
2. 生成所有可能的排列。
3. 检查并打印有效序列。
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_N 10

// 定义栈结构
typedef struct {
    int *data;
    int top;
    int capacity;
} Stack;

// 创建栈
Stack* createStack(int capacity) {
    Stack* stack = (Stack*)malloc(sizeof(Stack));
    stack->data = (int*)malloc(capacity * sizeof(int));
    stack->top = -1;
    stack->capacity = capacity;
    return stack;
}

// 入栈
void push(Stack *s, int value) {
    s->data[++s->top] = value;
}

// 出栈
int pop(Stack *s) {
    return s->data[s->top--];
}

// 查看栈顶元素
int peek(Stack *s) {
    return s->data[s->top];
}

// 检查栈是否为空
int isEmpty(Stack *s) {
    return s->top == -1;
}

// 释放栈
void freeStack(Stack *s) {
    free(s->data);
    free(s);
}
// 检查并打印序列
int checkAndPrintSequence(int *in, int *out, int n) {
    Stack* stack = createStack(n);  // 创建一个局部栈用于模拟入栈和出栈
    int i = 0, j = 0;   // 初始化两个量，一个用来统计入栈的数目，另一个用来统计出栈的数目

    while (i < n || !isEmpty(stack)) { // 入栈的数目小于n或栈不为空时继续循环
        if (in[i] == out[j]) { // 如果入栈的元素等于出栈的元素
            printf("Push %d, Pop %d\n", in[i], in[i]); // 直接对当前元素进行入栈和出栈操作
            i++; // 入栈的数目加一
            j++; // 出栈的数目加一
        } else if (!isEmpty(stack) && peek(stack) == out[j]) { // 如果栈不为空且栈顶元素等于出栈的元素
            printf("Pop %d\n", out[j]); // 直接对当前元素进行出栈操作
            pop(stack); // 出栈
            j++; // 出栈的数目加一
        } else if (i < n) { // 如果入栈的数目小于n
            printf("Push %d\n", in[i]); // 对当前元素进行入栈操作
            push(stack, in[i++]); // 入栈
        } else {
            break; // 如果入栈的数目大于n，则跳出循环
        }
    }
    

    freeStack(stack);
    return (j == n);
}

// 交换两个元素
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// 生成所有可能的排列
void generatePermutations(int *fixed, int *variable, int n, int k) {
    int in[] = {1, 2, 3, 4, 5, 6};
    int out[MAX_N];
    int count = 0;

    // 初始化输出数组
    memcpy(out, fixed, k * sizeof(int));
    memcpy(out + k, variable, n * sizeof(int));

    do {
        // 检查并打印有效序列
        printf("Trying sequence: ");
        for (int j = 0; j < n + k; j++) {
            printf("%d ", out[j]);
        }
        printf("\n");

        if (checkAndPrintSequence(in, out, n + k)) {
            printf("Valid Sequence %d:\n", ++count);
            for (int j = 0; j < n + k; j++) {
                printf("%d ", out[j]);
            }
            printf("\n\n");
        }
        else{
            printf("Invalid Sequence\n\n");
        }
        // 生成下一个排列
        int i = n + k - 1;
        while (i > k && out[i-1] >= out[i]) {
            i--;
        }
        if (i <= k) {
            break;
        }
        int j = n + k - 1;
        while (out[j] <= out[i-1]) {
            j--;
        }
        swap(&out[i-1], &out[j]);
        j = n + k - 1;
        while (i < j) {
            swap(&out[i], &out[j]);
            i++;
            j--;
        }
    } while (1);

    printf("Total valid sequences: %d\n", count);
}

int main() {
    int fixed[] = {3, 4};
    int variable[] = {1, 2, 5, 6};
    int n = sizeof(variable) / sizeof(variable[0]);
    int k = sizeof(fixed) / sizeof(fixed[0]);

    generatePermutations(fixed, variable, n, k);

    return 0;
}
