#
#
#	bo gcc 2.0
#		更改代码目录结构
#
# 	2016年 03月 02日 星期三 11:37:55 CST
#
include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

TARGET=file.o file-create file-change file-fcntl \
	   file-judge file-path file-rw file-rw-uncache \
	   file-sort file-tmp

all:$(TARGET)

file.o:file.c
	$(CC) -c $(CFLAGS) $^ $(LDFLAGS) -o $@

file-create:file-create.c
	$(CC) $(CFLAGS) $^ file.o $(LDFLAGS) -o $@

file-change:file-change.c
	$(CC) $(CFLAGS) $^ file.o $(LDFLAGS) -o $@

file-fcntl:file-fcntl.c
	$(CC) $(CFLAGS) $^ file.o $(LDFLAGS) -o $@

file-judge:file-judge.c
	$(CC) $(CFLAGS) $^ file.o $(LDFLAGS) -o $@

file-path:file-path.c
	$(CC) $(CFLAGS) $^ file.o $(LDFLAGS) -o $@

file-rw:file-rw.c
	$(CC) $(CFLAGS) $^ file.o $(LDFLAGS) -o $@

file-rw-uncache:file-rw-uncache.c
	$(CC) $(CFLAGS) $^ file.o $(LDFLAGS) -o $@

file-sort:file-sort.c
	$(CC) $(CFLAGS) $^ file.o $(LDFLAGS) -o $@

file-tmp:file-tmp.c
	$(CC) $(CFLAGS) $^ file.o $(LDFLAGS) -o $@

clean:
	rm $(TARGET) -rf

install:
	cp $(TARGET) $(BO_BINS_DIR)
