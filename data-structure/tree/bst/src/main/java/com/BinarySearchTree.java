package com;

import java.util.Iterator;
import java.util.NoSuchElementException;
import com.Queue;
import com.StdIn;
import com.StdOut;

/**
 * @file BinarySearchTree.java
 * @brief   二叉查找树的相关操作纪要
 *          2016-2-23:OH,SHIT,居然是C#代码，难怪看不懂
 * @author unlessbamboo
 * @version 1.0
 * @date 2016-02-22
 */


/**
 * @brief  ：泛型类子类
 *      1，<T>表示泛型参数，例如Map<key, value>,C++的知识好久没接触了....
 *      2，与泛型方法类似，泛型类的类型参数声明可以包含多个参数，逗号隔开
 *      3，
 */
public class BinarySearchTree<TKey extends Comparable<TKey>, TValue>
{
    private Node root;

    private class Node
    {
        public Node     left;
        public Node     right;
        public int      number;
        public TKey     key;
        public TValue   value;
 
        public Node(TKey key, TValue value, int number)
        {
            key = key;
            value = value;
            number = number;
        }
    }

    public BinarySearchTree() 
    {
        // nothing
    }

    /**
     * @brief   size :获取树节点数量
     *
     * @return  
     */
    public int size() 
    {
        return size(root);
    }
    private int size(Node node)
    {
        if (null == node) {
            return 0;
        } else {
            return node.number;
        }
    }


    public boolean isEmpty()
    {
        return size() == 0;
    }

    public boolean contains(TKey key) 
    {
        if (null == key) {
            throw new NullPointerException("Argumen to contains() is null.");
        }

        return get(key) != null;
    }



    /**
     * @brief   getRecursive
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
    private TValue getUnRecursive(Node node, TKey key)
    {
        int         cmp;
        TValue      result = null;

        while (null != node) {
            cmp = key.compareTo(node.key);
            if (cmp > 0) {
                node = node.right;
            } else if (cmp < 0) {
                node = node.left;
            } else {
                result = node.value;
                break;
            }
        }

        if (null == node) {
            return null; 
        } else {
            return result;
        }
    }

    public TValue get(TKey key)
    {
        return getRecursive(root, key); 
        //return getUnRecursive(root, key); 
    }

    /**
     * Return the number of keys in the symbol table strictly less than <tt>key</tt>.
     *
     * @param  key the key
     * @return the number of keys in the symbol table strictly less than <tt>key</tt>
     * @throws NullPointerException if <tt>key</tt> is <tt>null</tt>
     */
    public int rank(TKey key) 
    {
        if (key == null) {
            throw new NullPointerException("argument to rank() is null");
        }
        return rank(key, root);
    } 

    // Number of keys in the subtree less than key.
    private int rank(TKey key, Node x) 
    {
        int             cmp;

        if (x == null) {
            return 0; 
        }
        cmp = key.compareTo(x.key); 

        if (cmp < 0) {
            return rank(key, x.left); 
        } else if (cmp > 0) {
            return 1 + size(x.left) + rank(key, x.right); 
        } else {              
            return size(x.left); 
        }
    } 

     /**
     * Returns the keys in the BinarySearchTree in level order (for debugging).
     *
     * @return the keys in the BinarySearchTree in level order traversal
     */
    public Iterable<TKey> levelOrder() 
    {
        Queue<String> qQueue = new Queue<String>();
        Queue<TKey> keyQueue = new Queue<TKey>();
        Queue<Node> queue = new Queue<Node>();

        queue.enqueue(root);
        while (!queue.isEmpty()) {
            Node x = queue.dequeue();
            if (x == null) continue;
            keyQueue.enqueue(x.key);
            queue.enqueue(x.left);
            queue.enqueue(x.right);
        }
        return keyQueue;
    }

    /**
     * @brief   getRecursive :递归的遍历二叉树
     *
     * @param   root
     * @param   key
     *
     * @return  
     */
    private TValue getRecursive(Node node, TKey key)
    {
        int         cmp;

        if (null == node) {
            return null;
        }

        cmp = key.compareTo(node.key);
        if (cmp > 0) {
            return getRecursive(node.right, key);
        } else if (cmp < 0) {
            return getRecursive(node.left, key);
        } else {
            return node.value;
        }
    }

    public void put(TKey key, TValue value)
    {
        if (null == key) {
            throw new NullPointerException("first argument to put() is null");
        }
        if (null == value) {
            delete(key);
            return;
        }

        root = putRecursive(root, key, value);
        assert check();
    }

    /**
     * @brief   putRecursive :插入节点的递归算法实现
     *      步骤：
     *          1，如果节点为空，新建节点并插入当前位置，返回
     *          2，如果节点不为空，移动处理逻辑和查找一样
     *          3，最后更新每一个节点的number的值
     *
     * @param   key
     * @param   value
     *
     * @return  
     */
    private Node putRecursive(Node node, TKey key, TValue value)
    {
        int         cmp;

        if (null == node) {
            return new Node(key, value, 1);
        }

        cmp = key.compareTo(node.key);
        if (cmp < 0) {
            node.left = putRecursive(node.left, key, value);
        } else if (cmp > 0) {
            node.right = putRecursive(node.right, key, value);
        } else {
            node.value = value;
        }

        node.number = node.left.number + node.right.number + 1;
        return node;
    }

    /**
     * @brief   getMax :获取BinarySearchTree的最大值
     *      分析：
     *          根据BinarySearchTree的特点，最大值==最右节点，最小值==最左节点
     *          1，对于任何一个节点，判断右子树是否存在：
     *              存在，进入右子树
     *              不存在，得到最大值
     *          PS：最小值的获取也是类似
     *
     * @return  
     */
    public Node getMax()
    {
        if (isEmpty()) {
           throw new NoSuchElementException(
                   "called Max() with empty symbol table");
        }
        return getMax(root);
    }
    private Node getMax(Node node)
    {
        while (null != node.right) {
            node = node.right;
        }

        return node;
    }

    /**
     * @brief   getMin :获取最小值
     *
     * @return  
     */
    public Node getMin()
    {
        if (isEmpty()) {
           throw new NoSuchElementException(
                   "called min() with empty symbol table");
        }
        return getMin(root);
    }
    private Node getMin(Node node)
    {
        while (null != node.left) {
            node = node.left;
        }

        return node;
    }

    /**
     * @brief   floor :查找floor（所有比key小的数）中的最大值
     *      分析：
     *          要寻找比key小的最大值，使用查找方式，找到最右边的值
     *      步骤：
     *          1，对于任一节点，比较key和t[i]值：
     *          2，如果key小于t[i]，表示floor值在左子树上，1步骤
     *          3，如果key大于t[i]，表示floor值在右子树上
     *              获取右子树的floor值，如果floor为空，表示右子树上的
     *              所有节点都大于key，返回t[i]作为floor值；
     *          4，等于，返回t[i]
     *      PS:
     *          同理，ceiling也是类似方式（获取比key大）中最小值
     *
     * @param   key
     *
     * @return  
     */
    public TKey floor(TKey key)
    {
        Node            node = root;

        if (null == key) {
            throw new NullPointerException("argument to floor() is null");
        }
        if (isEmpty()) {
            throw new NoSuchElementException(
                    "called floor() with empty symbol table");
        }

        node = floorRecursive(node, key);
        if (null != node) {
            return node.key;
        } else {
            return null;
        }
    }
    private Node floorRecursive(Node node, TKey key)
    {
        int         cmp;
        Node        right;

        if (null == node) {
            return null;
        }

        cmp = key.compareTo(node.key);
        if (cmp == 0) {
            return node;
        } else if (cmp < 0) {
            return floorRecursive(node.left, key);
        } else {
            right = floorRecursive(node.right, key);
            if (null == right) {
                return node;
            } else {
                return right;
            }
        }
    }

    public TKey ceiling(TKey key)
    {
        Node        node = root;

        if (null == key) {
            throw new NullPointerException("argument to floor() is null");
        }
        if (isEmpty()) {
            throw new NoSuchElementException(
                    "called floor() with empty symbol table");
        }

        node  = ceilingRecursive(node, key);
        if (null == node) {
            return null;
        } else {
            return node.key;
        }
    }
    private Node ceilingRecursive(Node node, TKey key)
    {
        int             cmp;
        Node            left;

        if (null == node) {
            return null;
        }

        cmp = key.compareTo(node.key);
        if (cmp == 0) {
            return node;
        } else if (cmp > 0) {
            return ceilingRecursive(node.right, key);
        } else {
            left = ceilingRecursive(node.left, key);
            if (null == left) {
                return node;
            } else {
                return left;
            }
        }
    }

    /**
     * @brief   delete :删除某一个节点
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
     *          3，更新相关节点的number
     *      附加：
     *          随着删除的进行，整个二叉树会非常的不均衡
     *
     * @param   key
     *
     * @return  
     */
    public void delete(TKey key)
    {
        if (null == key) {
            throw new NullPointerException("argument to delete() is null");
        }
        root = deleteRecursive(root, key);
        assert check();
    }
    private Node deleteRecursive(Node node, TKey key) 
    {
        int                 cmp;
        Node                tmpNode;

        cmp = key.compareTo(node.key);
        if (cmp < 0) {
            node.left = deleteRecursive(node.left, key);
        } else if (cmp > 0) {
            node.right = deleteRecursive(node.right, key);
        } else {
            if (null == node.left) {
                return node.right;
            } else if (null == node.right) {
                return node.left;
            } else {
                tmpNode = node;
                node = getMin(node.right);
                node.right = deleteMin(tmpNode.right);
                node.left = tmpNode.left;
            }
        }

        node.number = node.left.number + node.right.number + 1;
        return node;
    }

    /**
     * @brief   deleteMin :删除最小节点，找到最左边的节点
     *
     * @return  
     */
    public void deleteMin() 
    {
        if (isEmpty()) {
            throw new NoSuchElementException("Symbol table underflow");
        }
        root = deleteMin(root);
        assert check();
    }
    private Node deleteMin(Node node)
    {
        if (node.left == null) {
            return node.right;
        }
        node.left = deleteMin(node.left);
        node.number = size(node.left) + size(node.right) + 1;
        return node;
    }


    /**
     * @brief   deleteMax :删除最大节点，找到最由边的节点
     *
     * @return  
     */
    public void deleteMax() 
    {
        if (isEmpty()) {
            throw new NoSuchElementException("Symbol table underflow");
        }
        root = deleteMax(root);
        assert check();
    }
    private Node deleteMax(Node node)
    {
        if (node.right == null) {
            return node.left;
        }
        node.right = deleteMax(node.right);
        node.number = size(node.left) + size(node.right) + 1;
        return node;
    }

    /**
     * @brief   keys :将树中所有Keys存入符号表（迭代器）中返回
     *          队列哦！
     *
     * @return  
     */
    public Iterable<TKey> keys()
    {
        return keys(getMin().key, getMax().key);
    }
    private Iterable<TKey> keys(TKey lo, TKey hi)
    {
        Queue<TKey>         queue = new Queue<TKey> ();

        if (null == lo) {
            throw new NullPointerException("Low argument to keys() is null");
        }
        if (null == hi) {
            throw new NullPointerException("High argument to keys() is null");
        }

        keys(root, queue, lo, hi);
        return queue;
    }
    private void keys(Node x, Queue<TKey> queue, TKey lo, TKey hi) 
    { 
        if (x == null) return; 
        int cmplo = lo.compareTo(x.key); 
        int cmphi = hi.compareTo(x.key); 
        if (cmplo < 0) keys(x.left, queue, lo, hi); 
        if (cmplo <= 0 && cmphi >= 0) queue.enqueue(x.key); 
        if (cmphi > 0) keys(x.right, queue, lo, hi); 
    } 

    /**
     * @brief   height :返回树的高度
     *
     * @return  
     */
    public int height()
    {
        return height(root);
    }
    private int height(Node node)
    {
        if (null == node) {
            return -1;
        }
        return Math.max(height(node.left), height(node.right)) + 1;
    }

    /**
     * @brief   check :验证BinarySearchTree树结构
     *
     * @return  
     */
    private boolean check()
    {
        if (!isBst()) {
            System.out.println("Not in symmetric order");
        }
        if (!isSizeConsistent()) {
            System.out.println("Subtree counts not consistent");
        }
        if (!isRankConsistent()) {
            System.out.println("Ranks not consistent");
        }

        return isBst() && isSizeConsistent() && isRankConsistent();
    }
    
    /**
     * @brief   isBst ：验证是否为一颗BinarySearchTree
     *
     * @return  
     */
    public boolean isBst()
    {
        return isBst(root, null, null);
    }
    private boolean isBst(Node node, TKey min, TKey max)
    {
        if (null == node) {
            return true;
        }

        if (min != null && node.key.compareTo(min) <= 0) {
            return false;
        }
        if (max != null && node.key.compareTo(max) >= 0) {
            return false;
        }
        return isBst(node.left, min, node.key) && isBst(node.right, node.key, max);
    }

    // are the size fields correct?
    private boolean isSizeConsistent() { return isSizeConsistent(root); }
    private boolean isSizeConsistent(Node x) {
        if (x == null) return true;
        if (x.number != size(x.left) + size(x.right) + 1) return false;
        return isSizeConsistent(x.left) && isSizeConsistent(x.right);
    } 

    // check that ranks are consistent
    private boolean isRankConsistent() {
        for (int i = 0; i < size(); i++)
            if (i != rank(select(i))) return false;
        for (TKey key : keys())
            if (key.compareTo(select(rank(key))) != 0) return false;
        return true;
    }

    /**
     * Return the kth smallest key in the symbol table.
     *
     * @param  k the order statistic
     * @return the kth smallest key in the symbol table
     * @throws IllegalArgumentException unless <tt>k</tt> is between 0 and
     *        <em>N</em> &minus; 1
     */
    public TKey select(int k) {
        if (k < 0 || k >= size()) {
            throw new IllegalArgumentException();
        }
        Node x = select(root, k);
        return x.key;
    }

    // Return key of rank k. 
    private Node select(Node x, int k) {
        if (x == null) {
            return null; 
        }
        int t = size(x.left); 

        if (t > k) {
            return select(x.left,  k); 
        } else if (t < k) {
            return select(x.right, k-t-1); 
        } else {            
            return x; 
        }
    } 

     /**
     * Unit tests the <tt>BinarySearchTree</tt> data type.
     */
    public static void main(String[] args) { 
        BinarySearchTree<String, Integer> st = new BinarySearchTree<String, Integer>();
        for (int i = 0; !StdIn.isEmpty(); i++) {
            String key = StdIn.readString();
            st.put(key, i);
        }

        for (String s : st.levelOrder())
            StdOut.println(s + " " + st.get(s));

        StdOut.println();

        for (String s : st.keys())
            StdOut.println(s + " " + st.get(s));
    }
}
