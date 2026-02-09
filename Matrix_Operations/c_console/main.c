/*
 * 矩阵运算 - C语言控制台版
 * 功能：矩阵加、矩阵减、矩阵乘、矩阵求逆、矩阵三角化、矩阵转置
 * 实现方式1：参数为二维数组名、行数、列数
 * 实现方式2：参数为指针、行数、列数
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_SIZE 20

/* 函数声明 */

/* 实现方式1：参数为二维数组名、行数、列数 */
void matrix_add_1(double matrix1[MAX_SIZE][MAX_SIZE], double matrix2[MAX_SIZE][MAX_SIZE],
                 double result[MAX_SIZE][MAX_SIZE], int rows, int cols);
void matrix_subtract_1(double matrix1[MAX_SIZE][MAX_SIZE], double matrix2[MAX_SIZE][MAX_SIZE],
                      double result[MAX_SIZE][MAX_SIZE], int rows, int cols);
void matrix_multiply_1(double matrix1[MAX_SIZE][MAX_SIZE], double matrix2[MAX_SIZE][MAX_SIZE],
                      double result[MAX_SIZE][MAX_SIZE], int rows1, int cols1, int cols2);
int matrix_transpose_1(double matrix[MAX_SIZE][MAX_SIZE], double result[MAX_SIZE][MAX_SIZE],
                     int rows, int cols);
void matrix_print_1(double matrix[MAX_SIZE][MAX_SIZE], int rows, int cols);

/* 实现方式2：参数为指针、行数、列数 */
void matrix_add_2(double *matrix1, double *matrix2, double *result, int rows, int cols);
void matrix_subtract_2(double *matrix1, double *matrix2, double *result, int rows, int cols);
void matrix_multiply_2(double *matrix1, double *matrix2, double *result,
                      int rows1, int cols1, int cols2);
int matrix_transpose_2(double *matrix, double *result, int rows, int cols);
void matrix_print_2(double *matrix, int rows, int cols);
int matrix_inverse_2(double *matrix, double *result, int n);
int matrix_gaussian_2(double *matrix, double *result, int rows, int cols);

/* 辅助函数 */
void clear_screen(void);
void pause_screen(void);
void print_separator(void);
void input_matrix_1(double matrix[MAX_SIZE][MAX_SIZE], int *rows, int *cols);
void input_matrix_elements(double matrix[MAX_SIZE][MAX_SIZE], int rows, int cols);

/* 主函数 */
int main(void) {
    char input[10];
    int choice;

    /* 矩阵存储 */
    double matrix1[MAX_SIZE][MAX_SIZE] = {0};
    double matrix2[MAX_SIZE][MAX_SIZE] = {0};
    double result[MAX_SIZE][MAX_SIZE] = {0};

    /* 用于方式2的指针版本 */
    double *p_matrix1, *p_result;

    int rows1, cols1, rows2, cols2;

    while (1) {
        clear_screen();
        print_separator();
        printf("          矩阵运算系统\n");
        print_separator();
        printf("  1. 矩阵加法\n");
        printf("  2. 矩阵减法\n");
        printf("  3. 矩阵乘法\n");
        printf("  4. 矩阵转置\n");
        printf("  5. 矩阵求逆（使用指针方式）\n");
        printf("  6. 矩阵三角化（使用指针方式）\n");
        printf("  0. 退出系统\n");
        print_separator();
        printf("\n请选择功能（0-6）：");

        scanf("%s", input);

        if (strlen(input) != 1 || input[0] < '0' || input[0] > '6') {
            printf("\n输入无效，请输入0-6之间的数字！\n");
            pause_screen();
            continue;
        }

        choice = input[0] - '0';

        switch (choice) {
            case 1: /* 矩阵加法 */
                printf("\n=== 矩阵加法 ===\n");
                printf("输入第一个矩阵：\n");
                input_matrix_1(matrix1, &rows1, &cols1);
                printf("输入第二个矩阵：\n");
                printf("注意：第二个矩阵必须是 %d 行 %d 列\n", rows1, cols1);
                input_matrix_elements(matrix2, rows1, cols1);
                rows2 = rows1;
                cols2 = cols1;

                if (rows1 != rows2 || cols1 != cols2) {
                    printf("\n错误：矩阵维度不匹配！\n");
                    pause_screen();
                    break;
                }

                matrix_add_1(matrix1, matrix2, result, rows1, cols1);

                printf("\n结果矩阵：\n");
                matrix_print_1(result, rows1, cols1);
                pause_screen();
                break;

            case 2: /* 矩阵减法 */
                printf("\n=== 矩阵减法 ===\n");
                printf("输入第一个矩阵：\n");
                input_matrix_1(matrix1, &rows1, &cols1);
                printf("输入第二个矩阵：\n");
                printf("注意：第二个矩阵必须是 %d 行 %d 列\n", rows1, cols1);
                input_matrix_elements(matrix2, rows1, cols1);
                rows2 = rows1;
                cols2 = cols1;

                if (rows1 != rows2 || cols1 != cols2) {
                    printf("\n错误：矩阵维度不匹配！\n");
                    pause_screen();
                    break;
                }

                matrix_subtract_1(matrix1, matrix2, result, rows1, cols1);

                printf("\n结果矩阵：\n");
                matrix_print_1(result, rows1, cols1);
                pause_screen();
                break;

            case 3: /* 矩阵乘法 */
                printf("\n=== 矩阵乘法 ===\n");
                printf("输入第一个矩阵：\n");
                input_matrix_1(matrix1, &rows1, &cols1);
                printf("输入第二个矩阵：\n");
                printf("注意：第二个矩阵的行数必须是 %d\n", cols1);
                input_matrix_1(matrix2, &rows2, &cols2);

                if (cols1 != rows2) {
                    printf("\n错误：矩阵维度不匹配！第一个矩阵的列数必须等于第二个矩阵的行数。\n");
                    pause_screen();
                    break;
                }

                matrix_multiply_1(matrix1, matrix2, result, rows1, cols1, cols2);

                printf("\n结果矩阵：\n");
                matrix_print_1(result, rows1, cols2);
                pause_screen();
                break;

            case 4: /* 矩阵转置 */
                printf("\n=== 矩阵转置 ===\n");
                printf("输入矩阵：\n");
                input_matrix_1(matrix1, &rows1, &cols1);

                matrix_transpose_1(matrix1, result, rows1, cols1);

                printf("\n转置矩阵：\n");
                matrix_print_1(result, cols1, rows1);
                pause_screen();
                break;

            case 5: /* 矩阵求逆（指针方式） */
                printf("\n=== 矩阵求逆 ===\n");
                printf("输入方阵：\n");
                input_matrix_1(matrix1, &rows1, &cols1);

                if (rows1 != cols1) {
                    printf("\n错误：只能对方阵求逆！\n");
                    pause_screen();
                    break;
                }

                p_matrix1 = &matrix1[0][0];
                p_result = &result[0][0];

                if (matrix_inverse_2(p_matrix1, p_result, rows1)) {
                    printf("\n逆矩阵：\n");
                    matrix_print_1(result, rows1, cols1);
                } else {
                    printf("\n错误：矩阵不可逆（行列式为零）！\n");
                }
                pause_screen();
                break;

            case 6: /* 矩阵三角化（指针方式） */
                printf("\n=== 矩阵三角化 ===\n");
                printf("输入矩阵：\n");
                input_matrix_1(matrix1, &rows1, &cols1);

                p_matrix1 = &matrix1[0][0];
                p_result = &result[0][0];

                matrix_gaussian_2(p_matrix1, p_result, rows1, cols1);

                printf("\n三角化矩阵：\n");
                matrix_print_1(result, rows1, cols1);
                pause_screen();
                break;

            case 0: /* 退出 */
                printf("\n感谢使用矩阵运算系统，再见！\n");
                pause_screen();
                return 0;

            default:
                break;
        }
    }

    return 0;
}

/* ==================== 实现方式1：参数为二维数组名、行数、列数 ==================== */

void matrix_add_1(double matrix1[MAX_SIZE][MAX_SIZE], double matrix2[MAX_SIZE][MAX_SIZE],
                 double result[MAX_SIZE][MAX_SIZE], int rows, int cols) {
    int i, j;
    for (i = 0; i < rows; i++) {
        for (j = 0; j < cols; j++) {
            result[i][j] = matrix1[i][j] + matrix2[i][j];
        }
    }
}

void matrix_subtract_1(double matrix1[MAX_SIZE][MAX_SIZE], double matrix2[MAX_SIZE][MAX_SIZE],
                      double result[MAX_SIZE][MAX_SIZE], int rows, int cols) {
    int i, j;
    for (i = 0; i < rows; i++) {
        for (j = 0; j < cols; j++) {
            result[i][j] = matrix1[i][j] - matrix2[i][j];
        }
    }
}

void matrix_multiply_1(double matrix1[MAX_SIZE][MAX_SIZE], double matrix2[MAX_SIZE][MAX_SIZE],
                      double result[MAX_SIZE][MAX_SIZE], int rows1, int cols1, int cols2) {
    int i, j, k;
    for (i = 0; i < rows1; i++) {
        for (j = 0; j < cols2; j++) {
            result[i][j] = 0;
            for (k = 0; k < cols1; k++) {
                result[i][j] += matrix1[i][k] * matrix2[k][j];
            }
        }
    }
}

int matrix_transpose_1(double matrix[MAX_SIZE][MAX_SIZE], double result[MAX_SIZE][MAX_SIZE],
                     int rows, int cols) {
    int i, j;
    for (i = 0; i < rows; i++) {
        for (j = 0; j < cols; j++) {
            result[j][i] = matrix[i][j];
        }
    }
    return 1;
}

void matrix_print_1(double matrix[MAX_SIZE][MAX_SIZE], int rows, int cols) {
    int i, j;
    for (i = 0; i < rows; i++) {
        for (j = 0; j < cols; j++) {
            printf("%8.2f ", matrix[i][j]);
        }
        printf("\n");
    }
}

/* ==================== 实现方式2：参数为指针、行数、列数 ==================== */

void matrix_add_2(double *matrix1, double *matrix2, double *result, int rows, int cols) {
    int i, j, index;
    for (i = 0; i < rows; i++) {
        for (j = 0; j < cols; j++) {
            index = i * MAX_SIZE + j;
            result[index] = matrix1[index] + matrix2[index];
        }
    }
}

void matrix_subtract_2(double *matrix1, double *matrix2, double *result, int rows, int cols) {
    int i, j, index;
    for (i = 0; i < rows; i++) {
        for (j = 0; j < cols; j++) {
            index = i * MAX_SIZE + j;
            result[index] = matrix1[index] - matrix2[index];
        }
    }
}

void matrix_multiply_2(double *matrix1, double *matrix2, double *result,
                      int rows1, int cols1, int cols2) {
    int i, j, k;
    int idx1, idx2, idxr;
    double sum;

    for (i = 0; i < rows1; i++) {
        for (j = 0; j < cols2; j++) {
            sum = 0;
            idxr = i * MAX_SIZE + j;
            for (k = 0; k < cols1; k++) {
                idx1 = i * MAX_SIZE + k;
                idx2 = k * MAX_SIZE + j;
                sum += matrix1[idx1] * matrix2[idx2];
            }
            result[idxr] = sum;
        }
    }
}

int matrix_transpose_2(double *matrix, double *result, int rows, int cols) {
    int i, j, idx_src, idx_dst;
    for (i = 0; i < rows; i++) {
        for (j = 0; j < cols; j++) {
            idx_src = i * MAX_SIZE + j;
            idx_dst = j * MAX_SIZE + i;
            result[idx_dst] = matrix[idx_src];
        }
    }
    return 1;
}

void matrix_print_2(double *matrix, int rows, int cols) {
    int i, j, index;
    for (i = 0; i < rows; i++) {
        for (j = 0; j < cols; j++) {
            index = i * MAX_SIZE + j;
            printf("%8.2f ", matrix[index]);
        }
        printf("\n");
    }
}

/* 矩阵求逆（使用高斯消元法） */
int matrix_inverse_2(double *matrix, double *result, int n) {
    int i, j, k, index, idx;
    double temp, factor;
    double *temp_matrix = (double *)malloc(n * n * sizeof(double));
    double *identity = (double *)malloc(n * n * sizeof(double));

    if (temp_matrix == NULL || identity == NULL) {
        return 0;
    }

    /* 复制矩阵并初始化单位矩阵 */
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            idx = i * MAX_SIZE + j;
            temp_matrix[idx] = matrix[idx];
            identity[idx] = (i == j) ? 1.0 : 0.0;
        }
    }

    /* 高斯消元法 */
    for (k = 0; k < n; k++) {
        /* 选主元 */
        index = k;
        for (i = k + 1; i < n; i++) {
            idx = i * MAX_SIZE + k;
            if (fabs(temp_matrix[idx]) > fabs(temp_matrix[index * MAX_SIZE + k])) {
                index = i;
            }
        }

        /* 交换行 */
        if (index != k) {
            for (j = 0; j < n; j++) {
                idx = k * MAX_SIZE + j;
                temp = temp_matrix[idx];
                temp_matrix[idx] = temp_matrix[index * MAX_SIZE + j];
                temp_matrix[index * MAX_SIZE + j] = temp;

                temp = identity[idx];
                identity[idx] = identity[index * MAX_SIZE + j];
                identity[index * MAX_SIZE + j] = temp;
            }
        }

        /* 消元 */
        if (fabs(temp_matrix[k * MAX_SIZE + k]) < 1e-10) {
            free(temp_matrix);
            free(identity);
            return 0; /* 矩阵不可逆 */
        }

        for (i = k + 1; i < n; i++) {
            factor = temp_matrix[i * MAX_SIZE + k] / temp_matrix[k * MAX_SIZE + k];
            for (j = k; j < n; j++) {
                idx = i * MAX_SIZE + j;
                temp_matrix[idx] -= factor * temp_matrix[k * MAX_SIZE + j];
            }
            for (j = 0; j < n; j++) {
                idx = i * MAX_SIZE + j;
                identity[idx] -= factor * identity[k * MAX_SIZE + j];
            }
        }
    }

    /* 回代 */
    for (i = n - 1; i >= 0; i--) {
        for (j = i + 1; j < n; j++) {
            idx = i * MAX_SIZE + j;
            identity[idx] -= temp_matrix[idx] * identity[j * MAX_SIZE + j];
        }
        idx = i * MAX_SIZE + i;
        identity[idx] /= temp_matrix[idx];
    }

    /* 复制结果 */
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            idx = i * MAX_SIZE + j;
            result[idx] = identity[idx];
        }
    }

    free(temp_matrix);
    free(identity);
    return 1;
}

/* 矩阵三角化（高斯消元） */
int matrix_gaussian_2(double *matrix, double *result, int rows, int cols) {
    int i, j, k, index, idx;
    double temp, factor;

    /* 复制矩阵 */
    for (i = 0; i < rows; i++) {
        for (j = 0; j < cols; j++) {
            idx = i * MAX_SIZE + j;
            result[idx] = matrix[idx];
        }
    }

    /* 高斯消元 */
    for (k = 0; k < rows && k < cols; k++) {
        /* 选主元 */
        index = k;
        for (i = k + 1; i < rows; i++) {
            idx = i * MAX_SIZE + k;
            if (fabs(result[idx]) > fabs(result[index * MAX_SIZE + k])) {
                index = i;
            }
        }

        /* 交换行 */
        if (index != k) {
            for (j = 0; j < cols; j++) {
                idx = k * MAX_SIZE + j;
                temp = result[idx];
                result[idx] = result[index * MAX_SIZE + j];
                result[index * MAX_SIZE + j] = temp;
            }
        }

        /* 消元 */
        if (fabs(result[k * MAX_SIZE + k]) < 1e-10) {
            continue; /* 跳过零主元 */
        }

        for (i = k + 1; i < rows; i++) {
            factor = result[i * MAX_SIZE + k] / result[k * MAX_SIZE + k];
            for (j = k; j < cols; j++) {
                idx = i * MAX_SIZE + j;
                result[idx] -= factor * result[k * MAX_SIZE + j];
            }
        }
    }

    return 1;
}

/* ==================== 辅助函数 ==================== */

void clear_screen(void) {
    system("cls || clear");
}

void pause_screen(void) {
    printf("\n按任意键继续...");
    getchar();
    getchar();
}

void print_separator(void) {
    printf("========================================\n");
}

void input_matrix_1(double matrix[MAX_SIZE][MAX_SIZE], int *rows, int *cols) {
    int i, j;

    printf("请输入矩阵的行数：");
    scanf("%d", rows);
    printf("请输入矩阵的列数：");
    scanf("%d", cols);

    if (*rows > MAX_SIZE || *cols > MAX_SIZE) {
        printf("错误：矩阵尺寸超过最大限制 %d！\n", MAX_SIZE);
        *rows = 0;
        *cols = 0;
        return;
    }

    printf("请输入矩阵元素（按行输入）：\n");
    for (i = 0; i < *rows; i++) {
        printf("第 %d 行：", i + 1);
        for (j = 0; j < *cols; j++) {
            scanf("%lf", &matrix[i][j]);
        }
    }
}

/* 输入已知尺寸的矩阵元素（方式1） */
void input_matrix_elements(double matrix[MAX_SIZE][MAX_SIZE], int rows, int cols) {
    int i, j;

    printf("请输入矩阵元素（按行输入）：\n");
    for (i = 0; i < rows; i++) {
        printf("第 %d 行：", i + 1);
        for (j = 0; j < cols; j++) {
            scanf("%lf", &matrix[i][j]);
        }
    }
}
