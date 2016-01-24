CC=gcc

CFLAGS=-g -Wall 
LDFLAGS=-lpthread
TARGET=killTest test execTest

all:$(TARGET)

execTest:execTest.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

killTest:killTest.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

test:test.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm -rf $(TARGET) 

