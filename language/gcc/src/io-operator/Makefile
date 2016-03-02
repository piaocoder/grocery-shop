#
#
#	bo gcc 2.0
#		更改代码目录结构
#
# 	2016年 03月 02日 星期三 11:37:55 CST
#
include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

TARGET=io.o io-print io-scanf

all:$(TARGET)

io.o:io.c
	$(CC) -c $(CFLAGS) $^ $(LDFLAGS) -o $@

io-print:io-print.c
	$(CC) $(CFLAGS) $^ io.o $(LDFLAGS) -o $@

io-scanf:io-scanf.c
	$(CC) $(CFLAGS) $^ io.o $(LDFLAGS) -o $@

clean:
	rm $(TARGET) -rf

install:
	cp $(TARGET) $(BO_BINS_DIR)
