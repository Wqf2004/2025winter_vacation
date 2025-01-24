#include <stdio.h>
#include <string.h>
int count_substring(char *str, char *sub) {
    int count = 0;
    int len = strlen(sub);
    for (int i = 0; i <= strlen(str) - len; i++) {
        if (strncmp(str + i, sub, len) == 0) {
            count++;
        }
    }
    return count;
}
int main() {
    char str[] = "aaddfdfsfsfdfsie";
    char sub[] = "fs";
    printf("The substring '%s' appears %d times in '%s'.\n", sub, count_substring(str, sub), str);
    return 0;
}