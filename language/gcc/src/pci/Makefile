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
LDFLAGS+=-L/usr/local/libev/lib/ -lev
TARGET=pci-msgq-send pci-pipi

all:$(TARGET)

pci-msgq-send:pci-msgq-send.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

pci-pipi:pci-pipi.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm $(TARGET) -rf

install:
	cp $(TARGET) $(BO_BINS_DIR)
