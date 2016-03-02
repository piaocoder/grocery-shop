CC=gcc
CFLAGS=-g -Wall -I/usr/local/libev/include/
TARGETS=pipe
LDFLAGS=-L/usr/local/libev/lib/ -lev

all:$(TARGETS)

pipe:pipe.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm *.o $(TARGETS) -rf
