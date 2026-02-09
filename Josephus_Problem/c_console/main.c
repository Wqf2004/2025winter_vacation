/*
 * Josephus环问题 - C语言控制台版
 * 包含四种变体
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_PEOPLE 64
#define MAX_NAME_LEN 16
#define MAX_CARDS 20

/*
 * (1) 带人名的Josephus环问题
 */
void josephus_with_names(char names[MAX_PEOPLE][MAX_NAME_LEN], int n, int k, int m) {
    int people[MAX_PEOPLE];
    int eliminated[MAX_PEOPLE];
    int current = k - 1;
    int remaining = n;

    for (int i = 0; i < n; i++) {
        people[i] = i;
    }

    printf("出列顺序:\n");
    for (int round = 0; round < n; round++) {
        current = (current + m - 1) % remaining;
        eliminated[round] = people[current];

        // 移动后面的元素
        for (int i = current; i < remaining - 1; i++) {
            people[i] = people[i + 1];
        }
        remaining--;
    }

    for (int i = 0; i < n; i++) {
        printf("%s\n", names[eliminated[i]]);
    }
}

/*
 * (2) 反Josephus环问题
 * 找到使得第x个人最后出列的起始位置k
 */
int reverse_josephus(int n, int m, int x) {
    for (int k = 1; k <= n; k++) {
        int people[MAX_PEOPLE];
        int remaining = n;
        int current = k - 1;

        for (int i = 0; i < n; i++) {
            people[i] = i + 1;
        }

        for (int round = 0; round < n - 1; round++) {
            current = (current + m - 1) % remaining;

            for (int i = current; i < remaining - 1; i++) {
                people[i] = people[i + 1];
            }
            remaining--;
        }

        if (people[0] == x) {
            return k;
        }
    }

    return -1;
}

/*
 * (3) Josephus环问题的变形 - 寻找最小的m使得最后剩下k个好人
 */
int josephus_variant(int k) {
    int total_people = 2 * k;

    for (int m = 1; m < 100000; m++) {
        int people[MAX_PEOPLE * 2];
        int remaining = total_people;
        int current = 0;

        for (int i = 0; i < total_people; i++) {
            people[i] = i + 1;
        }

        int good_eliminated = 0;
        while (remaining > k && good_eliminated == 0) {
            current = current % remaining;
            int eliminated = people[current];

            if (eliminated <= k) {
                good_eliminated = 1;
            }

            for (int i = current; i < remaining - 1; i++) {
                people[i] = people[i + 1];
            }
            remaining--;
            current = current % remaining;
        }

        if (remaining == k) {
            int all_good = 1;
            for (int i = 0; i < k; i++) {
                if (people[i] > k) {
                    all_good = 0;
                    break;
                }
            }
            if (all_good) {
                return m;
            }
        }
    }

    return -1;
}

/*
 * (4) 直线型报数问题
 */
void linear_counting(int n, int x, int cards[], int cards_len, int lucky[], int *lucky_count, int *cards_used) {
    int people[MAX_PEOPLE * 2];
    int remaining = n;
    int current_card_idx = 0;

    for (int i = 0; i < n; i++) {
        people[i] = i + 1;
    }

    while (remaining > x) {
        if (current_card_idx >= cards_len) break;

        int m = cards[current_card_idx];
        current_card_idx++;
        int current_idx = 0;

        while (current_idx < remaining && remaining > x) {
            current_idx = (current_idx + m - 1) % remaining;

            for (int i = current_idx; i < remaining - 1; i++) {
                people[i] = people[i + 1];
            }
            remaining--;
            current_idx = current_idx % remaining;
        }
    }

    *lucky_count = remaining;
    *cards_used = current_card_idx;
    for (int i = 0; i < remaining; i++) {
        lucky[i] = people[i];
    }
}

/*
 * 测试带人名的Josephus环问题
 */
void test_josephus_with_names() {
    printf("========================================\n");
    printf("(1) 带人名的Josephus环问题测试\n");
    printf("========================================\n");

    char names[MAX_PEOPLE][MAX_NAME_LEN] = {
        "Caobainan",
        "Mazhongyi",
        "Shenyongqiang",
        "Taozhengyi",
        "Jiangdebing"
    };
    int n = 5;
    int k = 2;
    int m = 3;

    printf("输入:\n");
    printf("  人数: %d\n", n);
    printf("  k=%d, m=%d\n", k, m);
    printf("\n");
    printf("输出:\n");

    josephus_with_names(names, n, k, m);
    printf("\n");
}

/*
 * 测试反Josephus环问题
 */
void test_reverse_josephus() {
    printf("========================================\n");
    printf("(2) 反Josephus环问题测试\n");
    printf("========================================\n");

    int n = 41, m = 3, x = 3;
    int result = reverse_josephus(n, m, x);

    printf("输入:\n");
    printf("  n=%d, m=%d, x=%d\n", n, m, x);
    printf("\n");
    printf("输出:\n");
    printf("  k=%d\n", result);
    printf("  验证: 期望 k=14, 实际 k=%d, %s\n\n", result, result == 14 ? "?" : "?");
}

/*
 * 测试Josephus环问题的变形
 */
void test_josephus_variant() {
    printf("========================================\n");
    printf("(3) Josephus环问题的变形测试\n");
    printf("========================================\n");

    struct {
        int k;
        int expected_m;
    } test_cases[] = {
        {3, 5},
        {4, 30}
    };

    for (int i = 0; i < 2; i++) {
        int k = test_cases[i].k;
        int expected_m = test_cases[i].expected_m;
        int result = josephus_variant(k);

        printf("输入: k=%d\n", k);
        printf("输出: m=%d\n", result);
        printf("验证: 期望 m=%d, 实际 m=%d, %s\n\n",
               expected_m, result, result == expected_m ? "?" : "?");
    }
}

/*
 * 测试直线型报数问题
 */
void test_linear_counting() {
    printf("========================================\n");
    printf("(4) 直线型报数问题测试\n");
    printf("========================================\n");

    // 测试用例1
    {
        int n = 10, x = 2;
        int cards[] = {3, 5, 4, 3, 2, 9, 6, 10, 10, 6, 2, 6, 7, 3, 4, 7, 4, 5, 3, 2};
        int lucky[MAX_PEOPLE * 2];
        int lucky_count, cards_used;

        printf("测试用例 1:\n");
        printf("输入:\n");
        printf("  n=%d, X=%d\n", n, x);
        printf("  卡片数值: ");
        for (int i = 0; i < 5; i++) printf("%d ", cards[i]);
        printf("\n\n");

        linear_counting(n, x, cards, 20, lucky, &lucky_count, &cards_used);

        printf("输出:\n");
        printf("  幸运位置: ");
        for (int i = 0; i < lucky_count; i++) {
            printf("%d ", lucky[i]);
        }
        printf("\n  使用卡片数: %d\n", cards_used);
        printf("验证: 位置=%s, 卡片数=%s\n\n",
               (lucky_count == 2 && lucky[0] == 1 && lucky[1] == 8) ? "?" : "?",
               (cards_used == 5) ? "?" : "?");
    }

    // 测试用例2
    {
        int n = 47, x = 6;
        int cards[] = {11, 2, 7, 3, 4, 8, 5, 10, 7, 8, 3, 7, 4, 2, 3, 9, 10, 2, 5, 3};
        int lucky[MAX_PEOPLE * 2];
        int lucky_count, cards_used;

        printf("测试用例 2:\n");
        printf("输入:\n");
        printf("  n=%d, X=%d\n", n, x);
        printf("  卡片数值: ");
        for (int i = 0; i < 11; i++) printf("%d ", cards[i]);
        printf("\n\n");

        linear_counting(n, x, cards, 20, lucky, &lucky_count, &cards_used);

        printf("输出:\n");
        printf("  幸运位置: ");
        for (int i = 0; i < lucky_count; i++) {
            printf("%d ", lucky[i]);
        }
        printf("\n  使用卡片数: %d\n", cards_used);
        printf("验证: 位置=%s, 卡片数=%s\n\n",
               (lucky_count == 6 && lucky[0] == 1 && lucky[1] == 3 &&
                lucky[2] == 16 && lucky[3] == 23 && lucky[4] == 31 && lucky[5] == 47) ? "?" : "?",
               (cards_used == 11) ? "?" : "?");
    }
}

int main() {
    test_josephus_with_names();
    test_reverse_josephus();
    test_josephus_variant();
    test_linear_counting();

    return 0;
}
