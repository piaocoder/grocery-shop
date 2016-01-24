CC=gcc
CFLAGS=-g -Wall
LDFLAGS=-lcrypto -lm
TARGETS=md5

all:$(TARGETS)

md5.o:md5.c
	$(CC) $(CFLAGS) -c $^ $(LDFLAGS) -o $@

clean:
	rm *.o $(TARGETS) -rf
