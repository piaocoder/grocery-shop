#
#
#	bo gcc 2.0
#		更改代码目录结构
#
# 	2016年 03月 02日 星期三 11:37:55 CST
#
include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

TARGET=ev-time.o ev-break ev-multiple ev-periodic \
	   ev-server-socket

CFLAGS+=-I/usr/local/libev/include/
LDFLAGS+=-L/usr/local/libev/lib/ -lev

all:$(TARGET)

ev-time.o:ev-time.c
	$(CC) -c $(CFLAGS) $^ $(LDFLAGS) -o $@

ev-break:ev-break.c
	$(CC) $(CFLAGS) $^ ev-time.o $(LDFLAGS) -o $@

ev-multiple:ev-multiple.c
	$(CC) $(CFLAGS) $^ ev-time.o $(LDFLAGS) -o $@

ev-periodic:ev-periodic.c
	$(CC) $(CFLAGS) $^ ev-time.o $(LDFLAGS) -o $@

ev-server-socket:ev-server-socket.c
	$(CC) $(CFLAGS) $^ ev-time.o $(LDFLAGS) -o $@

clean:
	rm $(TARGET) -rf

install:
	cp $(TARGET) $(BO_BINS_DIR)
