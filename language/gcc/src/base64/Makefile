#
#
#	kv server 1.0
#	base64 impl
#
#

include $(KV_DIR)/mk/vars.mk
include $(KV_DIR)/mk/compile.mk

CFLAGS+=-I$(KV_PACKAGES_DIR)/include/ -I$(KV_INCLUDE_DIR)/

INCLUDE_FILE=base64.h
OBJS=base64.o

all:$(OBJS) .move

.move:
	cp $(INCLUDE_FILE) $(KV_INCLUDE_DIR) -rf

%.o: %.c
	$(CC) -c $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm $(KV_INCLUDE_DIR)/$(INCLUDE_FILE) -rf
	rm $(OBJS) -rf
