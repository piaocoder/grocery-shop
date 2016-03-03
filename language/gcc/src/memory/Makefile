#
#
#	bo gcc 2.0
#		更改代码目录结构
#
# 	2016年 03月 02日 星期三 11:37:55 CST
#
include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

LDFLAGS+=-lcrypto 

TARGET=memory-example memory-compilate memory-distribute

all:$(TARGET)

memory-example:memory-example.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

memory-compilate:memory-compilate.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

memory-distribute:memory-distribute.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm $(TARGET) -rf

install:
	cp $(TARGET) $(BO_BINS_DIR)
