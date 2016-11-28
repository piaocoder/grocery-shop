#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "circularQueue.h"


#define QSIZE       10
#define QUIT        'q'
#define DQUEUE      'd'


int main(int argc, char **argv)
{
    PQUEUE          myq = NULL;
    char            input[100], output;
    int             newv;

    // 0 malloc
    myq = malloc(sizeof(QUEUE));
    if (NULL == myq) {
        perror("Malloc memory failed.");
        return -1;
    }

    // 1 创建循环队列，大小为10
    if (createQueue(myq, QSIZE) < 0) {
        perror("Malloc memory failed.");
        return -1;
    }

    // 2 根据输入数据，进行入队列操作
    do {
        printf("Enqueue, Please input new values: ");
        fgets((char*)input, 100, stdin);
        if  (!strncmp(input, "quit", strlen("quit"))) {
            break;
        }

        if (cEnqueue(myq, atoi(input)) < 0) {
            printf("Enqueue failed, sorry.");
            return -1;
        }

        traverseQueue(myq);
    } while(true);

    // 4 根据输入逻辑，判断是否持续的进行出对列操作，如果为空，退出
    do {
        printf("Whether going to dequeue?(Y/N): ");
        output = getchar();
        if (output == 'y' || output == 'Y') {
            if (cDequeue(myq, &newv) < 0) {
                break;
            }
            printf("Dequeue one element.\n");
            traverseQueue(myq);
        } else {
            break;
        }

        while (getchar() != '\n')
            continue;
    } while(true);
    
    return 0;
    
}
