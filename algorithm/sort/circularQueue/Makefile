#
#
#	bo gcc 1.0
#	src directory
#
#


CFLAGS=-g -ggdb3 -Wall
LDFLAGS=
CC=gcc


TARGET= test

all:$(TARGET)

circularQueue.o:circularQueue.c
	$(CC) -c $(CFLAGS) $^ -o $@

test:test.c circularQueue.o
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm -rf $(TARGET) 
