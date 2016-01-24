CC=gcc

CFLAGS=-g -Wall 
LDFLAGS=-lpthread
TARGET=killTest test testNull

all:$(TARGET)

killTest:killTest.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

test:test.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

testNull:testNull.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	cd ..; ls -l
	rm -rf $(TARGET) 

