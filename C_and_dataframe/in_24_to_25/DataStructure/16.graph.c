#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#define INF 999999 // 定义一个达不到的伪无穷大
#define MAX_VERTICES 100 // vertices顶点
// 此处也可使用limits.h包中的INT_MAX，即真无穷
typedef struct {
    int edges[MAX_VERTICES][MAX_VERTICES]; // 用两个顶点序号来定义一条边
    int numVertices; // 顶点的数目
} GraphMatrix;  // 图矩阵，即邻接矩阵

typedef struct Node {
    int vertex; // vertex是顶点的单数形式
    int weight; // 边的权重
    struct Node* next; // 当前顶点的下一个顶点的指针
} Node;  // 定义节点指针

typedef struct {
    Node* adjLists[MAX_VERTICES];  // 用节点类型创建的邻接表
    int numVertices; // 表的大小，表里面存的是下一个节点，即存储的是顶点的数目
} GraphList;

// 创建邻接矩阵图
void createGraphMatrix(GraphMatrix* g, int vertices) {
    // 用顶点个数和边的二维数组创建起一个邻接矩阵图
    g->numVertices = vertices;
    for (int i = 0; i < vertices; i++) {
        for (int j = 0; j < vertices; j++) {
            if (i == j) {
                g->edges[i][j] = 0; // 对角线上的值为0，表示相同的顶点不发生转移
            }
            else {
                g->edges[i][j] = INF; // 初始化为无穷大
            } //从而建立了vertices数量的顶点而没有任何边的连接
        }
    }
}

// 创建邻接表图
void createGraphList(GraphList* g, int vertices) {
    g->numVertices = vertices;
    for (int i = 0; i < vertices; i++) {
        g->adjLists[i] = NULL; // 初始化为空，也就是这个邻接表的每个顶点都没有相连的顶点
    }
}

// 深度优先遍历
void DFS(GraphMatrix* g, int start, int visited[])
{// start为进行深度优先遍历的源点
    visited[start] = 1;  // 将visited数组中start位置处置为1，表示被访问，visited的初始化在main函数中进行
    printf("%d ", start);

    for(int i = 0; i < g->numVertices; i++)
    {
        if(g->edges[start][i] >= 1 && g->edges[start][i] != INF && !visited[i])
        { // 马上用递归将起始点下移到后一个顶点
            DFS(g, i, visited);// 用递归的方式做
        }
    }
}

// 邻接表创建图的深度优先遍历
void DFSList(GraphList* g, int vertex, int visited[]) {
    visited[vertex] = 1;
    printf("%d ", vertex);
    Node* temp = g->adjLists[vertex];
    while (temp) {
        if (!visited[temp->vertex]) {
            DFSList(g, temp->vertex, visited);
        }
        temp = temp->next;
    }
}

// 广度优先遍历
void BFS(GraphMatrix* g, int startVertex) {
    int visited[MAX_VERTICES] = {0};// 开始为0，对已访问的顶点记为1
    int queue[MAX_VERTICES], front = 0, rear = 0;// 创建一个队列，每次都将当前相邻的顶点入队

    visited[startVertex] = 1;
    queue[rear++] = startVertex; // 入队

    while (front < rear) {
        int currentVertex = queue[front++]; // 更新当前顶点，就是用队列中出队的元素
        printf("%d ", currentVertex);

        for (int i = 0; i < g->numVertices; i++) {
            if (g->edges[currentVertex][i] >= 1 && g->edges[currentVertex][i] != INF && !visited[i]) {
                visited[i] = 1;
                queue[rear++] = i;
            }
        }
    }
}
// Dijkstra算法
void Dijkstra(GraphMatrix* g, int startVertex) {
    int distance[MAX_VERTICES]; // 路径长度，记录最短路径下的到源点的距离
    int visited[MAX_VERTICES] = {0}; // 初始化访问数组，被访问过就相当于是被操作了的顶点，一旦被操作处理过就放入S集合中
    int path[MAX_VERTICES]; // 路径数组，记录最短路径下的直接前驱

    // 初始化距离和路径
    for (int i = 0; i < g->numVertices; i++) {
        distance[i] = INT_MAX; // 设置为无穷大
        path[i] = -1; // 设置前驱为-1
    }
    distance[startVertex] = 0; // 将源点放入S集合中

    for (int count = 0; count < g->numVertices - 1; count++) 
    {   // 找到未访问的最小距离顶点
        int minIndex = -1;
        for (int v = 0; v < g->numVertices; v++) {
            if (!visited[v] && (minIndex == -1 || distance[v] < distance[minIndex])) {
                minIndex = v;
            }
        }
        visited[minIndex] = 1; //此处第一次访问的顶点为源点，并将其加入到S集合当中

        // 更新相邻顶点的距离
        for (int v = 0; v < g->numVertices; v++) {
            if (g->edges[minIndex][v] >= 1 && !visited[v] && distance[minIndex] != INT_MAX) {
                if (distance[minIndex] + g->edges[minIndex][v] < distance[v]) {
                    distance[v] = distance[minIndex] + g->edges[minIndex][v]; // 更新距离数组为可利用当前顶点缩短到达距离后的值
                    path[v] = minIndex; // 并在路径数组中更新当前顶点的直接前驱，为当前访问的顶点
                }
            }
        }
    }

    // 输出结果
    printf("顶点 %d 到其他顶点的最短路径:\n", startVertex);
    for (int i = 0; i < g->numVertices; i++) {
        printf("到顶点 %d 的距离: %d\n", i, distance[i]);
        // 输出路径
        if (distance[i] != INT_MAX) {
            printf("路径: %d", i);
            int j = path[i];
            while (j != -1) {
                printf(" <- %d", j);
                j = path[j];
            } // 这里是一个回溯的过程，如果想要从源点开始，那么就需要用另外的数组进行逐个统计记录
            printf("\n");
        }
    }
}

// Floyd算法
void Floyd(GraphMatrix* g) {
    int dist[MAX_VERTICES][MAX_VERTICES];
    int predecessor[MAX_VERTICES][MAX_VERTICES]; 

    // 初始化距离矩阵和前驱矩阵
    for (int i = 0; i < g->numVertices; i++) {
        for (int j = 0; j < g->numVertices; j++) {
            if (g->edges[i][j] > 0) {
                dist[i][j] = g->edges[i][j]; // 距离为边的权值
                predecessor[i][j] = i; 
            } else if (i == j) {
                dist[i][j] = 0; // 自己到自己的距离为0
                predecessor[i][j] = -1; 
            } else {
                dist[i][j] = INT_MAX; // 无边
                predecessor[i][j] = -1; 
            }
        }
    }
    for (int k = 0; k < g->numVertices; k++) {
        for (int i = 0; i < g->numVertices; i++) {
            for (int j = 0; j < g->numVertices; j++) {
                if (dist[i][k] != INT_MAX && dist[k][j] != INT_MAX && dist[i][j] > dist[i][k] + dist[k][j]) {
                    dist[i][j] = dist[i][k] + dist[k][j];
                    predecessor[i][j] = predecessor[k][j]; 
                }
            }
        }
    }

    // 输出结果
    printf("任意两点间的最短路径:\n");
    for (int i = 0; i < g->numVertices; i++) {
        for (int j = 0; j < g->numVertices; j++) {
            if (dist[i][j] == INT_MAX) {
                printf("从顶点 %d 到顶点 %d 的距离: 无法到达\n", i, j);
            } else {
                printf("从顶点 %d 到顶点 %d 的距离: %d\n", i, j, dist[i][j]);
                // 输出路径
                printf("路径: %d", j);
                int pred = predecessor[i][j];
                while (pred != -1) {
                    printf(" <- %d", pred);
                    pred = predecessor[i][pred];
                }
                printf("\n");
            }
        }
    }
}

// 调用测试函数的主函数main
int main() {
    GraphMatrix g;
    createGraphMatrix(&g, 5); // 假设图有5个顶点

    // 添加有向边
    g.edges[0][1] = 1;
    g.edges[1][0] = 2;
    g.edges[3][1] = 3;
    g.edges[4][3] = 4;
    g.edges[0][2] = 1;
    g.edges[1][3] = 1;
    g.edges[2][3] = 1;
    g.edges[3][4] = 1;

    // 深度优先遍历
    int visited[MAX_VERTICES] = {0};
    printf("深度优先遍历结果: ");
    DFS(&g, 0, visited);
    printf("\n");

    // 广度优先遍历
    printf("广度优先遍历结果: ");
    BFS(&g, 0);
    printf("\n");

    // Dijkstra算法
    Dijkstra(&g, 0);

    // Floyd算法
    Floyd(&g);
    printf("\n以上采用的是邻接矩阵的方式\n\n");


    // 用邻接表的方式创建一个图
    GraphList gList;
    createGraphList(&gList, 5); // 假设图有5个顶点
    Node* newNode;
    int edges[][3] = { {0, 1, 2}, {0, 2, 3}, {1, 3, 1}, {2, 3, 4}, {3, 4, 5} }; // 定义边的数组，包含权重
    int numEdges = sizeof(edges) / sizeof(edges[0]); // 计算边的数量

    for (int i = 0; i < numEdges; i++) {
        int src = edges[i][0];
        int dest = edges[i][1];
        int weight = edges[i][2]; // 获取权重

        newNode = (Node*)malloc(sizeof(Node));
        newNode->vertex = dest;
        newNode->weight = weight; // 设置权重
        newNode->next = gList.adjLists[src];
        gList.adjLists[src] = newNode;
    }
    // 深度优先遍历
    int visitedList[MAX_VERTICES] = {0}; // 初始化访问数组
    printf("邻接表的深度优先遍历结果: ");
    DFSList(&gList, 0, visitedList); // 从顶点0开始遍历
    printf("\n\n以上是邻接表的方式");
    // 释放内存
    for (int i = 0; i < gList.numVertices; i++) {
        Node* temp = gList.adjLists[i];
        while (temp) {
            Node* toFree = temp;
            temp = temp->next;
            free(toFree);
        }
    }
    return 0;
}
