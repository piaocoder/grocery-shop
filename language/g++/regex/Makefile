
CXXFLAGS=-g -Wall
LDFLAGS+=-lpcre

TARGET=regex-second

all:$(TARGET)

regex-second:regex-second.cpp
	$(CXX) $(CXXFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm $(TARGET) -rf

install:
	cp $(TARGET) $(BO_BINS_DIR)
