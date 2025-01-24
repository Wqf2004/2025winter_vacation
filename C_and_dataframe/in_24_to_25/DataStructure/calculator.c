#pragma warning(disable:4996)
#define _INTEGRAL_MAX_BITS 64
/*---------------------------------------
函数型计算器(VC++2010,Win32 Console)
功能：
目前提供了10多个常用数学函数:
⑴正弦sin
⑵余弦cos
⑶正切tan
⑷开平方sqrt
⑸反正弦arcsin
⑹反余弦arccos
⑺反正切arctan
⑻常用对数lg
⑼自然对数ln
⑽ｅ指数exp
⑾乘幂函数^
⑿向上取整ceil
⒀向下取整floor
⒁四舍五入取整Round
⒂取符号sign
⒃取绝对值abs
⒄度转弧度d2r
⒅弧度转度r2d
用法：
如果要求2的32次幂，可以打入2^32<回车>
如果要求30度角的正切可键入tan(d2r(30))<回车>
注意不能打入：tan(30)<Enter>
如果要求1.23弧度的正弦，有几种方法都有效：
sin(1.23)<Enter>
sin 1.23 <Enter>
sin1.23  <Enter>
如果验证正余弦的平方和公式,可打入sin(1.23)^2+cos(1.23)^2 <Enter>或sin1.23^2+cos1.23^2 <Enter>
此外两函数表达式连在一起,自动理解为相乘如：sin1.23cos0.77+cos1.23sin0.77就等价于sin(1.23)*cos(0.77)+cos(1.23)*sin(0.77)
当然你还可以依据三角变换，再用sin(1.23+0.77)也即sin2验证一下。
本计算器充分考虑了运算符的优先级因此诸如：2+3*4^2 实际上相当于：2+(3*(4*4))
另外函数名前面如果是数字,那么自动认为二者相乘.
同理，如果某数的右侧是左括号，则自动认为该数与括弧项之间隐含一乘号。
如：3sin1.2^2+5cos2.1^2 相当于3*sin2(1.2)+5*cos2(2.1)
又如：4(3-2(sqrt5-1)+ln2)+lg5 相当于4*(3-2*(√5 -1)+loge(2))+log10(5)
此外，本计算器提供了圆周率Pi键入字母时不区分大小写,以方便使用。
16进制整数以0x或0X开头，2进制整数以0b或0B开头，8进制整数以0o或0O开头，且可以包含下划线间隔。
----------------------------------------*/
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <locale.h>
//#include <windows.h>
const char Tab = 0x9;
const int  DIGIT = 1;
#define MAXLEN 65536
#define STACKSIZE 50
char s[MAXLEN],t[MAXLEN], *endss;
char gap[MAXLEN];
int pcs = 15;
int fmt;//0-正常|1-半角逗号每3位间隔整数部分|2-下划线每4位间隔整数部分
FILE *fp;
double sign(double dVal) {
         if (dVal>0.0) return  1.0;
    else if (dVal<0.0) return -1.0;
    else               return  0.0;
}
double Round(double dVal, short iPlaces) {//iPlaces>=0
    char tmp[30];
    double dRetval;
 
    sprintf(tmp, "%.*lf", iPlaces, dVal);
    sscanf(tmp, "%lf", &dRetval);
    return (dRetval);
}
double fun(double x, char op[STACKSIZE], char ops[STACKSIZE][5], int *iop) {
    char lar,lr;
    int ss,ee,nn,sh;
    char c;
    int i,j;
    __int64 result;
    char *e;
    char b[64+1];
 
 
    while (op[*iop - 1]<32) //本行使得函数嵌套调用时不必加括号,如 arcsin(sin(1.234)) 只需键入arcsin sin 1.234<Enter>
        switch (op[*iop - 1]) {
        case  7: x = sin(x);    (*iop)--; break;
        case  8: x = cos(x);    (*iop)--; break;
        case  9: x = tan(x);    (*iop)--; break;
        case 10: x = sqrt(x);   (*iop)--; break;
        case 11: x = asin(x);   (*iop)--; break;
        case 12: x = acos(x);   (*iop)--; break;
        case 13: x = atan(x);   (*iop)--; break;
        case 14: x = log10(x);  (*iop)--; break;
        case 15: x = log(x);    (*iop)--; break;
        case 16: x = exp(x);    (*iop)--; break;
        case 17: x = ceil(x);   (*iop)--; break;
        case 18: x = floor(x);  (*iop)--; break;
        case 19: x = Round(x,0);(*iop)--; break;
        case 20: x = sign(x);   (*iop)--; break;
        case 21: x = fabs(x);   (*iop)--; break;
        case 22: x = x*3.14159265358979323846264338328/180.0;   (*iop)--; break;
        case 23: x = x/3.14159265358979323846264338328*180.0;   (*iop)--; break;
        case 24://shift{l|a|r}{l|r}{ss}{ee|lnn}{sh}
            lar=ops[*iop - 1][0];// {l|a|r} Logic|Arithmetic|Rotate
            lr =ops[*iop - 1][1];// {l|r}   Left|Right
            ss =ops[*iop - 1][2];// {ss}    start_bit
            nn =ops[*iop - 1][3];// {nn}    n_bits
            sh =ops[*iop - 1][4];// {sh}    shift_bits
            ee =ss+nn-1;
            result=(__int64)x;
            _i64toa(result,b,2);
            sprintf(t,"%064s",b);
            switch (lar) {
            case 'l':
                switch (lr) {
                case 'l'://Logic Left Shift ss Lnn sh
                    //d63..ee   ==ss   ..d00
                    //t00..63-ee==63-ss..t63
                    for (j=0;j<sh;j++) {
                        for (i=0;i<nn-1;i++) t[63-ee+i]=t[63-ee+1+i];
                        t[63-ss]='0';
                    }
                break;
                case 'r'://Logic Right Shift ss Lnn sh
                    //d63..ee   ==ss   ..d00
                    //t00..63-ee==63-ss..t63
                    for (j=0;j<sh;j++) {
                        for (i=0;i<nn-1;i++) t[63-ss-i]=t[63-ss-1-i];
                        t[63-ee]='0';
                    }
                break;
                }
            break;
            case 'a':
                switch (lr) {
                case 'l'://Arithmetic Left Shift ss Lnn sh
                    //d63..ee   ==ss   ..d00
                    //t00..63-ee==63-ss..t63
                    for (j=0;j<sh;j++) {
                        for (i=0;i<nn-1;i++) t[63-ee+i]=t[63-ee+1+i];
                        t[63-ss]='0';
                    }
                break;
                case 'r'://Arithmetic Right Shift ss Lnn sh
                    //d63..ee   ==ss   ..d00
                    //t00..63-ee==63-ss..t63
                    for (j=0;j<sh;j++) {
                        for (i=0;i<nn-1;i++) t[63-ss-i]=t[63-ss-1-i];
                        t[63-ee]=t[63-ee+1];
                    }
                break;
                }
            break;
            case 'r':
                switch (lr) {
                case 'l'://Rotate Left Shift ss Lnn sh
                    //d63..ee   ==ss   ..d00
                    //t00..63-ee==63-ss..t63
                    for (j=0;j<sh;j++) {
                        c=t[63-ee];
                        for (i=0;i<nn-1;i++) t[63-ee+i]=t[63-ee+1+i];
                        t[63-ss]=c;
                    }
                break;
                case 'r'://Rotate Right Shift ss Lnn sh
                    //d63..ee   ==ss   ..d00
                    //t00..63-ee==63-ss..t63
                    for (j=0;j<sh;j++) {
                        c=t[63-ss];
                        for (i=0;i<nn-1;i++) t[63-ss-i]=t[63-ss-1-i];
                        t[63-ee]=c;
                    }
                break;
                }
            break;
            }
            x=(double)_strtoi64(t,&e,2);
            (*iop)--;
            break;
        }
    return x;
}
int isKMGTP(char c) {
    if (c=='k'||c=='K'||c=='m'||c=='M'||c=='g'||c=='G'||c=='t'||c=='T'||c=='p'||c=='P') return 1;
    return 0;
}
void check(int ii) {
    if (ii>=STACKSIZE-1) {
        fprintf(fp,"表达式太复杂导致内部堆栈溢出\n");
        if (fp!=stdout) fclose(fp);
        exit(10);
    }
}
void prompt(__int64 result) {
    int L;
 
    L=sprintf(t,"%I64x", result);
    if (L>13 && strncmp(t,"fff",3)) fprintf(stderr,"注意:超过13位十六进制的计算结果可能是不准确的！\n");
}
double calc(char *expr, char **addr) {
    static int deep; //递归深度
    static char *fname[] = { "sin","cos","tan","sqrt","arcsin","arccos","arctan","lg","ln","exp","ceil","floor","Round","sign","abs","d2r","r2d",NULL };
    double ST[STACKSIZE] = { 0.0 }; //数字栈
    char op[STACKSIZE] = { '+' }; //运算符栈
    char ops[STACKSIZE][5];
    int flag;
    char lar[2];
    char lr[2];
    int ss,ee,nn,sh;
    char c, *rexp, *pp, *pf;
    int ist = 1, iop = 1, last, i, n;
    __int64 i64;
    char binstr[64+1];
    char *e;
 
    if (!deep) {
        pp = pf = expr;
        do {
            c = *pp++;
            if (c != ' ' && c != Tab && c != ',' && c != '_')//跳过空格、Tab字符、半角逗号(通常作为千分位分割符)、下划线(0x或0b或0o后面的16或2或8进制数字间作为间隔)
                *pf++ = c;
        } while (c != '\0');
    }
    pp = expr;
    if ((c = *pp) == '-' || c == '+') {
        op[0] = c;
        pp++;
    }
    last = !DIGIT;
    while ((c = *pp) != '\0') {
        if (c == '(') {//左圆括弧
            deep++;
            ST[ist++] = calc(++pp, addr); check(ist);
            deep--;
            ST[ist - 1] = fun(ST[ist - 1], op, ops, &iop);
            pp = *addr;
            last = DIGIT;
            if (*pp == '(' || isalpha(*pp) && strnicmp(pp, "Pi", 2) && !isKMGTP(*pp)) {//目的是：当右圆括弧的右侧为左圆括弧或函数名字时，默认其为乘法
                op[iop++] = '*'; check(iop);
                last = !DIGIT;
                c = op[--iop];
                goto operate;
            }
        }
        else if (c == ')') {//右圆括弧
            pp++;
            break;//
        }
        else if (isalpha(c)) {
            if (!strnicmp(pp, "Pi", 2)) {
                if (last == DIGIT) {
                    fprintf(fp,"π左侧遇）\n"); if (fp!=stdout) fclose(fp); exit(1);
                }
                ST[ist++] = 3.14159265358979323846264338328; check(ist);
                ST[ist - 1] = fun(ST[ist - 1], op, ops, &iop);
                pp += 2;
                last = DIGIT;
                if (isalpha(pp[0]) && pp[0]!='x' && pp[0]!='X' && pp[0]!='b' && pp[0]!='B' && pp[0]!='o' && pp[0]!='O') {
                    fprintf(fp,"两个π或K/M/G/T/P相连\n"); if (fp!=stdout) fclose(fp); exit(2);
                }
                if (*pp == '(') {
                    fprintf(fp,"π右侧遇（\n"); if (fp!=stdout) fclose(fp); exit(3);
                }
            } else if (isKMGTP(pp[0])) {
                if (last == DIGIT) {
                    fprintf(fp,"%c左侧遇）\n",pp[0]); if (fp!=stdout) fclose(fp); exit(1);
                }
                double value=1.0;
                switch (pp[0]) {
                case 'k':value=1000.0            ;break;
                case 'K':value=1024.0            ;break;
                case 'm':value=1000000.0         ;break;
                case 'M':value=1048576.0         ;break;
                case 'g':value=1000000000.0      ;break;
                case 'G':value=1073741824.0      ;break;
                case 't':value=1000000000000.0   ;break;
                case 'T':value=1099511627776.0   ;break;
                case 'p':value=1000000000000000.0;break;
                case 'P':value=1125899906842624.0;break;
                }
                ST[ist++] = value; check(ist);
                ST[ist - 1] = fun(ST[ist - 1], op, ops, &iop);
                pp += 1;
                last = DIGIT;
                if (isalpha(pp[0]) && pp[0]!='x' && pp[0]!='X' && pp[0]!='b' && pp[0]!='B' && pp[0]!='o' && pp[0]!='O') {
                    fprintf(fp,"两个π或K/M/G/T/P相连\n"); if (fp!=stdout) fclose(fp); exit(2);
                }
                if (*pp == '(') {
                    fprintf(fp,"%c右侧遇（\n",pp[-1]); if (fp!=stdout) fclose(fp); exit(3);
                }
            } else {
                for (i = 0; (pf = fname[i]) != NULL; i++)
                    if (!strnicmp(pp, pf, strlen(pf))) break;
                if (pf != NULL) {
                    op[iop++] = 7 + i; check(iop);
                    pp += strlen(pf);
                } else {
                    flag=0;
                    if (5==sscanf(pp,"shift%1[lar]%1[lr]%2d%2d%2d%n",lar,lr,&ss,&ee,&sh,&n)) {
                        if ((lar[0]=='l' || lar[0]=='a' || lar[0]=='r')
                         && (lr[0]=='l' || lr[0]=='r')
                         && (0<=ss && ss<=62)
                         && (ss<=ee-1 && ee<=63)
                         && (0<sh && sh<=ee-ss+1)) {
                            op[iop] = 24;
                            pp += n;
                            ops[iop][0]=lar[0];
                            ops[iop][1]=lr[0];
                            ops[iop][2]=(char)ss;
                            ops[iop][3]=(char)(ee-ss+1);
                            ops[iop][4]=(char)sh;
                            iop++;
                            check(iop);
                            flag=1;
                        }
                    } else
                    if (5==sscanf(pp,"shift%1[lar]%1[lr]%2dl%2d%2d%n",lar,lr,&ss,&nn,&sh,&n)) {
                        if ((lar[0]=='l' || lar[0]=='a' || lar[0]=='r')
                         && (lr[0]=='l' || lr[0]=='r')
                         && (0<=ss && ss<=62)
                         && (2<=nn && ss+nn<=64)
                         && (0<sh && sh<=nn)) {
                            op[iop] = 24;
                            pp += n;
                            ops[iop][0]=lar[0];
                            ops[iop][1]=lr[0];
                            ops[iop][2]=(char)ss;
                            ops[iop][3]=(char)nn;
                            ops[iop][4]=(char)sh;
                            iop++;
                            check(iop);
                            flag=1;
                        }
                    }
                    if (!flag) {
                        fprintf(fp,"陌生函数名\n"); if (fp!=stdout) fclose(fp); exit(4);
                    }
                }
            }
        }
        else if (c == '+' || c == '-' || c==':' || c == '*' || c == '/' || c == '%' || c == '^' || c == '&' || c == '|' || c == '@' || c=='{' || c=='}') {
            char cc;
            if (last != DIGIT) {
                fprintf(fp,"运算符粘连\n"); if (fp!=stdout) fclose(fp); exit(5);
            }
            pp++;
            if (c == '+' || c == '-' || c== '|' || c== '@') {
                do {
                    cc = op[--iop];
                    --ist;
                    switch (cc) {
                    case '+':  ST[ist - 1] += ST[ist]; break;
                    case '-':  ST[ist - 1] -= ST[ist]; break;
                    case ':':  ST[ist - 1] = 60.0*ST[ist - 1]+ST[ist]; break;
                    case '*':  ST[ist - 1] *= ST[ist]; break;
                    case '/':  ST[ist - 1] /= ST[ist]; break;
                    case '%':  ST[ist - 1] = fmod(ST[ist - 1], ST[ist]); break;
                    case '^':  ST[ist - 1] = pow(ST[ist - 1], ST[ist]); break;
                    case '&':  ST[ist - 1] = (double)(((__int64)(ST[ist - 1]))& ((__int64)(ST[ist]))); break;
                    case '|':  ST[ist - 1] = (double)(((__int64)(ST[ist - 1]))| ((__int64)(ST[ist]))); break;
                    case '@':  ST[ist - 1] = (double)(((__int64)(ST[ist - 1]))^ ((__int64)(ST[ist]))); break;
                    case '{':  ST[ist - 1] = (double)(((__int64)(ST[ist - 1]))<<((__int64)(ST[ist]))); break;
                    case '}':  ST[ist - 1] = (double)(((__int64)(ST[ist - 1]))>>((__int64)(ST[ist]))); break;
                    }
                } while (iop);
                op[iop++] = c; check(iop);
            }
            else if (c == ':' || c == '*' || c == '/' || c == '%' || c=='&') {
            operate:
                cc = op[iop - 1];
                if (cc == '+' || cc == '-') {
                    op[iop++] = c; check(iop);
                } else {
                    --ist;
                    op[iop - 1] = c;
                    switch (cc) {
                    case ':':  ST[ist - 1] = 60.0*ST[ist - 1]+ST[ist]; break;
                    case '*':  ST[ist - 1] *= ST[ist]; break;
                    case '/':  ST[ist - 1] /= ST[ist]; break;
                    case '%':  ST[ist - 1] = fmod(ST[ist - 1], ST[ist]); break;
                    case '^':  ST[ist - 1] = pow(ST[ist - 1], ST[ist]); break;
                    case '&':  ST[ist - 1] = (double)(((__int64)(ST[ist - 1]))& ((__int64)(ST[ist]))); break;
                    case '|':  ST[ist - 1] = (double)(((__int64)(ST[ist - 1]))| ((__int64)(ST[ist]))); break;
                    case '@':  ST[ist - 1] = (double)(((__int64)(ST[ist - 1]))^ ((__int64)(ST[ist]))); break;
                    case '{':  ST[ist - 1] = (double)(((__int64)(ST[ist - 1]))<<((__int64)(ST[ist]))); break;
                    case '}':  ST[ist - 1] = (double)(((__int64)(ST[ist - 1]))>>((__int64)(ST[ist]))); break;
                    }
                }
            } else {//c == '^' || c=='{' || c=='}'
                cc = op[iop - 1];
                if (cc == '^' || cc == '{' || cc == '}') {
                    fprintf(fp,"乘幂^或左移{或右移}连用\n"); if (fp!=stdout) fclose(fp); exit(6);
                }
                op[iop++] = c; check(iop);
            }
            last = !DIGIT;
        } else {
            if (last == DIGIT) {
                fprintf(fp,"两数字粘连\n"); if (fp!=stdout) fclose(fp); exit(7);
            }
            if (pp[0] == '0') {
                if (pp[1] == 'x' || pp[1] == 'X') {
                    sscanf(pp + 2, "%I64x%n", &i64, &n);
                    rexp = pp + 2 + n;
                    ST[ist++] = (double)i64; check(ist);
                } else
                if (pp[1] == 'b' || pp[1] == 'B') {
                    binstr[0]=0; n=0;
                    sscanf(pp + 2, "%64[01]%n", binstr, &n);
                    i64=_strtoi64(binstr,&e,2);
                    rexp = pp + 2 + n;
                    ST[ist++] = (double)i64; check(ist);
                } else
                if (pp[1] == 'o' || pp[1] == 'O') {
                    binstr[0]=0; n=0;
                    sscanf(pp + 2, "%24[0-7]%n", binstr, &n);
                    i64=_strtoi64(binstr,&e,8);
                    rexp = pp + 2 + n;
                    ST[ist++] = (double)i64; check(ist);
                } else {
                    ST[ist++] = strtod(pp, &rexp); check(ist);
                }
            } else {
                ST[ist++] = strtod(pp, &rexp); check(ist);
            }
            ST[ist - 1] = fun(ST[ist - 1], op, ops, &iop);
            if (pp == rexp) {
                fprintf(fp,"非法字符\n"); if (fp!=stdout) fclose(fp); exit(8);
            }
            pp = rexp;
            last = DIGIT;
            if (*pp == '(' || isalpha(*pp)) {//目的是：当右圆括弧的右侧为左圆括弧或函数名字时，默认其为乘法
                op[iop++] = '*'; check(iop);
                last = !DIGIT;
                c = op[--iop];
                goto operate;
            }
        }
    }
    *addr = pp;
    if (iop >= ist) {
        fprintf(fp,"表达式有误\n"); if (fp!=stdout) fclose(fp); exit(9);
    }
    while (iop) {
        --ist;
        switch (op[--iop]) {
        case '+':  ST[ist - 1] += ST[ist]; break;
        case '-':  ST[ist - 1] -= ST[ist]; break;
        case ':':  ST[ist - 1] = 60.0*ST[ist - 1]+ST[ist]; break;
        case '*':  ST[ist - 1] *= ST[ist]; break;
        case '/':  ST[ist - 1] /= ST[ist]; break;
        case '%':  ST[ist - 1] = fmod(ST[ist - 1], ST[ist]); break;
        case '^':  ST[ist - 1] = pow(ST[ist - 1], ST[ist]); break;
        case '&':  ST[ist - 1] = (double)(((__int64)(ST[ist - 1]))& ((__int64)(ST[ist]))); break;
        case '|':  ST[ist - 1] = (double)(((__int64)(ST[ist - 1]))| ((__int64)(ST[ist]))); break;
        case '@':  ST[ist - 1] = (double)(((__int64)(ST[ist - 1]))^ ((__int64)(ST[ist]))); break;
        case '{':  ST[ist - 1] = (double)(((__int64)(ST[ist - 1]))<<((__int64)(ST[ist]))); break;
        case '}':  ST[ist - 1] = (double)(((__int64)(ST[ist - 1]))>>((__int64)(ST[ist]))); break;
        }
    }
    return ST[0];
}
char *gapfmt(char *res) {
    int L,i,j,k;
    char *p;
 
    if (fmt==0 || strchr(res,'e')) strcpy(gap,res);
    else if (fmt==1) {//1-半角逗号每3位间隔整数部分
        L=strlen(res);
        p=strrchr(res,'.');
        j=0;
        if (p) {
            for (i=L-1;i>=p-res;i--) {
                gap[j]=res[i];
                j++;
            }
            L=p-res;
        }
        k=0;
        for (i=L-1;i>=0;i--) {
            gap[j]=res[i];
            k++;
            j++;
            if ((k%3)==0 && i>0 && res[i-1]!='-') {
                gap[j]=',';
                j++;
            }
        }
        gap[j]=0;
        strrev(gap);
    }
    else if (fmt==2) {//2-下划线每4位间隔整数部分
        L=strlen(res);
        p=strrchr(res,'.');
        j=0;
        if (p) {
            for (i=L-1;i>=p-res;i--) {
                gap[j]=res[i];
                j++;
            }
            L=p-res;
        }
        k=0;
        for (i=L-1;i>=0;i--) {
            gap[j]=res[i];
            k++;
            j++;
            if ((k%4)==0 && i>0 && res[i-1]!='-') {
                gap[j]='_';
                j++;
            }
        }
        gap[j]=0;
        strrev(gap);
    }
    return gap;
}
void pretreatment() {//预处理
    int i,L,n,r;
    char *p,*q;
    double v;
    char D[2];
 
    fmt=0;
    if (s[0]==',') fmt=1;
    if (s[0]=='_') fmt=2;
 
    //将两边不是字母且左边不是非数字或串开头紧跟0的x替换为*,目的是支持用x代替*,且和0x开头的16进制数不冲突
    L=strlen(s);
    for (i=1;i<L;i++) {
        if (s[i]=='x' && (!isalpha(s[i-1]) || isKMGTP(s[i-1])) && !isalpha(s[i+1])) {
            if (!(
                 (i==1 && s[0]=='0')
              || (i>1 && s[i-1]=='0' && !isdigit(s[i-2]))
               )) s[i]='*';
        }
    }
 
    //将"数字\.数字[kmgtpKMGTP]"用()括住
    strcpy(t,s);
    p=&t[0];
    q=s;
    while (1) {
        r=sscanf(p,"%lf%n%1[GKMPTgkmpt]",&v,&n,D);
        if (r==EOF) break;//
        if (r==0) {
            L=sprintf(q,"%c",*p);
            q+=L;
            p++;
        } else if (r==1) {
            L=sprintf(q,"%.*s",n,p);
            q+=L;
            p+=n;
        } else if (r==2) {
            L=sprintf(q,"(%.*s%c)",n,p,D[0]);
            q+=L;
            p+=n+1;
        }
    }
}
int main(int argc, char **argv) {
    int a,c;
    double r;
    __int64 result;
    char *p;
    char b[64+1];
    char neg;
    FILE *f;
    int flag;
 
    setlocale( LC_ALL,"chs");
    fp=stdout;
    if (argc<2) {
        //if (GetConsoleOutputCP() != 936) system("chcp 936>NUL");//中文代码页
        printf("计算函数表达式的值。\n支持(),+,-,*,x,/,%%,^,&,|,@,{,},Pi,sin,cos,tan,sqrt,arcsin,arccos,arctan,lg,ln,exp,ceil,floor,Round,sign,abs,d2r,r2d,k,m,g,t,p,K,M,G,T,P,shift{l|a|r}{l|r}{ss}{ee|lnn}{sh}\n");
        while (1) {
            printf("请输入表达式：");
            fgets(s,MAXLEN,stdin);
            if ('\n' == s[strlen(s)-1]) s[strlen(s) - 1] = 0;
            if (s[0] == 0) break;//
            c=0;
            p=strrchr(s,' ');
            if (p) {
                p++;
                     if (1 == sscanf(p, ".%d", &pcs) && 0 <= pcs && pcs <= 15) c=1;
                else if (1 == sscanf(p, "g%d", &pcs) && 1 <= pcs && pcs <= 15) c=2;
                else if (1 == sscanf(p, "e%d", &pcs) && 0 <= pcs && pcs <= 15) c=3;
                else if (0==stricmp(p,"x_")                                  ) c=4;
                else if (p[0] == 'x' || p[0] == 'X'                          ) c=5;
                else if (p[0] == 'b' || p[0] == 'B'                          ) c=6;
                else if (p[0] == 'o' || p[0] == 'O'                          ) c=7;
                else if (p[0] == ':'                                         ) c=8;
            }
            if (c) p[-1]=0;
            pretreatment();
            r=calc(s, &endss);
            result=(__int64)r;
            switch (c) {
            case 0: sprintf(t,"%.15lg",      r); printf("%s\n",gapfmt(t)); break;
            case 1: sprintf(t,"%.*lf" , pcs, r); printf("%s\n",gapfmt(t)); break;
            case 2: sprintf(t,"%.*lg" , pcs, r); printf("%s\n",gapfmt(t)); break;
            case 3: printf("%.*le\n"  , pcs, r); break;
            case 4:
                sprintf(t,"%016I64x", result);
                printf("0x%.2s_%.2s_%.2s_%.2s_%.2s_%.2s_%.2s_%.2s\n",
                    t+ 0,
                    t+ 2,
                    t+ 4,
                    t+ 6,
                    t+ 8,
                    t+10,
                    t+12,
                    t+14);
                prompt(result);
            break;
            case 5:
                printf("0x%016I64x\n", result);
                prompt(result);
            break;
            case 6:
                _i64toa(result,b,2);
                sprintf(t,"%064s",b);
                printf("0b%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s\n",
                    t+ 0,
                    t+ 4,
                    t+ 8,
                    t+12,
                    t+16,
                    t+20,
                    t+24,
                    t+28,
                    t+32,
                    t+36,
                    t+40,
                    t+44,
                    t+48,
                    t+52,
                    t+56,
                    t+60);
                prompt(result);
            break;
            case 7:
                sprintf(t,"%024I64o", result);
                printf("0o%.4s_%.4s_%.4s_%.4s_%.4s_%.4s\n",
                    t+ 0,
                    t+ 4,
                    t+ 8,
                    t+12,
                    t+16,
                    t+20);
                prompt(result);
            break;
            case 8:
                if (fabs(r)<(10000*365+2500)*86400.0) {
                    neg=0;if (r<0) {r=-r;neg=1;}
                         if (r<    1.0) sprintf(t,                            "%.3lf" , r);
                    else if (r<   60.0) sprintf(t,                      "%02I64d.%03d",                                                          (__int64)r%60,(int)(fmod(r,1000.0)*1000.0+0.5)%1000);
                    else if (r< 3600.0) sprintf(t,              "%02I64d:%02I64d.%03d",                                       (__int64)r     /60,(__int64)r%60,(int)(fmod(r,1000.0)*1000.0+0.5)%1000);
                    else if (r<86400.0) sprintf(t,      "%02I64d:%02I64d:%02I64d.%03d",                 (__int64)r      /3600,(__int64)r%3600/60,(__int64)r%60,(int)(fmod(r,1000.0)*1000.0+0.5)%1000);
                    else                sprintf(t,"%I64d %02I64d:%02I64d:%02I64d.%03d",(__int64)r/86400,(__int64)r%86400/3600,(__int64)r%3600/60,(__int64)r%60,(int)(fmod(r,1000.0)*1000.0+0.5)%1000);
                    if (neg) printf("-%s\n",t); else printf("%s\n",t);
                } else {
                    sprintf(t,"%.15lg",r);
                    printf("%s\n",gapfmt(t));
                }
            break;
            }
        }
        return 0;
    }
    if (argc == 2 && 0 == strcmp(argv[1], "/?")) {
        //if (GetConsoleOutputCP() != 936) system("chcp 936>NUL");//中文代码页
        printf(
            "计算由≥1个命令行参数给出的函数表达式的值。\n"
            "支持(),+,-,*,x,/,%%,^^,^&,^|,^@,Pi,sin,cos,tan,sqrt,arcsin,arccos,arctan,lg,ln,exp,ceil,floor,Round,sign,abs,d2r,r2d,k,m,g,t,p,K,M,G,T,P\n"
            "最后一个参数是.0～.15 结果小数点后保留0～15位\n"
            "最后一个参数是g1～g15 结果保留有效数字1～15位\n"
            "最后一个参数是e0～e15 结果用科学计数法表示，且小数点后保留0～15位\n"
            "最后一个参数是x       结果以16进制正整数格式输出\n"
            "最后一个参数是x_      结果以16进制正整数且每2位用_间隔格式输出\n"
            "最后一个参数是b       结果以2进制正整数且每4位用_间隔格式输出\n"
            "最后一个参数是o       结果以8进制正整数且每4位用_间隔格式输出\n"
            "最后一个参数是:       结果以DDD HH:MM:SS.mss格式输出\n"
            "支持:间隔的HH:MM:SS.mss格式输入\n"
            "16进制整数以0x或0X开头，2进制整数以0b或0B开头，8进制整数以0o或0O开头，且可以包含下划线间隔\n"
            "支持64位二进制算数左移{和右移}运算符\n"
            "支持64位二进制指定部分位段二进制移位函数shift{l|a|r}{l|r}{ss}{ee|lnn}{sh} 其中:\n"
            "    {l|a|r} Logic|Arithmetic|Rotate 逻辑|算数|循环\n"
            "    {l|r}   Left|Right              左移|右移\n"
            "    {ss}    start_bit               开始位（00～63）\n"
            "    {ee}    end_bit                 结束位（开始位～63）\n"
            "    {nn}    n_bits                  位宽（02～64）\n"
            "    {sh}    shift_bits              移位次数（01～位宽）\n"
            "    例如“shiftar010503(0b101111) b”表示将二进制数101111算数右移bit01～bit05三次，结果为：\n"
            "        0b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0011_1101\n"
            "忽略表达式中的半角逗号(通常作为千分位分割符)\n"
            "第一个参数是半角逗号  结果整数部分每3位间隔半角逗号\n"
            "第一个参数是下划线    结果整数部分每4位间隔下划线\n"
            "第一个参数是c:\\data.txt，计算c:\\data.txt中各行总和或最后一行HH:MM:SS.mss与第一行HH:MM:SS.mss之差\n"
            "第一个参数是/f且c:\\jsresult.txt可写，将所有输出重定向到该文件\n"
        );
        return 0;
    }
    if (argc>2 && 0 == strcmp(argv[1], "/f")) {
        fp=fopen("c:\\jsresult.txt","w");
        if (NULL==fp) fp=stdout;
        for (a=2;a<argc;a++) argv[a-1]=argv[a];
        argc--;
    }
    strncpy(s, argv[1], MAXLEN - 1); s[MAXLEN - 1] = 0;
    if (argc>2) {
        for (a = 2; a<argc - 1; a++) {//将空格间隔的各参数连接到s
            if (strlen(s)+strlen(argv[a])<MAXLEN-1) {
                strcat(s, argv[a]);
            } else {
                fprintf(fp,"要计算的表达式太长(>%d个字符)\n",MAXLEN);
                if (fp!=stdout) fclose(fp);
                exit(12);
            }
        }
        if (1 == sscanf(argv[a], ".%d", &pcs) && 0 <= pcs && pcs <= 15) {//最后一个参数是.0～.15表示将计算结果保留小数0～15位
            pretreatment();
            sprintf(t,"%.*lf", pcs, calc(s, &endss));
            fprintf(fp,"%s\n",gapfmt(t));
        } else if (1 == sscanf(argv[a], "g%d", &pcs) && 1 <= pcs && pcs <= 15) {//最后一个参数是g1～g15表示将计算结果保留有效数字1～15位
            pretreatment();
            sprintf(t,"%.*lg", pcs, calc(s, &endss));
            fprintf(fp,"%s\n",gapfmt(t));
        } else if (1 == sscanf(argv[a], "e%d", &pcs) && 0 <= pcs && pcs <= 15) {//最后一个参数是e0～e15表示将计算结果用科学计数法表示，且小数点后保留0～15位
            pretreatment();fprintf(fp,"%.*le\n", pcs, calc(s, &endss));
        } else if (0==stricmp(argv[a],"x_")) {//最后一个参数是x_或X_表示将计算结果以16进制正整数且每2位用_间隔格式输出
            pretreatment();
            result=(__int64)calc(s, &endss);
            sprintf(t,"%016I64x", result);
            fprintf(fp,"0x%.2s_%.2s_%.2s_%.2s_%.2s_%.2s_%.2s_%.2s\n",
                t+ 0,
                t+ 2,
                t+ 4,
                t+ 6,
                t+ 8,
                t+10,
                t+12,
                t+14);
            prompt(result);
        } else if (argv[a][0] == 'x' || argv[a][0] == 'X') {//最后一个参数是x表示将计算结果以16进制正整数格式输出
            pretreatment();
            result=(__int64)calc(s, &endss);
            fprintf(fp,"0x%016I64x\n", result);
            prompt(result);
        } else if (argv[a][0] == 'b' || argv[a][0] == 'B') {//最后一个参数是b表示将计算结果以2进制正整数且每4位用_间隔格式输出
            pretreatment();
            result=(__int64)calc(s, &endss);
            _i64toa(result,b,2);
            sprintf(t,"%064s",b);
            fprintf(fp,"0b%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s_%.4s\n",
                t+ 0,
                t+ 4,
                t+ 8,
                t+12,
                t+16,
                t+20,
                t+24,
                t+28,
                t+32,
                t+36,
                t+40,
                t+44,
                t+48,
                t+52,
                t+56,
                t+60);
            prompt(result);
        } else if (argv[a][0] == 'o' || argv[a][0] == 'O') {//最后一个参数是o表示将计算结果以8进制正整数且每4位用_间隔格式输出
            pretreatment();
            result=(__int64)calc(s, &endss);
            sprintf(t,"%024I64o", result);
            printf("0o%.4s_%.4s_%.4s_%.4s_%.4s_%.4s\n",
                t+ 0,
                t+ 4,
                t+ 8,
                t+12,
                t+16,
                t+20);
            prompt(result);
        } else if (argv[a][0] == ':') {//最后一个参数是:表示将计算结果以DDD HH:MM:SS.mss格式输出
        colon:
            pretreatment();
            r=calc(s, &endss);
            if (fabs(r)<(10000*365+2500)*86400.0) {
                neg=0;if (r<0) {r=-r;neg=1;}
                     if (r<    1.0) sprintf(t,                            "%.3lf" , r);
                else if (r<   60.0) sprintf(t,                      "%02I64d.%03d",                                                          (__int64)r%60,(int)(fmod(r,1000.0)*1000.0+0.5)%1000);
                else if (r< 3600.0) sprintf(t,              "%02I64d:%02I64d.%03d",                                       (__int64)r     /60,(__int64)r%60,(int)(fmod(r,1000.0)*1000.0+0.5)%1000);
                else if (r<86400.0) sprintf(t,      "%02I64d:%02I64d:%02I64d.%03d",                 (__int64)r      /3600,(__int64)r%3600/60,(__int64)r%60,(int)(fmod(r,1000.0)*1000.0+0.5)%1000);
                else                sprintf(t,"%I64d %02I64d:%02I64d:%02I64d.%03d",(__int64)r/86400,(__int64)r%86400/3600,(__int64)r%3600/60,(__int64)r%60,(int)(fmod(r,1000.0)*1000.0+0.5)%1000);
                if (neg) fprintf(fp,"-%s\n",t); else fprintf(fp,"%s\n",t);
            } else {
                sprintf(t,"%.15lg",r);
                fprintf(fp,"%s\n",gapfmt(t));
            }
        } else {
            strcat(s, argv[a]);
        normal:
            pretreatment();
            sprintf(t,"%.15lg", calc(s, &endss));
            fprintf(fp,"%s\n",gapfmt(t));
        }
    } else if (0==strcmp(argv[1],"c:\\data.txt")) {
        f=fopen("c:\\data.txt","r");
        if (NULL==f) {
            fprintf(fp,"无法打开文件c:\\data.txt");
            if (fp!=stdout) fclose(fp);
            exit(11);
        }
        if (fgets(gap,MAXLEN,f)) {
            if (gap[strlen(gap)-1]=='\n') gap[strlen(gap)-1]=0;
            flag=1;
            if (2==sscanf(gap,"%d:%d",&a,&c)) flag=0;
            strcpy(s,gap);
            while (1) {
                if (NULL==fgets(gap,MAXLEN,f)) break;//
                if (gap[strlen(gap)-1]=='\n') gap[strlen(gap)-1]=0;
                if (flag) {
                    if (strlen(s)+2+strlen(gap)+1<MAXLEN-1) {
                        strcat(s, "+(");
                        strcat(s, gap);
                        strcat(s, ")");
                    } else {
                        fclose(f);
                        fprintf(fp,"要计算的表达式太长(>%d个字符)\n",MAXLEN);
                        if (fp!=stdout) fclose(fp);
                        exit(12);
                    }
                }
            }
            fclose(f);
            if (!flag) {
                strcat(gap, "-");
                strcat(gap, s);
                strcpy(s,gap);
                goto colon;
            } else goto normal;
        }
        fclose(f);
    } else {
        pretreatment();
        sprintf(t,"%.15lg", calc(s, &endss));
        fprintf(fp,"%s\n",gapfmt(t));
    }
    if (fp!=stdout) fclose(fp);
    return 0;
}