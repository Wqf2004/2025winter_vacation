#include <stdio.h>
#include <stdlib.h>
typedef int ElemType;

typedef struct Node {
    ElemType data; // 数据域
    struct Node *next; // 指针域，记得Node前要加struct，表示指针域
} Node;

typedef struct LinkList {
    Node *head; // 头指针
    int length; // 链表长度
} LinkList;

// 初始化链表 
LinkList* InitList() {
    LinkList *L = (LinkList *)malloc(sizeof(LinkList)); // 要记得用malloc给L分配内存
    L->head = NULL; // 头指针为空,链表为空,头节点指向一个空地址
    L->length = 0; // 初始链表长度为0
    // 带头结点的链表的初始化
    /*
    L->head = (Node *)malloc(sizeof(Node));
    L->head->next = NULL;
    L->length = 0;
    */
    return L;
}

/*1）创建一个单链表：从键盘读入几个整数，按输入顺序形成单链表。
将创建好的链表元素依次输出到屏幕上。
*/
void CreateList(LinkList *L) {
    printf("请输入链表的长度：");
    scanf("%d", &L->length);
    printf("请输入链表的元素：");
    for (int i = 0; i < L->length; i++) {
        Node *p = (Node *)malloc(sizeof(Node)); // 开辟一片新的内存空间用来存放新节点
        scanf("%d", &p->data); // 将新节点的数据域赋值为输入的整数
        p->next = NULL; // 对于新构建的节点要注意将其next指针指向NULL
        // 由于这是一个不带头节点的链表，所以要额外判断头节点是否为空
        if (L->head == NULL) {
            L->head = p; // 头节点被修改了，说明这是一个不带头节点的链表
        } 
        else {
            Node *q = L->head;
            while (q->next != NULL) { // 当q->next指向NULL时，跳出while循环
                q = q->next; // 而当q指向NULL时，q不存在next指针了，显然错误
            }
            q->next = p; // 让它指向新创建出来的节点p
        }
        // 带头结点的链表的创建
        /*
        Node *p = (Node *)malloc(sizeof(Node));
        scanf("%d", &p->data);
        Node *q = L->head;
        while (q->next != NULL) {
            q = q->next;
        }
        q->next = p;
        p->next = NULL;
        */
    }
}

// 输出链表
void PrintList(LinkList *L) {
    if(L->head == NULL)
    {
        printf("该表为空！");
        return;
    }
    Node *p = L->head;
    while (p != NULL) {
        printf("%d ", p->data);
        p = p->next; // 当循环是向后移动指针的过程，此时循环结束的标志可以选择当指针指向空停止
    }
    printf("\n");
    // 带头结点的链表的输出
    /*
    Node *p = L->head->next;
    while (p != NULL) {
        printf("%d ", p->data);
        p = p->next;
    }
    printf("\n");
    */
}

/*附加功能1：删除整个单链表。*/
void DeleteList(LinkList *L) {
    Node *p = L->head;
    while (p != NULL) {
        Node *q = p->next;
        free(p);
        p = q;
    }
/*
    while(p != NULL){
        p = p->next;
        free(p);
    } // 这里的p是指针变量，作为左值一经修改，其指向的地址就发生变化，
    //  意味着把后一个地址里的东西全部释放了（修改为没有价值的值），最终是连循环都跑不出的。。。
    // 你的编译器应该是开始识别出来是死循环，所以跑了一会儿，没跑动；后面几次干脆连循环都没进。
*/
    L->head = NULL;
    L->length = 0;
}

/*2）在已创建好的链表中插入一个元素：从键盘读入元素值和插入位置，
调用插入函数完成插入操作。然后将链表元素依次输出到屏幕上。
*/
void InsertList(LinkList *L, int pos, int value) {
    if (pos < 1 || pos > L->length + 1) { // pos是我们视角下的数组位置
        printf("插入位置无效！\n");
        return;
    }
    Node *p = (Node *)malloc(sizeof(Node));
    p->data = value; // 用函数传进来的实参赋值给p->data
    p->next = NULL;

    Node*q = L->head; // 找到对应位置，借助之前一位的节点完成插入。
    for(int i = 1; i < pos - 1; i++)
    {
        q = q->next;
    }
    if(pos == 1)
    {
        p->next = q;
    }
    else
    {
        p->next = q->next;
        q->next = p;
    }
    L->length++;
    // 带头结点的链表的插入
    /*
    Node *p = (Node *)malloc(sizeof(Node));
    scanf("%d", &p->data);
    Node *q = L->head;
    for (int i = 1; i < pos; i++) {
        q = q->next;
    }
    p->next = q->next;
    q->next = p;
    L->length++;
    */
}

/*3）在已创建好的链表中删除一个元素：从键盘读入欲删除的元素位置（序号），
调用删除函数完成删除操作。然后将链表元素依次输出到屏幕上。
*/
void DeleteElement(LinkList *L, int pos) {
    if(pos < 1 || pos > L->length - 1)
    {
        printf("删除不合法！");
        return;
    }
    if(L->length = 0)
    {
        printf("单链表已空！");
        return;
    } 

    Node*q = L->head;// 找到对应位置，借助之前一位的节点完成删除。
    for(int i = 1; i < pos -1; i++)
    {
        q = q->next;
    }
    if(pos == 1)
    {
        Node*p = L->head;
        L->head = L->head->next;
        free(p);
    }
    else{
        Node*p = q->next;
        q->next = p->next;
        free(p);
    }
    L->length--;
    // 带头结点的链表的删除
    /*
    Node *q = L->head;
    for (int i = 1; i < pos; i++) {
        q = q->next;
    }
    Node *p = q->next;
    q->next = p->next;
    free(p);
    L->length--;
    */
}

/*附加功能2：实现单链表中所有元素的翻转，即颠倒元素前后顺序。如：A->B->C->D，翻转后D->C->B->A*/
void reverseList(LinkList *L) {
    // 无头结点的链表翻转
    Node *prev = NULL;
    Node *current = L->head;
    Node *next = NULL;
    while (current != NULL) {
        next = current->next; // 用next保存当前节点的下一个节点，方便current指向下一个节点
        current->next = prev; // 1.将当前节点的next指针指向前一个节点
        prev = current; // 2.将prev指向当前节点，将prev向后移动一个节点
        current = next; // 3.将current指向next，将current向后移动一个节点
        // 1.2.3.执行后，实现了后一个节点指向前一个节点的操作
    }
    // 当current指向NULL时，prev指向最后一个节点，也就是翻转后的第一个节点
    L->head = prev; // 将头节点指向prev
}

/*附加功能3：用冒泡法实现单链表的排序。*/
void bubbleSort(LinkList *L) {
    if (L->head == NULL || L->head->next == NULL) return; // 空链表或只有一个节点，无需排序

    int swapped; // 用于判断是否发生了交换
    Node *ptr1; // 用于遍历链表的指针
    Node *lptr = NULL; // 用于标记链表的最后一个节点

    do {
        swapped = 0;
        ptr1 = L->head;

        while (ptr1->next != lptr) {
            if (ptr1->data > ptr1->next->data) {
                // 交换数据
                int temp = ptr1->data;
                ptr1->data = ptr1->next->data;
                ptr1->next->data = temp;
                swapped = 1;
            }
            ptr1 = ptr1->next;
        }
        lptr = ptr1;
    } while (swapped);
} // 改变链表的结构，只改变链表中元素的顺序

int main() {
    LinkList *L = InitList();
    CreateList(L);
    printf("链表创建完成，链表元素为：");
    PrintList(L);
    printf("\n请输入要插入的元素值和插入位置：");
    int value, pos;
    scanf("%d %d", &value, &pos);
    InsertList(L, pos, value);
    printf("插入元素后，链表元素为：");
    PrintList(L);
    printf("\n请输入要删除的元素位置：");
    scanf("%d", &pos);
    DeleteElement(L, pos);
    printf("删除元素后，链表元素为：");
    PrintList(L);
    reverseList(L);
    printf("\n翻转后，链表元素为：");
    PrintList(L);
    bubbleSort(L);
    printf("\n排序后，链表元素为：");
    PrintList(L);
    DeleteList(L);
    PrintList(L);
    return 0;
}