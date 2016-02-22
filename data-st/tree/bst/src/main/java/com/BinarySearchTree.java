package com;

/**
 * @file BinarySearchTree.java
 * @brief   二叉查找树的相关操作纪要
 * @author unlessbamboo
 * @version 1.0
 * @date 2016-02-22
 */


public class BinarySearchTree<TKey, TValue> : 
        SymbolTables<TKey, TValue> where TKey : 
        IComparable<TKey>, IEquatable<TValue>
{
    private Node root;

    private class Node
    {
        public Node     Left { get; set; }
        public Node     Right { get; set; }
        public int      Number { get; set; }
        public TKey     Key { get; set; }
        public TValue   Value { get; set; }
 
        public Node(TKey key, TValue value, int number)
        {
            this.Key = key;
            this.Value = value;
            this.Number = number;
        }
    }

    /**
     * @brief   GetRecursive
     *      分析：
     *          1，获取根节点
     *          2，比较bst[i]和key值：
     *              如果key大于bst[i]，则进入右子树
     *              如果key小于bst[i]，则进入左子树
     *              如果相等，返回
     *          3，返回错误
     *
     * @param   key：待查找键值
     *
     * @return  
     */
    public TValue GetUnRecursive(TKey key)
    {
        TValue          result = default(TValue);
        Node            node = root;

        while (null != node) {
            cmp = key.CompareTo(node.Key);
            if (cmp) {
                node = node.Right;
            } else if (cmp) {
                node = node.Left;
            } else {
                result = node.Value;
                break;
            }
        }

        return result;
    }

    public TValue Get(TKey key)
    {
        return GetRecursive(this.root, key); 
    }

    /**
     * @brief   GetRecursive :递归的遍历二叉树
     *
     * @param   root
     * @param   key
     *
     * @return  
     */
    public TValue GetRecursive(Node root, TKey key)
    {
        int         cmp;

        if (null == root) {
            return default(TValue);
        }

        cmp = key.CompareTo(root.Key);
        if (cmp > 0) {
            return GetRecursive(root.Right, key);
        } else if (cmp < 0) {
            return GetRecursive(root.Left, key);
        } else {
            return root.Value;
        }
    }

    public override void Put(TKey key, TValue value)
    {
        root = PutRecursive(this.root, key, value);
    }

    /**
     * @brief   PutRecursive :插入节点的递归算法实现
     *      步骤：
     *          1，如果节点为空，新建节点并插入当前位置，返回
     *          2，如果节点不为空，移动处理逻辑和查找一样
     *          3，最后更新每一个节点的Number的值
     *
     * @param   key
     * @param   value
     *
     * @return  
     */
    public Node PutRecursive(Node node, TKey key, TValue value)
    {
        int         cmp;

        if (null == node) {
            return new Node(key, value, 1);
        }

        cmp = key.CompareTo(node.Key);
        if (cmp < 0) {
            node.Left = PutRecursive(node.Left, key, value);
        } else {
            node.Right = PutRecursive(node.right, key, value);
        } else {
            node.Value = value;
        }

        node.Number = node.Left.Number + node.Right.Number + 1;
        return node;
    }

    /**
     * @brief   GetMax :获取BST的最大值
     *      分析：
     *          根据BST的特点，最大值==最右节点，最小值==最左节点
     *          1，对于任何一个节点，判断右子树是否存在：
     *              存在，进入右子树
     *              不存在，得到最大值
     *          PS：最小值的获取也是类似
     *
     * @return  
     */
    public Node GetMax(Node node)
    {
        while (null != node.Right) {
            node = node.Right;
        }

        return node;
    }

    public Node GetMin(Node node)
    {
        while (null != node.Left) {
            node = node.Left;
        }

        return node;
    }

    /**
     * @brief   Floor :查找Floor（所有比key小的数）中的最大值
     *      分析：
     *          要寻找比key小的最大值，使用查找方式，找到最右边的值
     *      步骤：
     *          1，对于任一节点，比较key和t[i]值：
     *          2，如果key小于t[i]，表示Floor值在左子树上，1步骤
     *          3，如果key大于t[i]，表示Floor值在右子树上
     *              获取右子树的Floor值，如果Floor为空，表示右子树上的
     *              所有节点都大于key，返回t[i]作为Floor值；
     *          4，等于，返回t[i]
     *      PS:
     *          同理，Ceiling也是类似方式
     *
     * @param   key
     *
     * @return  
     */
    public TKey Floor(TKey key)
    {
        Node            node = this.root;

        node = FloorRecursive(node, key);
        if (null != node) {
            return node.Key;
        } else {
            return default(TKey);
        }
    }

    public Node FloorRecursive(Node node, TKey key)
    {
        int         cmp;
        Node        right;

        if (null == node) {
            return null;
        }

        cmp = key.CompareTo(node.Key);
        if (cmp == 0) {
            return node;
        } else if (cmp < 0) {
            return FloorRecursive(node.Left, key);
        } else {
            right = FloorRecursive(node.Right, key);
            if (null == right) {
                return node;
            } else {
                return right;
            }
        }
    }

    public TKey Ceiling(Tkey key)
    {
        Node        node = this.root;

        node  = FloorCeiling(node, key);
        if (null == node) {
            return default(TKey);
        } else {
            return node.Key;
        }
    }

    public Node CeilingRecursive(Node node, TKey key)
    {
        int             cmp;
        Node            left;

        if (null == node) {
            return null;
        }

        cmp = key.CompareTo(node.Key);
        if (cmp == 0) {
            return node;
        } else if (cmp > 0) {
            return CeilingRecursive(node.Right, key);
        } else {
            left = CeilingRecursive(node.Left, key);
            if (null == left) {
                return node;
            } else {
                return left;
            }
        }
    }

    /**
     * @brief   Delete :删除某一个节点
     *      分析：
     *          1，如果节点没有孩子节点，将父节点的指针赋值为空即可；
     *          2，如果节点有一个孩子，用孩子节点替代当前节点即可；
     *          3，如果节点有多孩子：
     *              将右子树的最小节点替代当前节点
     *      步骤：
     *          1，对于任意一个节点，比较t[i]和key，获取待删除节点
     *          2，找到待删除节点i：
     *              若节点左子树为空，则直接用右子树替代当前节点
     *              若右子树为空，则直接用左子树替代当前节点；
     *              如果左右子树都不为空：
     *                  node == 右子树的最小值
     *                  替换
     *          3，更新相关节点的Number
     *      附加：
     *          随着删除的进行，整个二叉树会非常的不均衡
     *
     * @param   key
     *
     * @return  
     */
    public void Delete(TKey key)
    {
        this.root = DeleteRecursive(this.root, key);
    }

    public Node DeleteRecursive(Node node, TKey key) 
    {
        int                 cmp;
        Node                tmpNode;

        cmp = key.CompareTo(node.Key);
        if (cmp < 0) {
            node.Left = DeleteRecursive(node.Left, key);
        } else if (cmp > 0) {
            node.Right = DeleteRecursive(node.Right, key);
        } else {
            if (null == node.Left) {
                return node.Right;
            } else if (null == node.Right) {
                return node.Left;
            } else {
                tmpnode = node;
                node = GetMin(node.Right);
                node.Right = DeleteMin(tmpnode.Right);
                node.Left = tmpnode.Left;
            }
        }

        node.Number = node.Left.Number + node.Right.Number + 1;
        return node;
    }
}
