#include<stdio.h>
#include<stdlib.h>

// 二叉树结点类型定义;
typedef struct bnode
{  
    int data;
    struct bnode *lc, *rc; // 相当于一个节点处分叉出了两条链表
}BNode;

// 中序遍历（递归）；
void inOrderTraversal(BNode* node) {
    if (node == NULL) {
        return;
    }
    inOrderTraversal(node->lc); // 遍历左子树
    printf("%d ", node->data);  // 访问节点
    inOrderTraversal(node->rc); // 遍历右子树
}

// 先序遍历（递归）；
void preOrderTraversal(BNode* node) {
    if (node == NULL) {
        return;
    }
    printf("%d ", node->data);     // 访问节点
    preOrderTraversal(node->lc);   // 遍历左子树
    preOrderTraversal(node->rc);   // 遍历右子树
}

// 后序遍历（递归）；
void postOrderTraversal(BNode* node) {
    if (node == NULL) {
        return;
    }
    postOrderTraversal(node->lc); // 遍历左子树
    postOrderTraversal(node->rc); // 遍历右子树
    printf("%d ", node->data);    // 访问节点
}



// 按照先序遍历方法根据输入的字母序列创建二叉树（递归）；
BNode* create(char* sequence, int* index) {
    // 递归截止情况
    if (sequence[*index] == '#' || sequence[*index] == '\0') { 
        // 将*index视为扫描机器，当碰到'#'认为是当前对应位置子树的终止；碰到'\0'认为是整棵树的终止
        if(sequence[*index] == '\0') return NULL;
        (*index)++; // 当不为'\0'时，移动扫描机器到下一个位置
        return NULL;
    }

    // 用当前字符创建一个新的节点
    BNode* newNode = (BNode*)malloc(sizeof(BNode));
    newNode->data = sequence[*index] - '0'; // BNode的data域为int类型，用减'0'的方式从字符反算出值
    newNode->lc = NULL;
    newNode->rc = NULL;
    (*index)++; // 跳到下一个字符

    // 递归创建左右子树
    newNode->lc = create(sequence, index);
    newNode->rc = create(sequence, index);

    return newNode;
}

// 创建二叉排序树（递归）；
BNode* insert(BNode* root, int data) {
    // 判断当前树是否为空，为空则创建新节点
    if (root == NULL) {
        BNode* newNode = (BNode*)malloc(sizeof(BNode));
        newNode->data = data;
        newNode->lc = NULL;
        newNode->rc = NULL;
        return newNode; // 将这个新节点返回
    }

    // 不断递归到树里面去，找到为空的子树创建新节点
    if (data < root->data) {
        root->lc = insert(root->lc, data); 
    } 
    else {
        root->rc = insert(root->rc, data); 
    }

    return root;
}

// 请分别用递归和栈来实现求二叉树树高。
// 这是递归计算树高的方法
int calculataHeight(BNode* node)
{
    if(node == NULL)
    {
        return 0;
    }

    int leftHeight = calculataHeight(node->lc);
    int rightHeight = calculataHeight(node->rc);

    return leftHeight > rightHeight ? leftHeight:rightHeight+1;
}
// 定义栈节点结构体，用于存储节点及其对应的深度；
typedef struct StackNode {
    BNode *treeNode;
    int depth;
} StackNode;

// 用栈来实现二叉树的前序遍历；以及用栈来实现求二叉树树高
int preorderTraversalAndHeight(BNode *root) {
    if (root == NULL) return 0;

    // 初始化栈和最大高度
    StackNode stack[1000];
    int top = -1;
    int height = 0;

    // 根节点入栈，深度为1
    stack[++top].treeNode = root;
    stack[top].depth = 1;

    while (top != -1) {
        // 出栈并访问
        StackNode sn = stack[top--];
        BNode *node = sn.treeNode;
        int depth = sn.depth;

        printf("%d ", node->data);

        // 更新最大高度
        if (depth > height) {
            height = depth;
        }

        // 先右后左入栈，并更新深度
        if (node->rc) {
            stack[++top].treeNode = node->rc;
            stack[top].depth = depth + 1;
        }
        if (node->lc) {
            stack[++top].treeNode = node->lc;
            stack[top].depth = depth + 1;
        }
    }
    return height;
}

// 由先序遍历和中序遍历序列重构二叉树；
BNode* buildTree1(char* preorder, char* inorder, int inorderStart, int inorderEnd, int* preorderIndex) {
    // 递归截止情况：inorder的Start位置和End位置相遇
    if (inorderStart > inorderEnd) {
        return NULL;
    }

    // 用当前字符创建一个新的节点
    BNode* newNode = (BNode*)malloc(sizeof(BNode));
    newNode->data = preorder[*preorderIndex] - '0'; 
    newNode->lc = NULL;
    newNode->rc = NULL;
    (*preorderIndex)++;  // 跳到下一个字符

    // 找到当前插入节点对应在二叉树中的根节点，将树分成相应的左右子树
    int inorderIndex;
    for (inorderIndex = inorderStart; inorderIndex <= inorderEnd; inorderIndex++) {
        if (inorder[inorderIndex] - '0' == newNode->data) {
            break;
        }
    } 

    // 在对应的区间递归式的创建子树
    newNode->lc = buildTree1(preorder, inorder, inorderStart, inorderIndex - 1, preorderIndex);
    newNode->rc = buildTree1(preorder, inorder, inorderIndex + 1, inorderEnd, preorderIndex);

    return newNode;
}

// 已知后序和中序遍历序列，编程实现二叉树的重构（请写出算法步骤）。
BNode* buildTree2(char* postorder, char* inorder, int inorderStart, int inorderEnd, int* postorderIndex) {
    // 递归截止情况：inorder的Start位置和End位置相遇
    if (inorderStart > inorderEnd) {
        return NULL;
    }

    // 检查postorderIndex是否有效
    if (*postorderIndex < 0) {
        return NULL; // 如果postorderIndex无效，返回NULL
    }

    // 用当前字符创建一个新的节点
    BNode* newNode = (BNode*)malloc(sizeof(BNode));
    newNode->data = postorder[*postorderIndex] - '0'; 
    newNode->lc = NULL;
    newNode->rc = NULL;
    (*postorderIndex)--;  // 跳到前一个字符

    // 找到当前插入节点对应在二叉树中的根节点，将树分成相应的左右子树
    int inorderIndex;
    for (inorderIndex = inorderStart; inorderIndex <= inorderEnd; inorderIndex++) {
        if (inorder[inorderIndex] - '0' == newNode->data) {
            break;
        }
    } 

    // 在对应的区间递归式的创建子树
    newNode->rc = buildTree2(postorder, inorder, inorderIndex + 1, inorderEnd, postorderIndex);
    newNode->lc = buildTree2(postorder, inorder, inorderStart, inorderIndex - 1, postorderIndex);

    return newNode;
}

// 主函数
int main() {
    // 用字符串的形式创建一棵二叉树
    char sequence[] = "124##5##36##7"; 
    int index = 0; // 设计一个读取sequence中内容的扫描机器
    BNode* root1 = create(sequence, &index);

    // 用中、先、后序的方法分别遍历这棵二叉树
    printf("In-order traversal of the first tree: ");
    inOrderTraversal(root1);
    printf("\n");

    printf("Pre-order traversal of the first tree: ");
    preOrderTraversal(root1);
    printf("\n");

    printf("Post-order traversal of the first tree: ");
    postOrderTraversal(root1);
    printf("\n");

    // 通过数组来创建一棵二叉排序树
    BNode* root2 = NULL;
    int values[] = {5, 3, 7, 2, 4, 6, 8};
    for (int i = 0; i < sizeof(values) / sizeof(values[0]); i++) {
        root2 = insert(root2, values[i]);
    }

    // 用中、先、后序的方法分别遍历这棵二叉树
    printf("In-order traversal of the second tree (BST): ");
    inOrderTraversal(root2);
    printf("\n");

    printf("Pre-order traversal of the second tree (BST): ");
    preOrderTraversal(root2);
    printf("\n");

    printf("Post-order traversal of the second tree (BST): ");
    postOrderTraversal(root2);
    printf("\n");

    // 调用非递归方式的函数先序遍历第一棵二叉树
    printf("基于栈的方式对the first root进行先序遍历：");
    int height = preorderTraversalAndHeight(root1);
    printf("\nThe height of the first tree:%d\n ",height);

    // 调用buildTree1函数重构二叉树
    char preorder[] = "5342768"; 
    char inorder[] = "2435678";  
    int preorderIndex = 0;
    printf("字符串中有7个字符时字符串的真实长度为：%d\n",sizeof(inorder)); // 验证字符串的真实长度
    BNode* root3 = buildTree1(preorder, inorder, 0, sizeof(inorder) - 2, &preorderIndex); // Build the tree
    // 这里减2的原因是：为了获取中序遍历的最后一个有效索引，我们通常需要减去 1（因为索引是从 0 开始的），
    // 而在这里减去 2 可能是因为数组的最后一个元素是一个空字符（'\0'），所以需要再减去 1。
    printf("In-order traversal of the third tree used preorder: ");
    inOrderTraversal(root3);

    // 调用buildTree2函数重构二叉树
    char postorder[] = "2436875"; 
    int postorderIndex = sizeof(inorder) - 2;
    printf("\n"); 
    BNode* root4 = buildTree2(postorder, inorder, 0, sizeof(inorder) - 2, &postorderIndex); // Build the tree
    // 这里减2的原因是：为了获取中序遍历的最后一个有效索引，我们通常需要减去 1（因为索引是从 0 开始的），
    // 而在这里减去 2 可能是因为数组的最后一个元素是一个空字符（'\0'），所以需要再减去 1。
    printf("In-order traversal of the third tree used postorder: ");
    inOrderTraversal(root4);

    return 0;
}
