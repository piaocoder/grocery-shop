#include <stdio.h>
#include "avltree.h"
 
int main()
{
    node *t , *p;
    int i;
    int j = 0;
    const int max = 10;
 
    printf("--- C AVL Tree Demo  ---\n");
 
    t = NULL;
 
    printf("Insert: ");
    for( i = 0; i < max; i++, j = ( j + 7 ) % max )
    {
 
        t = insert( j, t );
        printf("%d ",j);
 
    }
    printf(" into the tree\n\n");
 
    display_avl(t);
 
    dispose(t);
 
    return 0;
}
