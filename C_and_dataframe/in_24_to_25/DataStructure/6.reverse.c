/* 数据结构（C语言）课后习题：
2、实现单链表逆转操作，示例：1 2 3 4 5 6 7 8 9 10, 逆转后： 10 9 8 7 6 5 4 3 2 1
（请先写出算法思想和实现步骤，再写代码）

算法思想：
1. 初始化三个指针：prev、current和next。
2. 将current指向链表的头节点。
3. 在while循环中，将next指向current的下一个节点。
4. 将current的next指针指向prev。
5. 将prev指向current。
6. 将current指向next。
7. 循环直到current为NULL。
*/

#include <stdio.h>
#include <stdlib.h>

// 定义链表节点结构
struct Node {
    int data;
    struct Node* next;
};

// 创建新节点
struct Node* createNode(int data) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

// 打印链表
void printList(struct Node* head) {
    struct Node* current = head;
    while (current != NULL) {
        printf("%d -> ", current->data);
        current = current->next;
    }
    printf("NULL\n");
}

// 逆转链表
struct Node* reverseList(struct Node* head) {
    struct Node* prev = NULL;
    struct Node* current = head;
    struct Node* next = NULL;
    while (current != NULL) {
        next = current->next;
        current->next = prev;
        prev = current;
        current = next;
    }
    return prev;
}

int main() {
    // 创建链表 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> 10
    struct Node* head = NULL;
    for (int i = 1; i <= 10; i++) {
        struct Node* newNode = createNode(i);
        newNode->next = head;
        head = newNode;
    }

    printf("原始链表: ");
    printList(head);    
    head = reverseList(head);
    printf("逆转后的链表: ");
    printList(head);

    return 0;
}           



