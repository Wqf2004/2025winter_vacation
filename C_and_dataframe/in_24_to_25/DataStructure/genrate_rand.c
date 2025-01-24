#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#define M_PI 3.14159265358979323846

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

int main()
{
    int rand_num;
    int count;
    srand((unsigned)time(NULL));
    for(int i=0; i<100; i++)
    {
        rand_num = randInterval(5, 35);
        printf("%d ", rand_num);
        if(rand_num>15&&rand_num<25) 
        {
            count++;
        }
    }
    printf("\n");
    printf("%d\n", count);
    return 0;
}