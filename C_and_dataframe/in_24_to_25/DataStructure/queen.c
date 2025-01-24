#include <stdio.h>

int main(){
	int queen[8] = {0};		//用来储存皇后的位置 即queen的值就为第i行的列
							//queen[0]表示第0行
							//queen[i]表示第i行
	int cnt = 0;			//表示摆放了几个皇后，也表示摆放皇后的行数。
	int col = 0;			//表示在这一列上摆放了皇后
	int sum = 0;			//总共有几种摆法
	while(1){
		//在(cnt,col)这个坐标摆放皇后

		if(cnt == 1 && queen[0] == 7 && col == 6){		//表示第一行的皇后已经到了第八列且第二行的皇后到了第六列位置，已经摆放不下皇后了就退出循环
			break;	
		}
		int isAttack = 0;		//用来表示皇后们之间是否能够攻击的到，如果攻击的到就是1，否则就为0
		int i=0;
		for(i=0;i<cnt;i++){
			if(queen[i] == col){	//表示在同一列上
				isAttack = 1;	
			}	
			int div_row = cnt -i;		//表示斜线上的纵坐标之差
			int div_col = queen[i]-col;		//表示斜线上横坐标之差
			if(div_row == div_col ||div_row == -div_col){ 	//表示在同一斜线上
				isAttack = 1;	
			}
		}
		if(isAttack == 0){	//表示可以放置
			queen[cnt] = col;		//记录皇后当前的列数
			cnt++;					//开始摆放下一个皇后
			col = 0;				//下一个皇后从第一列开始遍历
			if(cnt == 8){			//如果摆满了八个皇后就打印出他们的摆法
				for(i=0;i<8;i++){
					printf("%d  ",queen[i]+1);	
				}	
				printf("\n");	
				sum++;				//并且摆放种数+1
				do{		//越界问题	//回朔
					cnt--;		//撤回正在摆放的皇后
					col = queen[cnt]+1;		//往下一个列寻找摆放位置
				}while(col>=8);			
			}
		}else{			//表示不能摆放
			col++;
			while(col>=8){			//回朔
				cnt--;				//退一格
				col = queen[cnt]+1;	//上一个皇后往后移一格
			}
		}
	}
	printf("总共有%d种摆法\n",sum);
	return 0;	
}
