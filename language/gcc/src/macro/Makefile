#
#
#	bo gcc 2.0
#		更改代码目录结构
#
# 	2016年 03月 02日 星期三 11:37:55 CST
#
include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

TARGET=macro-test macro-args

all:$(TARGET)

macro-test:macro-test.c
	$(CC) $(CFLAGS) $^  $(LDFLAGS) -o $@

macro-args:macro-args.c
	$(CC) $(CFLAGS) $^  $(LDFLAGS) -o $@

clean:
	rm $(TARGET) -rf

install:
	cp $(TARGET) $(BO_BINS_DIR)
