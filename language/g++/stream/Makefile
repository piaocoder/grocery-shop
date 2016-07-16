CXX=g++

CXXFLAGS=-g -Wall --std=c++11
LDFLAGS=-lpthread
TARGET= ofstreamTest

all:$(TARGET)

ofstreamTest:ofstreamTest.cpp
	$(CXX) $(CXXFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm -rf $(TARGET) 

