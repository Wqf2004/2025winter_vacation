/* 数据结构（C语言）课后习题：
3、如果进站的车厢序列为123456，则能否得到435612和135426的出站序列，
并请说明为什么不能得到或者如何得到？（写出进栈和出栈的栈操作序列）

算法思想：
1. 出站序列435612：
    - 进站：1, 2, 3, 4
    - 出站：4, 3
    - 进站：5
    - 出站：5
    - 进站：6
    - 出站：6, 2, 1
    可以得到出站序列435621，无法得到435612，
    因为435612的出站序列中，1在2之前出站，而123456的进站序列中，1在2之前进站。

2. 出站序列135426：
    - 进站：1
    - 出站：1
    - 进站：2, 3
    - 出站：3
    - 进站：4, 5
    - 出站：5, 4
    - 出站：2
    - 进站：6
    - 出站：6
    可以得到出站序列135426。
*/

#include <stdio.h>
#include <stdlib.h>

// 定义栈结构
typedef struct Stack {
    int* array;
    int top;
    int capacity;
} Stack;


// 创建栈
Stack* createStack(int capacity) {
    Stack* stack = (Stack*)malloc(sizeof(Stack));
    stack->array = (int*)malloc(capacity * sizeof(int));
    stack->top = -1;
    stack->capacity = capacity;
    return stack;
}

// 检查栈是否为空
int isEmpty(Stack* stack) {
    return stack->top == -1;
}

// 清空栈
void freeStack(Stack* stack) {
    free(stack->array);
    free(stack);
}

// 入栈
void push(Stack* stack, int item) {
    if (stack->top == stack->capacity - 1) {
        printf("Stack is full\n");
        return;
    }
    stack->array[++stack->top] = item;
}

// 出栈
int pop(Stack* stack) {
    if (isEmpty(stack)) {
        printf("Stack is empty\n");
        return -1;
    }
    return stack->array[stack->top--];
}

// 获取栈顶元素
int peek(Stack* stack) {
    if (isEmpty(stack)) {
        printf("Stack is empty\n");
        return -1;
    }
    return stack->array[stack->top];
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

int main() {
    int in[] = {1, 2, 3, 4, 5, 6};
    int out1[] = {4, 3, 5, 6, 1, 2};
    int out2[] = {1, 3, 5, 4, 2, 6};
    int n = sizeof(in) / sizeof(in[0]);

    if (checkAndPrintSequence(in, out1, n)) {
        printf("Can get sequence 435612\n");    
    } 
    else {
        printf("Cannot get sequence 435612\n");
    }

    if (checkAndPrintSequence(in, out2, n)) {
        printf("Can get sequence 135426\n");
    } 
    else {
        printf("Cannot get sequence 135426\n");
    }
    return 0;
}
