#ifndef _SRC_AVL_TREE_H_
#define _SRC_AVL_TREE_H_
#include "common.h"

// 获取AVL树的高度
int avltree_height(bo_tree_node_t *tree);

// 前序遍历"AVL树"
void avltree_preorder(bo_tree_node_t *tree);
// 中序遍历"AVL树"
void avltree_inorder(bo_tree_node_t *tree);
// 后序遍历"AVL树"
void avltree_postorder(bo_tree_node_t *tree);

// (递归实现)查找"AVL树x"中键值为key的节点
bo_tree_node_t* avltree_search(bo_tree_node_t *x, u_short key);
// (非递归实现)查找"AVL树x"中键值为key的节点
bo_tree_node_t* avltree_iter_search(bo_tree_node_t *x, u_short key);

// 查找最小结点：返回tree为根结点的AVL树的最小结点。
bo_tree_node_t* avltree_minimum(bo_tree_node_t *tree);
// 查找最大结点：返回tree为根结点的AVL树的最大结点。
bo_tree_node_t* avltree_maximum(bo_tree_node_t *tree);

// 将结点插入到AVL树中，返回根节点
bo_tree_node_t* avltree_insert(bo_value_t *bo, bo_tree_node_t *tree, 
                            u_short key);
bo_tree_node_t* avltree_insert_node(bo_tree_node_t *tree, 
                                bo_tree_node_t *node);

// 删除结点(key是节点值)，返回根节点
bo_tree_node_t* avltree_delete(bo_tree_node_t *tree, u_short key);


bo_tree_node_t* avltree_delete_node(bo_tree_node_t *tree, bo_tree_node_t*z);

bo_tree_node_t* avltree_create_node(bo_value_t *bo, u_short key, 
                                    bo_tree_node_t *left, 
                                    bo_tree_node_t *right);

// 销毁AVL树
void avltree_destory(bo_tree_node_t *tree);

/** 
 * @brief   reset all node's fresh flag.
 * 
 * @param   tree
 */
void avltree_reset_fresh(bo_tree_node_t *tree);

/** 
 * @brief   get count(*) number
 * 
 * @param   tree
 * 
 * @return  The total number of node at tree
 */
int avltree_count_node(bo_tree_node_t *tree);

/** 
 * @brief   find expire node use interation method
 * 
 * @param   tree:avltree root
 * 
 * @return  tree
 */
bo_tree_node_t* avltree_iter_search_expire(bo_tree_node_t *tree);

#endif
