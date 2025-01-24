/* 
THIS FILE IS PART OF WenQiFeng 
bankSimualt.c - The whole part of simulation of bank service

THIS PROGRAM IS FREE SOFTWARE, BALABALA, IS LICENSED UNDER BALABALA
YOU SHOULD HAVE RECEIVED A COPY OF WTFPL LICENSE, IF NOT, BALABALA

Copyright (c) 2024 WenQiFeng 
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define M_PI 3.14159265358979323846
#define MAX_Q 4

#define CLOSE_TIME 450 // 定义银行关门时间:也就是银行一天营业8个半小时左右
/*定义银行客户*/
typedef struct client{
    int num; // 第几号客户
    int arrivalTime;// 客户到达银行的时间
    int duration;  // 办理业务所需时间
    int waitTime;  // 排队时间
}Client;

/*定义链式队列中的结点*/
typedef struct Node {
    Client data;  // 客户数据
    struct Node* next;
} Node;

/*定义队列结构体*/
typedef struct Queue {
    Node* front;
    Node* rear;
    int length;
} Queue;

/*初始化队列*/
void initQueue(Queue* queue) {
    queue->front = NULL;
    queue->rear = NULL;
    queue->length = 0;
}

/*判空*/
int isEmpty(Queue* queue) {
    return queue->front == NULL;
}

/*入队列*/
void enqueue(Queue* queue, Client data) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->data = data;
    newNode->next = NULL;

    if (isEmpty(queue)) {
        queue->front = newNode;
        queue->rear = newNode;
    } 
    else {
        queue->rear->next = newNode;
        queue->rear = newNode;
    }
    queue->length++;
}

/*出队列*/
int dequeue(Queue* queue) {
    if (isEmpty(queue)) {
        printf("Queue is empty\n");
        return 0;
    }

    Node* temp = queue->front;
    Client data = temp->data;
    queue->front = queue->front->next;
    free(temp);

    if (queue->front == NULL) {
        queue->rear = NULL;
    }
    queue->length--;
    return 1;
}

/*在若干队列中找到队列长度最短的一个*/
int findMin(Queue queues[], int numQueues) {
    int shortestIndex = 0;
    int shortestLength = queues[0].length;
    for (int i = 1; i < numQueues; i++) {
        if (queues[i].length < shortestLength) {
            shortestLength = queues[i].length;
            shortestIndex = i;
        }
    }
    return shortestIndex;
}

/*定义事件结点*/
typedef struct evnode{
    int occurTime;       //事件发生时间
    int nType;           //事件类型，-1表示到达事件，0-3表示四个窗口的离开事件
    struct evnode *next; //指针域
}evNode;

/*定义事件表结构体*/
typedef struct eventList{
    evNode* head;
    int length;
}eventList;

/*创建事件表*/
void initEventList(eventList*eventlist){
    eventlist->head = NULL;
    eventlist->length = 0;
}

/*在创建的事件表中插入事件*/
void insertEvent(eventList*eventlist, int occurTime, int nType){
    evNode* newEvent = (evNode*)malloc(sizeof(evNode));
    newEvent->occurTime = occurTime; // 新事件发生的时间
    newEvent->nType = nType; // 新事件的类型
    newEvent->next = NULL;
    if(eventlist->length == 0) {
        eventlist->head = newEvent;
    }
    else if(occurTime < eventlist->head->occurTime){ 
        newEvent->next = eventlist->head;
        eventlist->head = newEvent;
    }
    else{
        evNode* current = eventlist->head;
        while(current->next != NULL && current->next->occurTime < occurTime){
            current = current->next;
        }
        newEvent->next = current->next;
        current->next = newEvent;
    }
    eventlist->length++;
}

/*返回事件表中的第一个结点*/
evNode getFirstEvent(eventList*eventlist){
    return *(eventlist->head);
}

/*删除事件表中的第一个结点*/
int deleteEvent(eventList*eventlist)
{
    if(eventlist->head == NULL){
        return 0;
    }
    evNode* temp = eventlist->head;
    eventlist->head = eventlist->head->next;
    eventlist->length--;
    free(temp);
    return 1;
}

/*遍历事件表*/
void traverseEventList(eventList*eventlist){
    evNode* current = eventlist->head;
    while(current != NULL){
        if(current->nType == -1){
            printf("到达事件：在%d分钟时将有新客户到达\n", current->occurTime);
        }
        else{
            printf("离开事件：在%d分钟时在%d号窗口的客户将要离开\n", current->occurTime, current->nType+1);
        }
        current = current->next;
    }
}

/*生成指定范围内的随机数*/
// 生成标准正态分布的
float gaussrand_NORMAL() {
	float u1 = (float)rand()/RAND_MAX;
    float u2 = (float)rand()/RAND_MAX;
    float X = sqrt(-2 * log(u1)) * cos(2 * M_PI * u2);
	return X;
}

int randInterval(int min, int max){
    int rand_num;
    float interal = (max - min)/2.0;
    int inter = min + interal;
    do{
        int r0 = gaussrand_NORMAL()*log(3*interal);
        rand_num = r0 + inter;
    }while(rand_num < min || rand_num > max);
    return round(rand_num);  
}

/*模拟银行排队*/
double simulate()
{
    srand((unsigned int)time(NULL));// 初始化随机数生成器
    int overTime, totalTime;
    overTime = totalTime = 0;
    int severTime = 0; // 服务总时间
    int clientNum = 0; // 客户人数

    /*创建队列数组并进行初始化*/
    Queue queue[MAX_Q];
    for(int i = 0; i < MAX_Q; i++){
        initQueue(&queue[i]);
    }
    /*创建并初始化事件表*/
    eventList eventlist;
    initEventList(&eventlist);

    insertEvent(&eventlist, 0, -1); // 插入第一个事件

    /*扫描并处理事件列表*/
    int count = 0; //计数器
    int flag = 0; // 标志位
    while((&eventlist)->head != NULL)
    {
        printf("-----第%d次循环-----\n",++count);
        evNode evItem = getFirstEvent(&eventlist); // 获取事件表中的第一个事件
        deleteEvent(&eventlist);          // 删除事件表中的第一个事件
        if(eventlist.length <= 3) flag = 1; // 如果事件表将要空，标志位为true
        
        if(evItem.nType == -1)
        {//到达事件
            clientNum++; // 客户数加1
            /*生成新客户并输入随机数*/
            Client newClient;
            newClient.num = clientNum;
            newClient.arrivalTime = overTime;
            newClient.duration = randInterval(5,35); // 生成业务处理时间
            
            int shortestQueue = findMin(queue,MAX_Q); // 找到人数最少的队列下标
            if(isEmpty(&queue[shortestQueue])){ // 如果当前到达的客户前没有人排队
                //添加离开事件
                insertEvent(&eventlist, overTime + newClient.duration, shortestQueue);
                newClient.waitTime = 0;
            }
            printf("客户%d于银行开始营业的%d分钟来到银行，并进入%d号窗口\n", newClient.num, newClient.arrivalTime, shortestQueue+1);
            printf("客户%d的业务处理时长为%d分钟\n", newClient.num, newClient.duration);
            enqueue(&queue[shortestQueue], newClient); // 新客户进入人数最少的队列
            
            
            /*随机生成下一个用户到达的间隔时间*/
            int interArrivalTime = randInterval(1,10); // 随机生成下一个用户到达的间隔时间
            overTime += interArrivalTime; // 计算下一个用户到达的时间
            if(overTime < CLOSE_TIME){ // 判断其能否在银行关门前进入银行
                insertEvent(&eventlist, overTime, -1); // 可以将这位客户到达的事件插入事件链表
                if(eventlist.length == 5 && flag){  // 每当事件表满时遍历事件表
                    printf("\n");
                    printf("\n");
                    printf("=======事件表满(预言)=======\n");
                    traverseEventList(&eventlist); 
                    flag = 0;  // 标志位为false
                }
            }
            else{
                printf("#########银行关门了#########\n");
                printf("最后一个客户是%d,而随后的不能进入银行的人将在%d分钟后到达\n",clientNum,overTime); // 打印第一个不能进入银行的人到达时间
                continue;
            }
        }
        else{//离开事件
            int win = evItem.nType; // 获得客户所在的窗口号
            Client outClient = queue[win].front->data; // 获取头结点数据
            if(dequeue(&queue[win])){ // 从队列中删除一个客户
                printf("客户%d于银行开始营业的%d分钟离开%d号窗口,逗留时间为%d分钟\n", outClient.num, evItem.occurTime, win+1, outClient.waitTime + outClient.duration); //             
                int waitInLine = 0; // 排队时间
                if(!isEmpty(&queue[win])){  
                    Client* nextClient = &queue[win].front->data; // 获取下一个客户
                    insertEvent(&eventlist, evItem.occurTime + nextClient->duration, win); // 插入下一个客户的离开事件
                    waitInLine = (evItem.occurTime - nextClient->arrivalTime); // 计算下一个人的排队时间
                    nextClient->waitTime = waitInLine; // 更新下一个客户的排队时间
                    queue[win].front->data.arrivalTime = evItem.occurTime; // 更新处理到下一个客户的时间 
                }
                severTime += outClient.duration; // 服务总时间
                totalTime += (waitInLine + outClient.duration); // 总逗留时间
            }
        }
    }
    // 返回平均等待时间
    printf("服务的总时长为%d分钟\n",severTime); // 打印服务总时长
    printf("总的排队时间为%d分钟\n", totalTime - severTime); // 打印总排队时间
    printf("总的逗留时间为%d分钟\n", totalTime); // 打印总逗留时间
    printf("总的客户数为%d\n", clientNum); // 打印总客户数
    return totalTime*1.0 / clientNum; // 返回平均等待时间
}

/*主函数*/
int main()
{
    double avgWaitTime = simulate();
    printf("Average wait time: %.5f mins\n", avgWaitTime); // 打印平均等待时间
    return 0;
}
