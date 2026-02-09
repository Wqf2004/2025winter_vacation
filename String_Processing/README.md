# 字符串处理

## 问题描述

包含四个字符串处理问题的实现。

### (1) DNA排序

一个字符串的逆序数定义为：该字符串中出现的次序相反的字符对（按照字母表顺序）的数目。DNA字符串中只包含4种字符，即字母A，G，C，T。给定若干个DNA字符串，将这些DNA字符串按照每个字符串的逆序数从小到大排序。

**输入格式：**
- 字符串的个数n
- 每个字符串的长度m
- n个DNA字符串

**输出格式：**
- 按照每个字符串的逆序数从小到大排好序后的n个字符串

**样例：**
```
输入：
6 10
AACATGAAGG
TTTTGGCCAA
TTTGGCCAAA
GATCAGATTT
CCCGGGGGGA
ATCGATGCAT

输出：
CCCGGGGGGA
AACATGAAGG
GATCAGATTT
ATCGATGCAT
TTTTGGCCAA
TTTGGCCAAA
```

---

### (2) 字符串排序

给定n个字符串，在这n个字符串中有相同的字符串，不同的字符串只有num个。将这n个字符串中num个不同的字符串按照字典序排序，并输出每个字符串在这n个字符串中所占的比例，精确到4位小数。

**输入格式：**
- 字符串的个数n
- n个字符串

**输出格式：**
- 每个字符串及其出现比例（精确到4位小数）

---

### (3) 整理单词

输入包含4个部分：
1. 字典，包含至少一个、至多100个单词，每个单词一行
2. 一行内容为XXXXXX，表示字典结束
3. 一个或多个你要整理的"字符串"
4. 一行内容为XXXXXX，表示输入结束

对于输入中每个要整理的"字符串"，输出在字典里存在的单词，该单词与要整理的字符串长度相同，且包含的字母是完全相同的，只是字母的排列可以不同。如果在字典里找到不止一个单词与要整理的字符串相对应时，要把它们按照字典序排序，每个单词占一行。如果在字典里没找到相对应的单词则输出"NOT A VALID WORD"。

**样例：**
```
输入：
tarp
given
score
refund
only
trap
work
earn
course
pepper
part
XXXXXX
resco
nfudre
aptr
sett
oresuc
XXXXXX

输出：
score
******
refund
******
part
tarp
trap
******
NOT A VALID WORD
******
course
******
```

---

### (4) 字符串种类统计

输入n个字符串，每个字符串的长度都相同，均为m，这n个字符串中有相同的。输出n行数据，第1行输出n个字符串中只出现1次的字符串种类数，第2行输出n个字符串中出现2次的字符串种类数，依此类推。

**输入格式：**
- n和m的值
- n个字符串

**输出格式：**
- n行，第i行输出出现i次的字符串种类数

**样例1：**
```
输入：
9 6
AAAAAA
ACACAC
GTTTTG
ACACAC
GTTTTG
ACACAC
ACACAC
TCCCCC
TCCCCC

输出：
1
2
0
1
0
0
0
0
0
```

---

## 项目结构

```
String_Processing/
├── coding/
│   ├── main.c              # C语言实现
│   ├── main.py             # Python实现
│   ├── dataset.txt         # 测试数据集
│   ├── run.sh              # Linux/Mac运行脚本
│   ├── run.bat             # Windows运行脚本
│   ├── compile.sh          # Linux/Mac编译脚本
│   └── compile.bat         # Windows编译脚本
└── README.md               # 本文件
```

---

## 运行方式

### Python版本

```bash
cd coding
python main.py
```

### C语言版本

#### Windows:
```bash
cd coding
compile.bat
# 或手动编译
gcc main.c -o main.exe
main.exe
```

#### Linux/Mac:
```bash
cd coding
bash compile.sh
# 或手动编译
gcc main.c -o main
./main
```

---

## 算法说明

### (1) DNA排序

1. 定义字母顺序：A < C < G < T
2. 对于每个DNA字符串，计算逆序数（即统计满足i<j且dna[i]>dna[j]的字符对数）
3. 按逆序数从小到大排序

### (2) 字符串排序

1. 使用哈希表统计每个字符串的出现次数
2. 按字典序对字符串进行排序
3. 计算每个字符串的出现比例

### (3) 整理单词

1. 构建字典集合
2. 对于每个输入字符串，统计各字母出现次数
3. 在字典中查找长度相同且字母组成相同的单词
4. 按字典序排序匹配结果

### (4) 字符串种类统计

1. 统计每个字符串的出现次数
2. 创建长度为n+1的数组，下标i表示出现次数i的字符串种类数
3. 输出统计结果

---

## 复杂度分析

| 问题 | 时间复杂度 | 空间复杂度 |
|------|-----------|-----------|
| (1) DNA排序 | O(n²·m) | O(n·m) |
| (2) 字符串排序 | O(n·log·n + L·log·L) | O(L) |
| (3) 整理单词 | O(D·L·K) | O(D·L) |
| (4) 字符串种类统计 | O(n·L) | O(n·L) |

注：n为字符串数量，m为字符串长度，D为字典大小，L为字符串平均长度，K为要整理的字符串数量
