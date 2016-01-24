CC=gcc

CFLAGS=-g -Wall 
LDFLAGS=-lpthread
TARGET=object.o daemonTest test

all:$(TARGET)

object.o:object.c
	$(CC) $(CFLAGS) -c $^ $(LDFLAGS) -o $@

daemonTest:daemonTest.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

test:test.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) object.o -o $@

clean:
	rm -rf $(TARGET) 

