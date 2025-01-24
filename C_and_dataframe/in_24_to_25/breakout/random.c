#include<stdio.h>
#include<stdlib.h>
#include<time.h>
/*生成指定范围内的真随机数*/
int randInterval(int min, int max){
    
    return rand() % (max - min + 1) + min;
}
double simulate(){
    srand((unsigned int)time(NULL));
    for(int i = 0; i < 10; i++){
        printf("%d ",randInterval(5,35));
    }
}
int main(){
    simulate();
    return 1;
}
