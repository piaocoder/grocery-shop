#include "avltree.h"

#include <stdio.h>
#include <stdlib.h>

#define HEIGHT(p)    ( (p==NULL) ? -1 : (((bo_tree_node_t*)(p))->height) )
#define MAX(a, b)    ( (a) > (b) ? (a) : (b) )

static inline void avltree_value_copy(bo_tree_node_t *new, bo_tree_node_t *old);

static inline void avltree_value_copy(bo_tree_node_t *new, bo_tree_node_t *old)
{
    // Value not include height.
    new->key = old->key;
    new->value = old->value;
}

/*
 * 获取AVL树的高度
 */
int avltree_height(bo_tree_node_t *tree)
{
    return HEIGHT(tree);
}

/*
 * 前序遍历"AVL树"
 */
void avltree_preorder(bo_tree_node_t *tree)
{
    if(tree != NULL)
    {
        avltree_preorder(tree->left);
        avltree_preorder(tree->right);
    }
}


/*
 * 中序遍历"AVL树"
 */
void avltree_inorder(bo_tree_node_t *tree)
{
    if(tree != NULL)
    {
        avltree_inorder(tree->left);
        avltree_inorder(tree->right);
    }
}

/*
 * 后序遍历"AVL树"
 */
void avltree_postorder(bo_tree_node_t *tree)
{
    if(tree != NULL)
    {
        avltree_postorder(tree->left);
        avltree_postorder(tree->right);
    }
}

/*
 * (递归实现)查找"AVL树x"中键值为key的节点
 */
bo_tree_node_t* avltree_search(bo_tree_node_t *x, u_short key)
{
    if (x==NULL || x->key==key) {
        return x;
    }

    if (key < x->key) {
        return avltree_search(x->left, key);
    }
    else {
        return avltree_search(x->right, key);
    }
}

/*
 * (非递归实现)查找"AVL树x"中键值为key的节点
 */
bo_tree_node_t* avltree_iter_search(bo_tree_node_t *x, u_short key)
{
    while ((x!=NULL) && (x->key!=key))
    {
        if (key < x->key) {
            x = x->left;
        } 
        else {
            x = x->right;
        }
    }

    return x;
}

/* 
 * 查找最小结点：返回tree为根结点的AVL树的最小结点。
 */
bo_tree_node_t* avltree_minimum(bo_tree_node_t *tree)
{
    if (tree == NULL) {
        return NULL;
    }

    while(tree->left != NULL) {
        tree = tree->left;
    }

    return tree;
}
 
/* 
 * 查找最大结点：返回tree为根结点的AVL树的最大结点。
 */
bo_tree_node_t* avltree_maximum(bo_tree_node_t *tree)
{
    if (tree == NULL) {
        return NULL;
    }

    while (tree->right != NULL) {
        tree = tree->right;
    }

    return tree;
}

/*
 * LL：左左对应的情况(左单旋转)。
 *
 * 返回值：旋转后的根节点
 */
static bo_tree_node_t* left_left_rotation(bo_tree_node_t *k2)
{
    bo_tree_node_t *k1;

    k1 = k2->left;
    k2->left = k1->right;
    k1->right = k2;

    k2->height = MAX( HEIGHT(k2->left), HEIGHT(k2->right)) + 1;
    k1->height = MAX( HEIGHT(k1->left), k2->height) + 1;

    return k1;
}

/*
 * RR：右右对应的情况(右单旋转)。
 *
 * 返回值：旋转后的根节点
 */
static bo_tree_node_t* right_right_rotation(bo_tree_node_t *k1)
{
    bo_tree_node_t *k2;

    k2 = k1->right;
    k1->right = k2->left;
    k2->left = k1;

    k1->height = MAX( HEIGHT(k1->left), HEIGHT(k1->right)) + 1;
    k2->height = MAX( HEIGHT(k2->right), k1->height) + 1;

    return k2;
}

/*
 * LR：左右对应的情况(左双旋转)。
 *
 * 返回值：旋转后的根节点
 */
static bo_tree_node_t* left_right_rotation(bo_tree_node_t *k3)
{
    k3->left = right_right_rotation(k3->left);

    return left_left_rotation(k3);
}

/*
 * RL：右左对应的情况(右双旋转)。
 *
 * 返回值：旋转后的根节点
 */
static bo_tree_node_t* right_left_rotation(bo_tree_node_t *k1)
{
    k1->right = left_left_rotation(k1->right);

    return right_right_rotation(k1);
}

/*
 * 创建AVL树结点。
 *
 * 参数说明：
 *     key 是键值。
 *     left 是左孩子。
 *     right 是右孩子。
 */
bo_tree_node_t* avltree_create_node(bo_value_t *bo, u_short key, 
                                    bo_tree_node_t *left, 
                                    bo_tree_node_t *right)
{
    bo_tree_node_t          *node;

    node = (bo_tree_node_t*)calloc(1, sizeof(bo_tree_node_t));
    if (node == NULL) {
        zlog_warn(bo->error, "Malloc memory failed.");
        return NULL;
    }
    node->key = key;
    node->height = 0;
    node->left = left;
    node->right = right;
    node->value = 0;

    return node;
}

/* 
 * 将结点插入到AVL树中，并返回根节点
 *  1,如果找到对应的节点(在执行update之前重置所有fresh标志位)：
 *          更新新鲜度，表示没必要剔除
 *
 * 参数说明：
 *     tree AVL树的根结点
 *     key 插入的结点的键值
 * 返回值：
 *     根节点
 */
bo_tree_node_t* avltree_insert(bo_value_t *bo, bo_tree_node_t *tree, 
                            u_short key)
{
    if (tree == NULL) {
        tree = avltree_create_node(bo, key, NULL, NULL);
        if (tree==NULL) {
            return NULL;
        }
    } else if (key < tree->key) {
        tree->left = avltree_insert(bo, tree->left, key);
        if (HEIGHT(tree->left) - HEIGHT(tree->right) == 2) {
            if (key < tree->left->key)
                tree = left_left_rotation(tree);
            else
                tree = left_right_rotation(tree);
        }
    } else if (key > tree->key) {
        tree->right = avltree_insert(bo, tree->right, key);
        if (HEIGHT(tree->right) - HEIGHT(tree->left) == 2) {
            if (key > tree->right->key)
                tree = right_right_rotation(tree);
            else
                tree = right_left_rotation(tree);
        }
    } else {
    }

    tree->height = MAX( HEIGHT(tree->left), HEIGHT(tree->right)) + 1;

    return tree;
}

bo_tree_node_t* avltree_insert_node(bo_tree_node_t *tree, 
                                bo_tree_node_t *node)
{
    if (tree == NULL) {
        tree = node;
    } else if (node->key < tree->key) {
        tree->left = avltree_insert_node(tree->left, node);
        if (HEIGHT(tree->left) - HEIGHT(tree->right) == 2) {
            if (node->key < tree->left->key)
                tree = left_left_rotation(tree);
            else
                tree = left_right_rotation(tree);
        }
    } else if (node->key > tree->key) {
        tree->right = avltree_insert_node(tree->right, node);
        if (HEIGHT(tree->right) - HEIGHT(tree->left) == 2) {
            if (node->key > tree->right->key)
                tree = right_right_rotation(tree);
            else
                tree = right_left_rotation(tree);
        }
    } else {
        return NULL;
    }

    tree->height = MAX( HEIGHT(tree->left), HEIGHT(tree->right)) + 1;

    return tree;
}

/* 
 * 删除结点(z)，返回根节点
 *
 * 参数说明：
 *     ptree AVL树的根结点
 *     z 待删除的结点
 * 返回值：
 *     根节点
 */
bo_tree_node_t* avltree_delete_node(bo_tree_node_t *tree, bo_tree_node_t*z)
{
    bo_tree_node_t *tmp = NULL;

    if (tree==NULL || z==NULL) {
        return NULL;
    }

    if (z->key < tree->key) {
        tree->left = avltree_delete_node(tree->left, z);
        if (HEIGHT(tree->right) - HEIGHT(tree->left) == 2) {
            bo_tree_node_t*r =  tree->right;
            if (HEIGHT(r->left) > HEIGHT(r->right)) {
                tree = right_left_rotation(tree);
            } else {
                tree = right_right_rotation(tree);
            }
        }
    } else if (z->key > tree->key) {
        tree->right = avltree_delete_node(tree->right, z);
        if (HEIGHT(tree->left) - HEIGHT(tree->right) == 2)
        {
            bo_tree_node_t*l =  tree->left;
            if (HEIGHT(l->right) > HEIGHT(l->left)) {
                tree = left_right_rotation(tree);
            } else {
                tree = left_left_rotation(tree);
            }
        }
    } else {
        if ((tree->left) && (tree->right))
        {
            if (HEIGHT(tree->left) > HEIGHT(tree->right)) {
                bo_tree_node_t*max = avltree_maximum(tree->left);
                avltree_value_copy(tree, max);
                tree->left = avltree_delete_node(tree->left, max);
            } else {
                bo_tree_node_t*min = avltree_maximum(tree->right);
                avltree_value_copy(tree, min);
                tree->right = avltree_delete_node(tree->right, min);
            }
        } else {
            tmp = tree;
            tree = tree->left ? tree->left : tree->right;
            free(tmp);
        }
    }

    return tree;
}

/* 
 * 删除结点(key是节点值)，返回根节点
 *
 * 参数说明：
 *     tree AVL树的根结点
 *     key 待删除的结点的键值
 * 返回值：
 *     根节点
 */
bo_tree_node_t* avltree_delete(bo_tree_node_t *tree, u_short key)
{
    bo_tree_node_t       *z = NULL; 

    if ((z = avltree_search(tree, key)) != NULL)
        tree = avltree_delete_node(tree, z);
    return tree;
}

/* 
 * 销毁AVL树
 */
void avltree_destory(bo_tree_node_t *tree)
{
    if (tree==NULL)
        return ;

    if (tree->left != NULL)
        avltree_destory(tree->left);
    if (tree->right != NULL)
        avltree_destory(tree->right);

    free(tree);
}

/** 
 * @brief   get count(*) number
 * 
 * @param   tree
 * 
 * @return  The total number of node at tree
 */
int avltree_count_node(bo_tree_node_t *tree)
{
    if (NULL == tree->left && NULL == tree->right) {
        return 1;
    }

    return avltree_count_node(tree->left) + 
        avltree_count_node(tree->right);
}

