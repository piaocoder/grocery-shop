#CC=/usr/local/gccgraph/bin/gcc
CC=gcc
CFLAGS=-g -Wall
TARGETS=configIO.o scanfIO printfIO

all:$(TARGETS)

configIO.o:configIO.c
	$(CC) -c $(CFLAGS) $^ -o $@

scanfIO:scanfIO.c
	$(CC) $(CFLAGS) $^ configIO.o -o $@

printfIO:printfIO.c
	$(CC) $(CFLAGS) $^ configIO.o -o $@

clean:
	rm *.o $(TARGETS) -rf
