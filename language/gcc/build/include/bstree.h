#ifndef _SRC_BST_BSTREE_H_
#define _SRC_BST_BSTREE_H_

typedef unsigned short  u_short;
struct bo_node {
    u_short              bo;
    void                *lhead;      //The header of list.
    struct bo_node      *left;
    struct bo_node      *right;
};

typedef struct bo_node bo_node_t;

#define BST_OK                         0
#define ERR_BST_ENOUGH_MEMORY          -30001 
#define ERR_BST_EMPTY_TREE             -30002 


/** 
 * @brief   find minimum node in a binary tree
 * 
 * @param   node: The binary tree's header node
 * 
 * @return  a structure node
 */
bo_node_t* find_min(bo_node_t *node);

/** 
 * @brief   find maximum node in a binary tree
 * 
 * @param   node: The binary tree's header node
 * 
 * @return  a structure node
 */
bo_node_t* find_max(bo_node_t *node);

/** 
 * @brief   insert a data to binary tree
 * 
 * @param   node: The binary tree's header node    
 * @param   data: a data
 * 
 * @return  a new node which is inserting just.
 */
bo_node_t * insert_node(bo_node_t *node, u_short bo, void *lhead);
   
/** 
 * @brief   delete a node by data
 * 
 * @param   node: The binary tree's header node
 * @param   data: a data
 * 
 * @return  The next node for delete node.
 */
bo_node_t *delete_node(bo_node_t *node, u_short bo);

/** 
 * @brief   find a now by data
 * 
 * @param   node: The binary tree's header node
 * @param   data: a data
 * 
 * @return  a node which is finding
 */
bo_node_t * find_node(bo_node_t *node, u_short bo);

#endif
