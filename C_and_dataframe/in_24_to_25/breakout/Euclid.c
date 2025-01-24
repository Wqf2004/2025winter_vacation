//c语言常用包
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <stdbool.h>

//应用Euclid算法计算两个整数的最大公约数
int gcd(int a, int b) {
    if (b == 0) {
        return a;
    } else {
        return gcd(b, a % b);
    }
}

//计算两个整数的最小公倍数
int lcm(int a, int b) {
    return (a * b) / gcd(a, b);
}

int main() {
    int a, b;
    printf("请输入两个整数：");
    scanf("%d %d", &a, &b);
    printf("最大公约数为：%d\n", gcd(a, b));
    printf("最小公倍数为：%d\n", lcm(a, b));
    return 0;
}