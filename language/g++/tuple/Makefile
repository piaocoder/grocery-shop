CXX=g++

CXXFLAGS=-g -Wall --std=c++11
LDFLAGS=-lpthread
TARGET=simpletest

all:$(TARGET)

simpletest:simpletest.cpp
	$(CXX) $(CXXFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm -rf $(TARGET) 

