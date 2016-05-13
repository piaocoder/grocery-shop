#
#
#	bo gcc 2.0
#		更改代码目录结构
#
# 	2016年 03月 02日 星期三 11:37:55 CST
#
include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

LDFLAGS+=-lpcre

TARGET=regex-pcre regex-test regex-second

all:$(TARGET)

regex-pcre:regex-pcre.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

regex-second:regex-second.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

regex-test:regex-test.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm $(TARGET) -rf

install:
	cp $(TARGET) $(BO_BINS_DIR)
