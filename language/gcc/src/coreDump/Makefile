CC=gcc
CFLAGS=-g -ggdb -Wall

all:exe

exe:example.c
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm *.o exe -rf
