CC=gcc

CFLAGS=-g -Wall 
LDFLAGS=-lpthread
TARGET= test array init

all:$(TARGET)

array:array.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

test:test.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

init:init.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

testNull:testNull.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm -rf $(TARGET) 

