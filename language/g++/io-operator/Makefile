CXX=g++

CFLAGS=-g -Wall 
LDFLAGS=-lpthread
TARGET= mmap-test

all:$(TARGET)

mmap-test:mmap-test.cpp
	$(CXX) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm -rf $(TARGET) 

