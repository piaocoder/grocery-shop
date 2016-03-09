CC=gcc
CFLAGS=-g -Wall
#TARGETS=generic_list_test list_test
TARGETS=list_test

CFLAGS+=./list.h

all:$(TARGETS)

generic_list_test:generic_list_test.c
	$(CC) $(CFLAGS) $^ -o $@

list_test:list_test.c
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm *.o $(TARGETS) -rf
