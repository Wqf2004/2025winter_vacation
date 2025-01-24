#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// BF算法：即暴力匹配算法的实现
void StrReplace1(char *T, char *P, char *S) 
{
    int pos = -1; // 初始化位置为-1，表示未找到匹配
    int lenT = strlen(T);
    int lenP = strlen(P);
    int lenS = strlen(S);

    for (int i = 0; i <= lenT - lenP; i++) {
        int j = 0;
        while (j < lenP && T[i + j] == P[j]) {
            j++;
        }
        if (j == lenP) {
            pos = i; // 找到匹配的位置
            break;
        }
    }

    // 如果未找到匹配，直接返回
    if (pos == -1) {
        return;
    }

    // 从T中删除子串P
    for (int i = pos + lenP; i <= lenT; i++) {
        T[i - lenP] = T[i];
    }
    lenT -= lenP; // 更新T的长度

    // 将子串S从pos处开始插入到T中
    // 需要确保T有足够的空间来容纳S
    for (int i = lenT; i >= pos; i--) {
        T[i + lenS] = T[i];
    }
    for (int i = 0; i < lenS; i++) {
        T[pos + i] = S[i];
    }
    T[pos + lenS] = '\0'; // 更新T的结尾

    // 打印替换后的字符串
    printf("After replacement: %s\n", T);
}
// 时间复杂度分析：
// BF算法的时间复杂度为O((lenT - lenP + 1) * lenP)，在最坏情况下为O(lenT * lenP)。
// 删除和插入操作的时间复杂度为O(lenT)，因为在最坏情况下需要移动所有字符。
// 总的时间复杂度为O(lenT * lenP + lenT)，简化后为O(lenT * (lenP + 1))。

// KMP算法：基于next数组的实现方式
void StrReplace2(char *T, char *P, char *S) 
{
    int pos = -1; // 初始化位置为-1，表示未找到匹配
    int lenT = strlen(T);
    int lenP = strlen(P);
    int lenS = strlen(S);
    int *next = (int *)malloc(lenP * sizeof(int));

    // 计算next数组
    next[0] = -1;
    int j = 0, k = -1;
    while (j < lenP - 1) {
        if (k == -1 || P[j] == P[k]) {
            j++;
            k++;
            next[j] = k;
        } else {
            k = next[k];
        }
    }

    j = 0; // T的索引
    k = 0; // P的索引
    while (j < lenT) {
        if (k == -1 || T[j] == P[k]) {
            j++;
            k++;
        }
        if (k == lenP) {
            pos = j - k; // 找到匹配的位置
            break;
        } else if (j < lenT && T[j]!= P[k]) {
            k = next[k];
        }
    }

    // 如果未找到匹配，直接返回
    if (pos == -1) {
        free(next);
        return;
    }

    // 从T中删除子串P
    for (int i = pos + lenP; i < lenT; i++) {
        T[i - lenP] = T[i];
    }
    lenT -= lenP; // 更新T的长度

    // 将子串S从pos处开始插入到T中
    for (int i = lenT; i >= pos; i--) {
        T[i + lenS] = T[i];
    }
    for (int i = 0; i < lenS; i++) {
        T[pos + i] = S[i];
    }
    // 更新T的长度，重新计算为当前实际长度
    lenT = strlen(T);
    T[lenT] = '\0'; // 更新T的结尾

    // 打印替换后的字符串
    printf("After replacement: %s\n", T);
}

// 时间复杂度分析：O(lenT + lenP)
int main() {
    char originalT1[] = "Hello, World!"; // 保存原始字符串
    char P[] = "World";
    char S[] = "Universe";
    StrReplace1(originalT1, P, S); // 使用原始字符串进行第一次替换
    char originalT2[] = "Hello, World!"; // 再次保存原始字符串
    StrReplace2(originalT2, P, S); // 使用原始字符串进行第二次替换
    return 0;
}