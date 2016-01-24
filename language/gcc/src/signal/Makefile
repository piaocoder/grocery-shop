CC=gcc

CFLAGS=-g -Wall 
LDFLAGS=-lpthread
TARGET=killTest signalMask

all:$(TARGET)

killTest:killTest.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

signalMask:signalMask.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm -rf $(TARGET) 

