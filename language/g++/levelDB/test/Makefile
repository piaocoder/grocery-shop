CXX=g++

# 1,安装levelDB,首先转到tag v1.18下面
# 		make
# 		# 保证都是软连接
# 		mv libleveldb.* /usr/local/leveldb/lib/
# 		mv include/leveldb /usr/local/leveldb/include
# 2,添加文件搜索路径
# 		vim /etc/ld.so.conf
# 		ldconf
# 不知道为何，在centos中，/usr/local/lib/不在默认搜索路径下面
# 一旦指定了-L，必须同时指定-I，否则提示找不到
CFLAGS=-g -Wall  -I/usr/local/levelDB/include/
CXXFLAGS=-g -Wall  -I/usr/local/levelDB/include/ -I../
LDFLAGS=-L/usr/local/levelDB/lib/ -lleveldb

TARGET=leveldb-test
OBJS=../leveldb-opt.o leveldb-test.o

all:$(TARGET)

%.o: %.c
	$(CXX) $(CXXFLAGS) -c $^ $(LDFLAGS) -o $@

leveldb-test:$(OBJS)
	$(CXX) $^ $(LDFLAGS) -o $@

clean:
	rm -rf $(TARGET) *.o

