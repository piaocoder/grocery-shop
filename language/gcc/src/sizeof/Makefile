CC=gcc

CFLAGS=-g -Wall 
LDFLAGS=-lpthread
TARGET= test array

all:$(TARGET)

array:array.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

test:test.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

testNull:testNull.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm -rf $(TARGET) 

