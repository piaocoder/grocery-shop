#ifndef STACK_H_INCLUDED
#define STACK_H_INCLUDED
#include "common.h"

typedef void*  StackItem;
typedef struct stack_lst stack_lst_t;
typedef struct stack_lst_node stack_lst_node_t;

struct stack_lst_node {
	StackItem         item;				/** The data of this node. **/
	stack_lst_node_t *next;		/** The next node (the one below the top). **/
};

struct stack_lst {
	int count; 	/** The number of items in the stack. **/
	stack_lst_node_t *top;	/** The top item of the stack. **/
};


stack_lst_t *stack_create();
void stack_destroy(stack_lst_t *stack);
void stack_clean(stack_lst_t *stack);
bool stack_is_empty(stack_lst_t *stack);
int stack_size(stack_lst_t *stack);
StackItem stack_top(stack_lst_t *stack);
bool stack_push(stack_lst_t *stack, StackItem item);
StackItem stack_pop(stack_lst_t *stack);

#endif
