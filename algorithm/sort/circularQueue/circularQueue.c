#include <stdio.h>
#include <stdlib.h>

#include "circularQueue.h"


int createQueue(PQUEUE Q, int maxsize)
{
    Q->values = (int*)malloc(sizeof(int)*maxsize); 
    if (NULL == Q->values) {
        return -1;
    }
    Q->front = Q->rear = 0;
    Q->maxsize = maxsize;
    return 0;
}


void traverseQueue(PQUEUE Q)
{
    int   i = Q->front;

    printf("Display queue values:\n");
    while (i%Q->maxsize != Q->rear) {
        printf("%d ", Q->values[i]);
        i++;
    }
    printf("\n");
}


int fullQueue(PQUEUE Q)
{
    return Q->front == (Q->rear+1)%Q->maxsize ? true : false;
}


int emptyQueue(PQUEUE Q)
{
    return Q->front == Q->rear ? true : false;
}


int cEnqueue(PQUEUE Q, int value)
{
    if (fullQueue(Q)) {
        return false;
    } else {
        Q->values[Q->rear] = value;
        Q->rear = (Q->rear+1)%Q->maxsize;
        return true;
    }
}


int cDequeue(PQUEUE Q, int *value)
{
    if (emptyQueue(Q)) {
        return false;
    } else {
        *value = Q->values[Q->front];
        Q->front = (Q->front+1)%Q->maxsize;
        return true;
    }
}
