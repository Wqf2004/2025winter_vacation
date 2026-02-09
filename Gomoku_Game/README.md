# 五子棋游戏

**⏳ 待开发**
二十、五子棋游戏
    1、问题描述
请用所学的C语言知识实现一个命令行下的五子棋游戏。要求有棋盘界面，并实现人与人、人与计算机、计算机与人三种对弈模式。
下面给出本游戏的设计要点提示。
    2、显示棋盘
首先解释如何在命令行下显示一个由字符组合的五子棋棋盘。在学完C语言之后我们知道字符（char）在内存中是以ASCII码的形式保存在一个字符中，数值范围是-128到127，其中也包括像’$’、’%’、’&’等漂亮的符号。同理的，为保存包括中文在内的所有符号，除ASCII码之外还有类似Unicode等其他编码形式，其中就包括了类似’┏’、’ ┓’、’ ┗’、’ ┛’等表格符号，只是它们都需要两个字符的空间来保存！下表给出这些符号对应的Unicode值，你可以尝试写一个简单的C语言程序来验证是否正确。
符号	Unicode值（16进制）	符号	Unicode值（16进制）
┏	0xA9B3	┓	0xA9B7
┗	0xA9BB	┛	0xA9BF
┯	0xA9D3	┷	0xA9DB
┠	0xA9C4	┨	0xA9CC
┼	0xA9E0	○	0xA1F0
●	0xA1F1		
有了上面的编码后就可以将它们显示到屏幕上。用 putchar(); 可以打印字符，比如 putchar(48); （等价于 putchar(‘0’); ）显示一个字符’0’到屏幕上的，执行如下代码：
putchar ( 0xA9 );
putchar ( 0xB3 );
就能在屏幕上打印出一个’┏’，其他字符也可用相同的方法显示。但这样编码会很复杂，可以将将它们保存到一个全局的数组中，打印时直接调用即可！比如在代码中有如下的实现：
const char element[][3] = {
	{0xA9, 0xB3},	// top left
	{0xA9, 0xD3},	// top center
	{0xA9, 0xB7},	// top right
	{0xA9, 0xC4},	// middle left
	{0xA9, 0xE0},	// middle center
	{0xA9, 0xCC},	// middle right
	{0xA9, 0xBB},	// bottom left
	{0xA9, 0xDB},	// bottom center
	{0xA9, 0xBF},	// bottom right

	{0xA1, 0xF1},	// black
	{0xA1, 0xF0} 	// white
};
在定义字符串的时候切忌不要忘记结尾的’\0’也需要占用一个字符的空间，因此element每个元素的长度为3！为了提高调用代码的可读性，还需要定义一些常量：
#define TAB_TOP_LEFT 0x0
#define TAB_TOP_CENTER 0x1
#define TAB_TOP_RIGHT 0x2
#define TAB_MIDDLE_LEFT 0x3
#define TAB_MIDDLE_CENTER 0x4
#define TAB_MIDDLE_RIGHT 0x5
#define TAB_BOTTOM_LEFT 0x6
#define TAB_BOTTOM_CENTER 0x7
#define TAB_BOTTOM_RIGHT 0x8
#define CHESSMAN_BLACK 0x9
#define CHESSMAN_WHITE 0xA
此时，如果要打印左上角的表格符就执行 printf ( elements[TAB_TOP_LEFT] ); 即可。也正因为如此，在程序内部只需用一个整形二维数组来记录棋盘的状态！
现在标准的五子棋棋盘规格是15×15，因此程序中做如下定义。
#define BOARD_SIZE 15
int chessboard[BOARD_SIZE+2][BOARD_SIZE+2];
不要忘记棋盘的边缘部分，所以chessboard的真实大小是17×17！然后在程序刚刚启动的时候对这个数组做初始化（init_chessboard），生成一张空的棋盘。如下所示。
void init_chessboard ( void )
{
	int w, h;
	chessboard[0][0] = TAB_TOP_LEFT;
	chessboard[0][BOARD_SIZE+1] = TAB_TOP_RIGHT;
	chessboard[BOARD_SIZE+1][0] = TAB_BOTTOM_LEFT;
	chessboard[BOARD_SIZE+1][BOARD_SIZE+1] = TAB_BOTTOM_RIGHT;
	代码省略
}
每次显示棋盘是都需要清空屏幕，可以用system函数（stdlib.h）调用系统清屏命令。比如在Windows下清屏命令是“cls”，Linux下是“clear”。为了方便程序调用，可定义一个宏：
#undef CLS
#ifdef WIN32
#  define CLS "cls"
#else
#  define CLS "clear"
#endif
在程序编译时，根据不同的系统自动选择不同的清屏命令。以后的代码中就可以使用system ( CLS ); 来做执行清屏了！
另外一个需要注意的地方：windows下命令提示符默认是黑底白字（传说中的黑框），使得原本的黑子变成了白色，而白子反而成了黑色。因此需要通过 system ( “color F0” ); 将屏幕设置成白底黑字！以下就是显示棋盘的代码：
void show_chessboard ( void )
{
	int w, h;
	system ( CLS );
#ifdef WIN32
	system ( "color F0" );
#endif
	代码省略
}
    3、对弈
根据题目要求，落子操作可以由人（from_user）或计算机(from_computer)完成。因此在程序启动时需要打印菜单提供用户选择模式：
int choice ()
{
	int res = 0;
	puts ( "1) 计-人" );
	puts ( "2) 人-计" );
	puts ( "3) 人-人" );
	puts ( "*) 退出" );
	scanf ( "%d", &res );
	return res;
}
但无论落子的位置是由谁提供，整个操作的过程是一样的：都只需提供当前棋子的颜色，然后函数返回给棋子的坐标。这里牵涉到“坐标”这个数据类型，它是一个由横坐标X和纵坐标Y组成的结构体，结构体定义和落子函数的声明如下：
typedef struct {
	int x, y;
} POINT;
POINT from_user ( int color );
POINT from_computer ( int color );
观察这两个函数的声明，你会发现除了函数名有略微不同，返回值、参数类型都是一样的！而执行人机对弈时需要在这两个函数之间来回切换。为了方便编码，这里用了一个长度为2的函数指针数组来动态决定选择哪个落子函数。
然后就可以通过简单的调用 POINT p = (*get_point[who]) ( color ); 来获得落子的位置，其中who取值为0、1，为当前执棋者，color为当前棋子的颜色。
落完子，接下来就需要判断一下比赛是否已经结束（has_end）。判断时无须大费周章地扫描整个棋盘，只需检查一下最后一颗落子的位置是否构成五子连珠。除去棋盘边缘部分，和棋子相连的都有8个方向，但这8个方向都是两两对称的（比如上方向和下方向），因此真正检查的只有4个方向，定义如下：
const int dir[4][2] = {
	{0, -1},	// 横
	{-1, -1},	// 撇
	{-1, 0},	// 竖
	{-1, 1} 	// 捺
};
从落子的位置出发，检查每个方向相连同色棋子个数是否不小于5个：
int has_end ( POINT p )
{
	int i, j, d;
代码省略
	return false;
}
代码中IN_BOARD和EQUAL为宏定义，功能是判断某个坐标是否在棋盘上以及棋盘上两个位置的棋子颜色是否相同。如果游戏结束函数就返回true。请注意此处的true和false并非真正的布尔型变量，而只是为了提高可读性而定义的枚举：
enum { false = 0, true = !false };
    4、落子
问题描述中提到要求实现人机对弈的功能，只要保证计算机按照五子棋规则下棋，至于输赢并不重要！
扫描整个棋盘，对每个未落子的位置进行分析，获得“将棋子放到该处”的价值，最后把棋子摆放在价值最高的位置！代码如下：
POINT from_computer ( int color )
{
	POINT p = {0, 0}, m = p;
	int max = 0, v;
代码省略
	return m;
}

根据五子棋的规则：你在棋盘某处放了一颗棋子，如果它能和周围其他棋子连成二子连珠、三子连珠，就称它为“活二”、“活三”；如果能阻挡对方的棋子形成二子连珠、三子连珠，就称它为“冲二”、“冲三”。依次类推！那么就可以给“活二”、“冲三”等设定一个价值，将这些所有的值累加起来就是在该位置落子的价值了！
除了这些，还可以添加位置的价值，比如越靠近中心的位置价值越高，而边缘部分则价值相对较低。方法很多，任由你发挥聪明才智来改进！以下是参考代码：
int calc_value ( POINT p )
{
	static const int values[] = {
		0, 100, 600, 6000, 40000
	};
	static const int center = BOARD_SIZE / 2 + BOARD_SIZE % 2;
	int i, j, d;
	int sum = 0;
代码省略
	return sum + (center-abs(center-p.x)) * (center-abs(center-p.y));
}
2）from_user的方法就很简单了！只有让用户从键盘输入坐标即可，只是要确保输入的位置是可用的！参考代码如下：
POINT from_user ( int color )
{
	POINT p = {0, 0};
	int failure = false;
代码省略
	return p;
}
    5、运行效果
根据上述思路实现的五子棋游戏，运行界面应如下所示。这里演示的是人机对弈（计算机先落子）。
 

## 项目概述

五子棋是一款经典的策略游戏，本程序实现完整的双人对战功能。

## 功能需求

- 棋盘绘制
- 落子判断
- 胜负判定
- 悔棋功能
- 重新开始
- 对局记录

## 版本规划

- C语言控制台版
- PyQt5桌面版
- Streamlit网页版

## 开发进度

- [x] 版本一：C语言控制台版
- [x] 版本二：PyQt5桌面版
- [x] 版本三：Streamlit网页版

## 目录结构

```
Gomoku_Game/
├── c_console/           # C语言控制台版
│   ├── main.c
│   ├── compile.bat
│   ├── compile.sh
│   └── README.md
├── pyqt5_gui/          # PyQt5桌面版
│   ├── main.py
│   ├── data_manager.py
│   ├── requirements.txt
│   ├── README.md
│   ├── run.bat
│   └── ui/
│       ├── __init__.py
│       ├── login_dialog.py
│       ├── main_window.py
│       └── [功能页面]
├── streamlit_app/       # Streamlit网页版
│   ├── app.py
│   ├── data_manager.py
│   ├── requirements.txt
│   ├── README.md
│   └── run.bat
└── dataset/
    ├── [数据文件1]
    ├── [数据文件2]
    └── password.txt    # 密码文件
```

## 开发说明

参考 SMMS（项目一）的开发流程和文件结构，实现以下功能：

1. 棋盘绘制
2. 落子判断
3. 胜负判定
4. 悔棋功能
5. 重新开始
6. 对局记录

## 完成时间

2025年2月
