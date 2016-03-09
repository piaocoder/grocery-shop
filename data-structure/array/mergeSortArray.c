#include <stdio.h>
#include <string.h>


/**
 * @brief   mergeUnrecursiveArray 
 *      分析：
 *          1，保证array1有足够的空间进行存储，因为最后的空间是固定的，
 *              所以从尾部开始往前进行合并，算法和memcpy的算法非常像
 *          2，初始化
 *              index1 = len1 - 1;
 *              index2 = len2 - 1;
 *              result = len1 + len2 - 1;
 *          3，合并
 *              while (index1>=0 && index2>=0):
 *                  if (array1[index1] > array2[index2])
 *                      array1[result--] = array1[index1--];
 *                  else
 *                      array1[result--] = array2[index2--];
 *          4，merge remain values
 *              if (index1>=0) 无需关注
 *              else:
 *                  while (index2>=0)
 *                      array1[result--] = array2[index2--];
 *
 *
 * @param   array1[]
 * @param   len1
 * @param   array2[]
 * @param   len2
 */
void mergeUnrecursiveArray(int array1[], int len1, int array2[], int len2)
{
    int             index1, index2, result;
    
    index1 = len1 - 1;
    index2 = len2 - 1;
    result = len1 + len2 - 1;

    // marge
    while (index1 >= 0 && index2 >= 0) {
        if (array1[index1] > array2[index2]) {
            array1[result--] = array1[index1--];
        } else {
            array1[result--] = array2[index2--];
        }
    }

    // merge remain values
    while (index2 >= 0) {
        array1[result--] = array2[index2--];
    }
}
