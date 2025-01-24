#include<stdio.h>
#include<stdlib.h>

//----采用动态分配的顺序存储结构----//
typedef int* Triplet; // 给int的指针变量类型取了一个别名为Triplet
typedef struct{
    Triplet *base; // 那么这里的base就是一个指指针（一个指针数组）
    int row, col, num;
}TSMatrix;
void Init(TSMatrix *M, int r, int c, int t){
    M->row = r;
    M->col = c;
    M->num = t;
    M->base = (Triplet *)malloc(t * sizeof(Triplet));
    for(int i = 0; i < t; i++){
        M->base[i] = (Triplet)malloc(3 * sizeof(int));
        scanf("%d%d%d", &M->base[i][0], &M->base[i][1], &M->base[i][2]);
    }
}
void Destroy(TSMatrix *M){
    for(int i = 0; i < M->num; i++){
        free(M->base[i]);
    }
    free(M->base);
}
void Disp(TSMatrix M){
    int k = 0;
    for(int i = 1; i <= M.row; i++){
        for(int j = 1; j <= M.col; j++){
            if(i == M.base[k][0] && j == M.base[k][1]){
                printf("%4d", M.base[k][2]);
                k++;
            }
            else{
                printf("%4d", 0);
            }
        }
        printf("\n");
    }
}
int main(){
    TSMatrix M;
    Init(&M, 3, 3, 5);
    Disp(M);
    Destroy(&M);
    return 0;
}
