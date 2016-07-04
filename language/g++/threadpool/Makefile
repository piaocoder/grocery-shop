#
#
#	log-analysis server 1.0
#
#

CXX=g++
CXXFLAGS=-g -Wall -std=c++0x ThreadPool.h
LDFLAGS=-pthread

TARGET=example

all:$(TARGET)


$(TARGET):example.cpp
	$(CXX) $(CXXFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm *.o *.a *.so $(TARGET) $(LIBTARGET) -rf

install:
	echo "Nothing*********************"

