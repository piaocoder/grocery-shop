#
#
#	bo gcc 1.0
#	src directory
#
#

include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

TARGET= getopt-test

all:$(TARGET)

getopt-test:getopt-test.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm -rf $(TARGET) 

install:
	cp $(TARGET) $(BO_BINS_DIR)
