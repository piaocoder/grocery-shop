#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

int func(int *array, int m, int n) 
{
    int i,j;

    for(i=0;i<m;i++) {
        for(j=0;j<n;j++)
            printf("\t%d", *(array +i*n +j));
        printf("\n");
    }
    return 0;
}

int func2(int **array, int m) 
{
    printf("Func2\n");

    return 0;
}

int func1(int **array, int m, int n) {
    printf("---\n");
    return 0;
}

int one_dimension(const int array[], int m)
{
    int         i = 0;

    for (i=0; i<m; i++) {
        printf("array[%d]=%d ", i, array[i]);
    }
    printf("\n");

    return 0;
}

int
array_test_sizeof()
{
    int     array[12];

    printf("测试12个元素的整型数组的sizeof值：%lu\n", sizeof(array));

    return 0;
}

int main(int argc,char** argv) {
    int m=3,n=3;
    int array[][3] = {{1,2,3},{4,5,6},{7,9,9}};
    int one[] = {4, 8, 9, 10};
    int **p = NULL;

    // 1
    func(array[0], m, n);

    // 2
    //func1(array, m, n);
    
    //3
    one_dimension(one, 4);
    
    //4 
    p = (int **)array;
    printf("xxxxxxxxxxxxxxxx\n");
    **p = 4;
    printf("xxxxxxxxxxxxxxxx\n");
    //func2(p, n);
    
    // 5
    array_test_sizeof();
   
    return 0;
}
