/*
 * 字符串处理 - C语言控制台版
 * 包含四个问题：DNA排序、字符串排序、整理单词、字符串种类统计
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_STR_LEN 100
#define MAX_WORDS 100
#define MAX_DNA_LEN 100

/*
 * (1) DNA排序 - 计算逆序数
 */
int calculate_dna_inversion(char *dna, int len) {
    int count = 0;
    char order[] = {'A', 'C', 'G', 'T'};

    for (int i = 0; i < len; i++) {
        for (int j = i + 1; j < len; j++) {
            int pos_i = -1, pos_j = -1;
            for (int k = 0; k < 4; k++) {
                if (order[k] == dna[i]) pos_i = k;
                if (order[k] == dna[j]) pos_j = k;
            }
            if (pos_i > pos_j) count++;
        }
    }
    return count;
}

void dna_sort() {
    printf("========================================\n");
    printf("(1) DNA排序\n");
    printf("========================================\n");

    int n, m;
    printf("输入 n m: ");
    scanf("%d %d", &n, &m);

    char dnas[MAX_WORDS][MAX_DNA_LEN + 1];
    int inversions[MAX_WORDS];

    for (int i = 0; i < n; i++) {
        scanf("%s", dnas[i]);
        inversions[i] = calculate_dna_inversion(dnas[i], m);
    }

    // 冒泡排序（根据逆序数）
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (inversions[j] > inversions[j + 1]) {
                // 交换逆序数
                int temp = inversions[j];
                inversions[j] = inversions[j + 1];
                inversions[j + 1] = temp;

                // 交换DNA字符串
                char temp_str[MAX_DNA_LEN + 1];
                strcpy(temp_str, dnas[j]);
                strcpy(dnas[j], dnas[j + 1]);
                strcpy(dnas[j + 1], temp_str);
            }
        }
    }

    printf("\n排序结果:\n");
    for (int i = 0; i < n; i++) {
        printf("%s\n", dnas[i]);
    }
    printf("\n");
}

/*
 * (2) 字符串排序
 */
void string_sort() {
    printf("========================================\n");
    printf("(2) 字符串排序\n");
    printf("========================================\n");

    int n;
    printf("输入字符串个数 n: ");
    scanf("%d", &n);
    getchar();  // 消耗换行符

    char strings[MAX_WORDS][MAX_STR_LEN];
    char unique_strings[MAX_WORDS][MAX_STR_LEN];
    int counts[MAX_WORDS] = {0};
    int unique_count = 0;

    for (int i = 0; i < n; i++) {
        fgets(strings[i], MAX_STR_LEN, stdin);
        // 去除换行符
        strings[i][strcspn(strings[i], "\n")] = '\0';

        // 检查是否已在唯一列表中
        int found = 0;
        for (int j = 0; j < unique_count; j++) {
            if (strcmp(strings[i], unique_strings[j]) == 0) {
                counts[j]++;
                found = 1;
                break;
            }
        }
        if (!found) {
            strcpy(unique_strings[unique_count], strings[i]);
            counts[unique_count] = 1;
            unique_count++;
        }
    }

    // 按字典序排序
    for (int i = 0; i < unique_count - 1; i++) {
        for (int j = 0; j < unique_count - i - 1; j++) {
            if (strcmp(unique_strings[j], unique_strings[j + 1]) > 0) {
                char temp[MAX_STR_LEN];
                strcpy(temp, unique_strings[j]);
                strcpy(unique_strings[j], unique_strings[j + 1]);
                strcpy(unique_strings[j + 1], temp);

                int temp_count = counts[j];
                counts[j] = counts[j + 1];
                counts[j + 1] = temp_count;
            }
        }
    }

    printf("\n排序结果:\n");
    for (int i = 0; i < unique_count; i++) {
        double percentage = (double)counts[i] / n * 100;
        printf("%s %.4f\n", unique_strings[i], percentage);
    }
    printf("\n");
}

/*
 * (3) 整理单词
 */
void arrange_words() {
    printf("========================================\n");
    printf("(3) 整理单词\n");
    printf("========================================\n");

    char dictionary[MAX_WORDS][MAX_STR_LEN];
    int dict_count = 0;

    printf("输入字典(每行一个单词, 输入XXXXXX结束):\n");
    while (1) {
        fgets(dictionary[dict_count], MAX_STR_LEN, stdin);
        dictionary[dict_count][strcspn(dictionary[dict_count], "\n")] = '\0';

        if (strcmp(dictionary[dict_count], "XXXXXX") == 0) {
            break;
        }
        dict_count++;
    }

    printf("输入要整理的字符串(输入XXXXXX结束):\n");
    while (1) {
        char input[MAX_STR_LEN];
        fgets(input, MAX_STR_LEN, stdin);
        input[strcspn(input, "\n")] = '\0';

        if (strcmp(input, "XXXXXX") == 0) {
            break;
        }

        char matches[MAX_WORDS][MAX_STR_LEN];
        int match_count = 0;
        int input_len = strlen(input);

        // 统计输入字符串中每个字母的出现次数
        int input_counts[26] = {0};
        for (int i = 0; i < input_len; i++) {
            input_counts[input[i] - 'a']++;
        }

        // 在字典中查找匹配的单词
        for (int i = 0; i < dict_count; i++) {
            if (strlen(dictionary[i]) != input_len) {
                continue;
            }

            int dict_counts[26] = {0};
            for (int j = 0; j < strlen(dictionary[i]); j++) {
                dict_counts[dictionary[i][j] - 'a']++;
            }

            int match = 1;
            for (int k = 0; k < 26; k++) {
                if (input_counts[k] != dict_counts[k]) {
                    match = 0;
                    break;
                }
            }

            if (match) {
                strcpy(matches[match_count], dictionary[i]);
                match_count++;
            }
        }

        // 按字典序排序匹配结果
        for (int i = 0; i < match_count - 1; i++) {
            for (int j = 0; j < match_count - i - 1; j++) {
                if (strcmp(matches[j], matches[j + 1]) > 0) {
                    char temp[MAX_STR_LEN];
                    strcpy(temp, matches[j]);
                    strcpy(matches[j], matches[j + 1]);
                    strcpy(matches[j + 1], temp);
                }
            }
        }

        // 输出结果
        if (match_count == 0) {
            printf("NOT A VALID WORD\n");
        } else {
            for (int i = 0; i < match_count; i++) {
                printf("%s\n", matches[i]);
            }
        }
        printf("******\n");
    }
    printf("\n");
}

/*
 * (4) 字符串种类统计
 */
void string_type_statistics() {
    printf("========================================\n");
    printf("(4) 字符串种类统计\n");
    printf("========================================\n");

    int n, m;
    printf("输入 n m: ");
    scanf("%d %d", &n, &m);

    char strings[MAX_WORDS][MAX_STR_LEN];
    char unique_strings[MAX_WORDS][MAX_STR_LEN];
    int counts[MAX_WORDS] = {0};
    int unique_count = 0;

    for (int i = 0; i < n; i++) {
        scanf("%s", strings[i]);

        // 检查是否已在唯一列表中
        int found = 0;
        for (int j = 0; j < unique_count; j++) {
            if (strcmp(strings[i], unique_strings[j]) == 0) {
                counts[j]++;
                found = 1;
                break;
            }
        }
        if (!found) {
            strcpy(unique_strings[unique_count], strings[i]);
            counts[unique_count] = 1;
            unique_count++;
        }
    }

    // 统计每个出现次数对应的字符串种类数
    int result[MAX_WORDS + 1] = {0};
    for (int i = 0; i < unique_count; i++) {
        result[counts[i]]++;
    }

    printf("\n统计结果:\n");
    for (int i = 1; i <= n; i++) {
        printf("%d\n", result[i]);
    }
    printf("\n");
}

int main() {
    dna_sort();
    string_sort();
    arrange_words();
    string_type_statistics();

    return 0;
}
