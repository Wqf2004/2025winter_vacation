/* 数据结构（C语言）课后习题：
5、如何实现循环队列（顺序）中的每个存储空间都能得到利用，试编写入队和出队算法。

算法思想：
1. 初始化一个循环队列，使用一个数组来存储队列元素，并设置队列的头部和尾部指针。
2. 入队操作：
   - 检查队列是否已满，如果已满则无法入队。
   - 将元素添加到队列尾部，并更新尾部指针。
   - 如果尾部指针到达数组末尾，则将其重置为0，以实现循环。
3. 出队操作：   
   - 检查队列是否为空，如果为空则无法出队。
   - 将队列头部元素出队，并更新头部指针。
   - 如果头部指针到达数组末尾，则将其重置为0，以实现循环。
4. 检查队列是否为空：
   - 如果头部指针和尾部指针相同，则队列为空。
5. 检查队列是否已满：
   - 如果头部指针和尾部指针相邻，则队列已满。
*/

#include <stdio.h>
#include <stdlib.h>

#define N 20 
// 顺序循环队列类型定义
typedef struct
{     
    int data[N];
    int front, rear;
    int isEmpty;        // 标志位，表示队列是否为空
}Queue;

// 初始化循环队列
void initializeQueue(Queue *queue) {
    queue->front = 0;
    queue->rear = 0;
    queue->isEmpty = 1;  // 初始时队列为空
}

// 循环队列判满
int isFull(Queue *queue) {
    return (!queue->isEmpty) && (queue->front == queue->rear);
}

// 循环队列判空
int isEmpty(Queue *queue) {
    return queue->isEmpty;
}

// 打印循环队列的元素
void printQueue(Queue *queue) {
    if (isEmpty(queue)) {
        printf("Queue is empty.\n");
        return;
    }
    printf("Queue elements: ");
    int i = queue->front;   
    while (i != queue->rear) {
        printf("%d ", queue->data[i]);
        i = (i + 1) % N;
    }
    printf("\n");
}

// 出队函数
int Dequeue(Queue *q)
{
    if(isEmpty(q))
    {
        return 0;
    }
    int value = q->data[q->front];
    q->front = (q->front + 1) % N;
    if (q->front == q->rear) { // 如果队头和队尾指针相遇，则队列为空
        q->isEmpty = 1;
    }
    return value;
}

// 循环队列入队函数
void Enqueue(Queue *q, int value)
{
    if(isFull(q))
    {
        return;
    }
    q->data[q->rear] = value;
    q->rear = (q->rear + 1) % N;
    q->isEmpty = 0;
}

// 删除循环队列当中的负数，保留非负数，并且保持顺序不变
void DelMinus(Queue *q)
{
    int value;
    Queue tempQueue; // 临时队列
    initializeQueue(&tempQueue); // 初始化临时队列

    // 处理队列中的所有元素
    while(!isEmpty(q)) {
        value = Dequeue(q); // 出队一个元素
        if(value >= 0) { // 只处理非负数
            Enqueue(&tempQueue, value); // 将非负数入队到临时队列
        }
    }

    // 将临时队列中的元素重新放回原队列
    while(!isEmpty(&tempQueue)) {
        Enqueue(q, Dequeue(&tempQueue)); // 从临时队列出队并入队到原队列
    }
}

// 主函数
int main()
{
    Queue q;
    int i, a[] = {1, 0, -2, 3, -4, 5, -6, 7, -8, 9, -10}; // 数组a中有正数有负数也可以为0
    initializeQueue(&q);
    for(i = 0; i < 10; i++){
        Enqueue(&q, a[i]);
    }  
    printf("Before DelMinus:\n");
    printQueue(&q);
    DelMinus(&q);
    printf("After DelMinus:\n");
    printQueue(&q);
    return 0;
}