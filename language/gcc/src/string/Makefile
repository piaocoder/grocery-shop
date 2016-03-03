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
LDFLAGS+=-lcrypto -L/usr/local/libev/lib/ -lev

TARGET=string-escape string-int-test \
	   string-strtok string-phase \
	   string-trim string-zero 

all:$(TARGET)

string-escape:string-escape.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

string-int-test:string-int-test.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

string-phase:string-phase.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

string-strtok:string-strtok.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

string-trim:string-trim.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

string-zero:string-zero.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm $(TARGET) -rf

install:
	cp $(TARGET) $(BO_BINS_DIR)
