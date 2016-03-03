#
#
#	bo gcc 2.0
#		更改代码目录结构
#
# 	2016年 03月 02日 星期三 11:37:55 CST
#
include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

TARGET=time-config.o time-compare time-current-day \
	   time-current-time time-periodic time-rand \
	   time-transform

all:$(TARGET)

time-config.o:time-config.c
	$(CC) -c $(CFLAGS) $^ $(LDFLAGS) -o $@

time-compare:time-compare.c
	$(CC) $(CFLAGS) $^ time-config.o $(LDFLAGS) -o $@

time-current-day:time-current-day.c
	$(CC) $(CFLAGS) $^ time-config.o $(LDFLAGS) -o $@

time-current-time:time-current-time.c
	$(CC) $(CFLAGS) $^ time-config.o $(LDFLAGS) -o $@

time-periodic:time-periodic.c
	$(CC) $(CFLAGS) $^ time-config.o $(LDFLAGS) -o $@

time-rand:time-rand.c
	$(CC) $(CFLAGS) $^ time-config.o $(LDFLAGS) -o $@

time-transform:time-transform.c
	$(CC) $(CFLAGS) $^ time-config.o $(LDFLAGS) -o $@

clean:
	rm $(TARGET) -rf

install:
	cp $(TARGET) $(BO_BINS_DIR)
