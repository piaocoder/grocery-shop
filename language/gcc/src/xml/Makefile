CC=gcc
CFLAGS=-g -Wall -I/usr/local/libxml2/include/libxml2/
LDFLAGS=-L/usr/local/libxml2/lib/ -lxml2
TARGETS=link
all:$(TARGETS)

link:link.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm *.o $(TARGETS) -rf
