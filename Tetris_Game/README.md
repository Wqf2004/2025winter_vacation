# 俄罗斯方块游戏

**⏳ 待开发**

十八、俄罗斯方块游戏

    **1** **、游戏功能需求**

    **（1）**** 游戏界面需求**

良好的用户界面设计。本游戏主要有两个界面，一是用于主游戏区的游戏画布，用来显示游戏时运动和落下去的方块，二是[用于显示下一个方块以及游戏运行时间和得分的]()。

    **（2） 游戏控制需求**

方块下落时，可通过键盘方向键（上、下、左、右键）对该方块进行向上(变形),向下（加速）、向左、向右移动。

    **（3） 图形显示需求**

随机给出不同的形状（长条形、Z字形、反Z形、田字形、7字形、反7形、T字型）下落填充给定的区域，若填满一条便消掉，记分，当达到一定的分数时，过关，一共设置十关，每关方块下落的速度不同，游戏中先结束的一方为本局输家，十关过后，胜出局数多的为赢家。

本游戏通过键盘和鼠标进行操作，在Windows的操作系统下，利用键盘的上、下、左、右键对方块进行移动变形，要使用键盘的接口事件。利用鼠标进行开始、暂停、继续等控制。

下面给出本游戏的设计要点提示。

 **2** **、实现过程**

 **（**  **1** **）功能描述**

俄罗斯方块主要分为四个功能模块

|  |
| - |
|  |

    **（2）功能模块设计**

    **① 游戏执行主流程**

    本俄罗斯方块游戏执行主流程如下图所示。在判断键值时，有左移VK_LEFT、右移VK_RIGHT、下移VK_DOWN、变形旋转VK_UP、退出VK_ESC键值的判断[。]()

|  |
| - |
|  |

    **②游戏方块预览**

新游戏方块将在下图所示的4×4的正方形小方块中预览。使用随机函数rand()来产生1~19之间的游戏方块编号，并作为预览的方块编号。其中的正方形小方块的大小为BSIZE×BSIZE。BSIZE为设定的像素大小。

![](file:///C:/Users/20426/AppData/Local/Temp/msohtmlclip1/01/clip_image008.jpg)

    **③游戏方块控制**

当游戏方块左右移动、下落、旋转时，要清除先前的游戏方块，用新坐标重绘游戏方块。当消除满行时，要重绘游戏底板的当前状态。

清除方块的过程为：用先画轮廓再填充的方式，使用背景色填充小方块，然后使用前景色画一个游戏底板中的小方块。循环此过程，变化当前坐标，填充及画出共16个这样的小方块。这样在游戏底板中，清除了此游戏方块。

    **④数据结构处理**

g_iNumber是其中图形初始情况的编号，下面对各个情况下的变形数据进行分析，应为一共有19种不同形状的俄罗斯方块。

(1)   ▓▓

▓▓

g_aiNextBlock[0][0]=6+10;
g_aiNextBlock[0][1]=0+4;//

g_aiNextBlock[1][0]=7+10;
g_aiNextBlock[1][1]=0+4; //

g_aiNextBlock[2][0]=6+10;
g_aiNextBlock[2][1]=1+4; //

g_aiNextBlock[3][0]=7+10;
g_aiNextBlock[3][1]=1+4;//

    (2)
▓▓▓▓

g_aiMoveBlock[1][0]=aiStockBlock[0][0];

g_aiMoveBlock[1][1]=aiStockBlock[0][1]+1;

g_aiMoveBlock[2][0]=aiStockBlock[0][0];

g_aiMoveBlock[2][1]=aiStockBlock[0][1]+2;

g_aiMoveBlock[3][0]=aiStockBlock[0][0];

g_aiMoveBlock[3][1]=aiStockBlock[0][1]+3;

(3)         ▓

    ▓

▓

    ▓

    g_aiMoveBlock[1][0]=aiStockBlock[0][0]+1;

    g_aiMoveBlock[1][1]=aiStockBlock[0][1];

    g_aiMoveBlock[2][0]=aiStockBlock[0][0]+2;

    g_aiMoveBlock[2][1]=aiStockBlock[0][1];

    g_aiMoveBlock[3][0]=aiStockBlock[0][0]+3;

    g_aiMoveBlock[3][1]=aiStockBlock[0][1];

    (4)
▓

    ▓▓

    ▓

    g_aiMoveBlock[0][0]=aiStockBlock[0][0]+2;

    g_aiMoveBlock[0][1]=aiStockBlock[0][1];

    g_aiMoveBlock[3][0]=aiStockBlock[0][0]+1;

    g_aiMoveBlock[3][1]=aiStockBlock[0][1];

    (5)
        ▓▓

    ▓▓

g_aiMoveBlock[0][0]=aiStockBlock[0][0]-2;

    g_aiMoveBlock[0][1]=aiStockBlock[0][1];

    g_aiMoveBlock[3][0]=aiStockBlock[3][0];

    g_aiMoveBlock[3][1]=aiStockBlock[3][1]+2;

(6)         ▓

    ▓▓

    ▓

g_aiMoveBlock[1][0]=aiStockBlock[0][0]-1;

g_aiMoveBlock[1][1]=aiStockBlock[0][1];

g_aiMoveBlock[3][0]=aiStockBlock[2][0]+1;

g_aiMoveBlock[3][1]=aiStockBlock[2][1];

(7) ▓▓

    ▓▓

g_aiMoveBlock[1][0]=aiStockBlock[3][0]-2;

g_aiMoveBlock[1][1]=aiStockBlock[3][1];

g_aiMoveBlock[3][0]=aiStockBlock[2][0]-1;

g_aiMoveBlock[3][1]=aiStockBlock[2][1]+1;

(8) ▓

    ▓

    ▓▓

g_aiMoveBlock[2][0]=aiStockBlock[0][0]+1;

g_aiMoveBlock[2][1]=aiStockBlock[0][1];

g_aiMoveBlock[3][0]=aiStockBlock[0][0]+2;

g_aiMoveBlock[3][1]=aiStockBlock[0][1];

(9) ▓▓▓

▓

g_aiMoveBlock[1][0]=aiStockBlock[2][0];

g_aiMoveBlock[1][1]=aiStockBlock[2][1]+1;

g_aiMoveBlock[3][0]=aiStockBlock[2][0];

g_aiMoveBlock[3][1]=aiStockBlock[2][1]+2;

(10)  ▓▓

    ▓

    ▓

g_aiMoveBlock[0][0]=aiStockBlock[0][0]+2;

g_aiMoveBlock[0][1]=aiStockBlock[0][1];

g_aiMoveBlock[2][0]=aiStockBlock[1][0]+1;

g_aiMoveBlock[2][1]=aiStockBlock[1][1];

g_aiMoveBlock[3][0]=aiStockBlock[1][0]-1;

g_aiMoveBlock[3][1]=aiStockBlock[1][1];

(11)          ▓

    ▓▓▓

g_aiMoveBlock[0][0]=aiStockBlock[0][0]-2;

g_aiMoveBlock[0][1]=aiStockBlock[0][1];

g_aiMoveBlock[1][0]=aiStockBlock[1][0]-1;

g_aiMoveBlock[1][1]=aiStockBlock[1][1];

g_aiMoveBlock[2][0]=aiStockBlock[3][0];

g_aiMoveBlock[2][1]=aiStockBlock[3][1]+1;

g_aiMoveBlock[3][0]=aiStockBlock[1][0];

g_aiMoveBlock[3][1]=aiStockBlock[1][1]+1;

(12)▓

    ▓

    ▓▓

g_aiMoveBlock[0][0]=aiStockBlock[0][0]-1;

g_aiMoveBlock[0][1]=aiStockBlock[0][1];

g_aiMoveBlock[2][0]=aiStockBlock[1][0]-1;

g_aiMoveBlock[2][1]=aiStockBlock[1][1];

g_aiMoveBlock[3][0]=aiStockBlock[1][0]+1;

g_aiMoveBlock[3][1]=aiStockBlock[1][1];

(13)       ▓

    ▓▓▓

g_aiMoveBlock[1][0]=aiStockBlock[0][0]+1;

g_aiMoveBlock[1][1]=aiStockBlock[0][1];

g_aiMoveBlock[3][0]=aiStockBlock[0][0];

g_aiMoveBlock[3][1]=aiStockBlock[0][1]+2;

(14)        ▓▓

    ▓

    ▓

g_aiMoveBlock[2][0]=aiStockBlock[0][0]+2;

g_aiMoveBlock[2][1]=aiStockBlock[0][1];

g_aiMoveBlock[3][0]=aiStockBlock[2][0]+2;

g_aiMoveBlock[3][1]=aiStockBlock[2][1];

(15)        ▓▓▓

    ▓

g_aiMoveBlock[0][0]=aiStockBlock[0][0]+1;

g_aiMoveBlock[0][1]=aiStockBlock[0][1];

g_aiMoveBlock[1][0]=aiStockBlock[1][0];

g_aiMoveBlock[1][1]=aiStockBlock[1][1]+1;

g_aiMoveBlock[2][0]=aiStockBlock[1][0];

g_aiMoveBlock[2][1]=aiStockBlock[1][1]+2;

g_aiMoveBlock[3][0]=aiStockBlock[0][0];

g_aiMoveBlock[3][1]=aiStockBlock[0][1]+2;

(16)      ▓

    ▓▓▓

g_aiMoveBlock[1][0]=aiStockBlock[0][0];

g_aiMoveBlock[1][1]=aiStockBlock[0][1]+2;

(17)         ▓

    ▓▓

    ▓

g_aiMoveBlock[0][0]=aiStockBlock[2][0]-1;

g_aiMoveBlock[0][1]=aiStockBlock[2][1];

(18)        ▓▓▓

▓

g_aiMoveBlock[0][0]=aiStockBlock[2][0];

g_aiMoveBlock[0][1]=aiStockBlock[2][1]-1;

g_aiMoveBlock[3][0]=aiStockBlock[0][0];

g_aiMoveBlock[3][1]=aiStockBlock[0][1];

(19)         ▓

    ▓▓

    ▓

g_aiMoveBlock[1][0]=aiStockBlock[3][0];

g_aiMoveBlock[1][1]=aiStockBlock[3][1];

g_aiMoveBlock[3][0]=aiStockBlock[2][0]+1;

g_aiMoveBlock[3][1]=aiStockBlock[2][1];

**⑤****函数功能描述**

(1) DrawFixPlace()

函数原型：void DrawFixPlace(HDC hDc)

DrawFixPlace()用于绘制分割线及提示文字。

(2) TextOutTime()

函数原型：void TextOutTime(HDC
hDc,TIMESTRUCT timestruct)

TextOutTime()用于输出输出游戏运行时间。

(3)TextOutScore()

函数原型：void TextOutScore(HDC hDc,int
iScore)

TextOutScore()用于输出游戏得分。

(4) DrawBlock()

函数原型：void DrawBlock(HDC hDc,int
Block[4][2],bool Erasure)

DrawBlock()用于绘制方块。

(5)DrawFixBlock()

函数原型：void  DrawFixBlock(HDC      hDc,int Blocks[MULTIPLEGMPLACE+2][MULTIPLEHEIGHT+1],int
iTop,bool Erasure)

DrawFixBlock()用于绘制堆积的方块。

(6)WinMain()

函数原型：int WINAPI WinMain(HINSTANCE
hInstance,HINSTANCE hPrevInstance,PSTR szCmdLine,int iCmdShow)

WinMain()整个游戏的主控部分。

    **⑥程序预处理**

包括加载头文件，定义结构体、常量和变量，并对它们进行初始化工作。

// winmain.cpp/#define MULTIPLEGMPLACE          13                  // 游戏区倍宽(倍数个单位的宽,只是一个倍数)

// 自定义一些消息宏

#define DM_NEW WM_USER+1               //
自定义消息ID,产生新的"俄罗斯方块"时进行一些处理

// 自定义定时器宏

#define IDT_TIMERONE 1

#define IDT_TIMERTWO 2

// 自定义一个时间结构

typedef struct

{

    int
Hour,Minute,Second;

}TIMESTRUCT;

// 窗口函数声明

LRESULT CALLBACK WndProc(HWND hWnd,UINT message,WPARAM wParam,LPARAM
lParam) // 自定义函数的声明

void DrawFixPlace(HDC hDc);

void TextOutTime(HDC hDc,TIMESTRUCT timestruct);

void TextOutScore(HDC hDc,int iScore);

void DrawBlock(HDC hDc,int Block[4][2],bool Erasure);

void DrawFixBlock(HDC hDc,int
Blocks[MULTIPLEGMPLACE+2][MULTIPLEHEIGHT+1],int iTop,bool Erasure);

#endif

## 项目概述

俄罗斯方块是一款经典的益智游戏，本程序实现完整的游戏逻辑和界面。

## 功能需求

- 方块下落
- 方块旋转
- 消行计分
- 等级系统
- 暂停/继续
- 最高分记录

## 版本规划

- C语言控制台版
- PyQt5桌面版
- Streamlit网页版

## 开发进度

- [ ] 版本一：C语言控制台版
- [ ] 版本二：PyQt5桌面版
- [ ] 版本三：Streamlit网页版

## 目录结构

```
Tetris_Game/
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

1. 方块下落
2. 方块旋转
3. 消行计分
4. 等级系统
5. 暂停/继续
6. 最高分记录

## 完成时间

待定
