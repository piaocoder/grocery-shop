CXX=g++

CXXFLAGS=-g -Wall 
LDFLAGS=-lpthread
TARGET=pair-test

all:$(TARGET)

pair-test:pair-test.cpp
	$(CXX) $(CXXFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm -rf $(TARGET) 

