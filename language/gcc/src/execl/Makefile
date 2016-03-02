#
#
#	bo gcc 2.0
#		更改代码目录结构
#
# 	2016年 03月 02日 星期三 11:37:55 CST
#
include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

TARGET=execl-test

all:$(TARGET)

execl-test:execl-test.c
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm $(TARGET) -rf

install:
	cp $(TARGET) $(BO_BINS_DIR)
