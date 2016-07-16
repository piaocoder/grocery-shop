
CXXFLAGS=-g -Wall -std=c++11
LDFLAGS=

TARGET=jsoncpp-test
objs=jsoncpp.o jsoncpp-test.o

all:$(objs) $(TARGET)

%.o:%.cpp
	$(CXX) -c $(CXXFLAGS) $^ $(LDFLAGS) -o $@

jsoncpp-test:jsoncpp-test.o jsoncpp.o
	$(CXX) $^ $(LDFLAGS) -o $@

clean:
	rm $(TARGET) -rf

install:
	cp $(TARGET) $(BO_BINS_DIR)
