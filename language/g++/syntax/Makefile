#
#
#	log-analysis server 1.0
#
#

CXX=g++
CXXFLAGS=-g -Wall -std=c++11
LDFLAGS=-pthread

TARGET=scope

all:$(TARGET)


$(TARGET):scope.cpp
	$(CXX) $(CXXFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm *.o *.a *.so $(TARGET) $(LIBTARGET) -rf

install:
	echo "Nothing*********************"

