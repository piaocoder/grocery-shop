#
#
#	bo gcc 2.0
#		更改代码目录结构
#
# 	2016年 03月 02日 星期三 11:37:55 CST
#
include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

TARGET=signal-kill signal-mask signal-null-test

all:$(TARGET)

signal-kill:signal-kill.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

signal-mask:signal-mask.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

signal-null-test:signal-null-test.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm $(TARGET) -rf

install:
	cp $(TARGET) $(BO_BINS_DIR)
