CC=gcc
CFLAGS=-g -Wall
OBJECTS=trim

all:$(OBJECTS)

trim:trim.c
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm *.o $(OBJECTS) -rf
