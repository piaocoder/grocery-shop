#
#
#	bo gcc 1.0
#	src directory
#
#

include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

TARGET= test array-pointer array-init

all:$(TARGET)

array-pointer:array-pointer.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

test:test.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

array-init:array-init.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm -rf $(TARGET) 

install:
	cp $(TARGET) $(BO_BINS_DIR)
