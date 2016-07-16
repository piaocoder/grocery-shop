#
#
#	bo gcc 2.0
#		更改代码目录结构
#
# 	2016年 03月 02日 星期三 11:37:55 CST
#
include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

CFLAGS+=-I/usr/local/libev/include/
LDFLAGS+=-lcrypto -L/usr/local/libev/lib/ -lev -lpthread

OBJS=thpool.o
TARGET=socket-client socket-server \
	   socket-noudp-client socket-noudp-server \
	   socket-unix-client socket-unix-server \
	   socket-unix-system \
	   socket-noudp-mul-server socket-noudp-mul-client

all:$(OBJS) $(TARGET)

%.o: %.c
	$(CC) -c $(CFLAGS) $^ $(LDFLAGS) -o $@

socket-client:socket-client.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

socket-server:socket-server.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

socket-noudp-server:socket-noudp-server.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

socket-noudp-client:socket-noudp-client.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

socket-unix-client:socket-unix-client.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

socket-unix-server:socket-unix-server.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

socket-unix-system:socket-unix-system.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

socket-noudp-mul-server:socket-noudp-mul-server.c
	$(CC) $(CFLAGS) $^ $(OBJS) $(LDFLAGS) -o $@

socket-noudp-mul-client:socket-noudp-mul-client.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm $(TARGET) *.o -rf

install:
	cp $(TARGET) $(BO_BINS_DIR)
