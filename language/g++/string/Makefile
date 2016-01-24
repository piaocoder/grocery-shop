CXX=g++

CFLAGS=-g -Wall 
LDFLAGS=-lpthread
TARGET= trim

all:$(TARGET)

trim:trim.cpp
	$(CXX) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm -rf $(TARGET) 

