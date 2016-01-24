CC=gcc

CFLAGS=-g -Wall 
LDFLAGS=-lpthread
TARGET= variable_struct

all:$(TARGET)

variable_struct:variable_struct.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm -rf $(TARGET) 

