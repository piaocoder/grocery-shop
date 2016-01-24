CC=gcc
CFLAGS=-g -Wall

TARGET=simple_regex simple_pcre
LDFLAGS=/usr/local/libev/lib/libev.a -lpthread -L/usr/local/pcre/lib/ -lpcre
CFLAGS=-g -Wall -I/usr/local/pcre/include/

all:$(TARGET)

simple_regex:simple_regex.c
	$(CC) $(CFLAGS) $^  $(LDFLAGS) -o $@

simple_pcre:simple_pcre.c
	$(CC) $(CFLAGS) $^  $(LDFLAGS) -o $@

clean:
	rm *.o $(TARGET) -rf
