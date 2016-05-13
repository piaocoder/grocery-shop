
CXXFLAGS=-g -Wall
LDFLAGS+=-lpthread

SERVEROBJS=timer-manager.o timer-test.o
TARGET=timer-test

all:$(TARGET)

%.o:%.cpp
	$(CXX) -c $(CXXFLAGS) $^ $(LDFLAGS) -o $@

timer-test:$(SERVEROBJS)
	$(CXX) $(CXXFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm $(TARGET) -rf

install:
