CXX=g++

CXXFLAGS=-g -Wall --std=c++11
LDFLAGS=-lpthread
TARGET=multiTest

all:$(TARGET)

multiTest:multiTest.cpp
	$(CXX) $(CXXFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm -rf $(TARGET) 

