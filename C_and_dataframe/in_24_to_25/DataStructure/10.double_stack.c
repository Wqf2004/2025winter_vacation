/* 数据结构（C语言）课后习题：
6、使用两个栈来实现一个队列。
需要实现enqueue（入队）、dequeue（出队）和front（返回队首元素）操作。

算法思想：
1. 初始化两个栈，用于模拟入队和出队操作。
2. 入队操作：将元素压入栈1。
3. 出队操作：如果栈2为空，则将栈1中的所有元素依次弹出并压入栈2，然后从栈2中弹出栈顶元素。
4. 返回队首元素：如果栈2为空，则将栈1中的所有元素依次弹出并压入栈2，然后返回栈2的栈顶元素。
5. 检查栈是否为空：如果栈1和栈2都为空，则队列为空。
6. 检查栈是否已满：如果栈1已满，则队列已满。
*/

#include <stdio.h>
#include <stdlib.h>

// 定义栈结构
struct Stack {
    int* array;
    int top;
    int capacity;
};

// 创建栈
struct Stack* createStack(int capacity) {
    struct Stack* stack = (struct Stack*)malloc(sizeof(struct Stack));
    stack->array = (int*)malloc(capacity * sizeof(int));
    stack->top = -1;
    stack->capacity = capacity;
    return stack;
}

// 检查栈是否为空
int isEmpty(struct Stack* stack) {
    return stack->top == -1;
}

// 检查栈是否已满
int isFull(struct Stack* stack) {
    return stack->top == stack->capacity - 1;
}

// 入栈
void push(struct Stack* stack, int item) {
    if (isFull(stack)) {
        printf("Stack is full\n");
        return;
    }
    stack->array[++stack->top] = item;
}

// 出栈
int pop(struct Stack* stack) {
    if (isEmpty(stack)) {
        printf("Stack is empty\n");
        return -1;
    }
    return stack->array[stack->top--];
}

// 获取栈顶元素
int peek(struct Stack* stack) {
    if (isEmpty(stack)) {
        printf("Stack is empty\n");
        return -1;
    }
    return stack->array[stack->top];
}

// 定义队列结构，使用两个栈
struct Queue {
    struct Stack* stack1;
    struct Stack* stack2;
};

// 创建队列
struct Queue* createQueue(int capacity) {
    struct Queue* queue = (struct Queue*)malloc(sizeof(struct Queue));
    queue->stack1 = createStack(capacity);
    queue->stack2 = createStack(capacity);
    return queue;
}

// 入队操作
void enqueue(struct Queue* queue, int item) {
    push(queue->stack1, item);
}

// 出队操作
int dequeue(struct Queue* queue) {
    if (isEmpty(queue->stack2)) {
        while (!isEmpty(queue->stack1)) {
            push(queue->stack2, pop(queue->stack1));
        }
    }
    return pop(queue->stack2);
}

// 返回队首元素
int front(struct Queue* queue) {
    if (isEmpty(queue->stack2)) {
        while (!isEmpty(queue->stack1)) {
            push(queue->stack2, pop(queue->stack1));
        }
    }
    return peek(queue->stack2);
}

// 测试队列操作
int main() {
    struct Queue* queue = createQueue(10);
    enqueue(queue, 1);
    enqueue(queue, 2);
    enqueue(queue, 3);
    printf("Front element is %d\n", front(queue));
    printf("Dequeued element is %d\n", dequeue(queue));
    printf("Front element is %d\n", front(queue));
    enqueue(queue, 4);
    printf("Dequeued element is %d\n", dequeue(queue));
    printf("Front element is %d\n", front(queue));
    return 0;
}

