CC=gcc
CFLAGS=-g -Wall

TARGET=simple_python
LDFLAGS=/usr/local/libev/lib/libev.a -lpthread -lpython2.7
CFLAGS=-g -Wall -I/usr/local/libev/include/ -I/usr/include/python2.7/

all:$(TARGET)

simple_python:simple_python.c
	$(CC) $(CFLAGS) $^  $(LDFLAGS) -o $@

clean:
	rm *.o $(TARGET) -rf
