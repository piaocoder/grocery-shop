/**
 * @file circularQueue.h
 * @brief 循环队列
 *          1，参数front/rear
 *          2，参数含义
 *              队列空时，rear==front
 *              队列满时，（rear+1)%maxsize == front
 * @author unlessbamboo@gmail.com
 * @version 1.0
 * @date 2016-11-15
 */

#ifndef _CIRCULARQUEUE_H_
#define _CIRCULARQUEUE_H_
typedef struct cqueue       QUEUE,*PQUEUE;
#define true 1
#define false 0
struct cqueue {
    int         *values;
    int          front;
    int          rear;
    int          maxsize;
};


int createQueue(PQUEUE Q, int maxsize);
void traverseQueue(PQUEUE Q);
int fullQueue(PQUEUE Q);
int emptyQueue(PQUEUE Q);
int cEnqueue(PQUEUE Q, int value);
int cDequeue(PQUEUE Q, int *rvalue);



#endif
