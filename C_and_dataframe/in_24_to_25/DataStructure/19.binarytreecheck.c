/*给定一个无序序列，编程实现平均查找长度最小的二叉排序树的构造，
并编写二叉排序树查找函数。*/

#include <stdio.h>
#include <stdlib.h>

// Structure for a binary search tree node
struct TreeNode {
    int value;
    struct TreeNode* left;
    struct TreeNode* right;
};

// Function to create a new tree node
struct TreeNode* createNode(int value) {
    struct TreeNode* newNode = (struct TreeNode*)malloc(sizeof(struct TreeNode));
    newNode->value = value;
    newNode->left = newNode->right = NULL;
    return newNode;
}

// Function to insert a value into the BST
struct TreeNode* insert(struct TreeNode* root, int value) {
    if (root == NULL) {
        return createNode(value);
    }
    if (value < root->value) {
        root->left = insert(root->left, value);
    } else {
        root->right = insert(root->right, value);
    }
    return root;
}

// Function to search for a value in the BST
struct TreeNode* search(struct TreeNode* root, int value) {
    if (root == NULL || root->value == value) {
        return root; // Found or reached leaf
    }
    if (value < root->value) {
        return search(root->left, value);
    }
    return search(root->right, value);
}

// Function to build the BST from an array
struct TreeNode* buildBST(int arr[], int size) {
    struct TreeNode* root = NULL;
    for (int i = 0; i < size; i++) {
        root = insert(root, arr[i]);
    }
    return root;
}