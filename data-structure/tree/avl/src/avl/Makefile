#
#
#	bo server 1.0
#	avl impl
#
#

include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

CFLAGS+=-I$(BO_LIBS_DIR)/include/ -I$(BO_INCLUDE_DIR)/

INCLUDE_FILE=avltree.h
OBJS=avltree.o

all:$(OBJS) .move

.move:
	cp $(INCLUDE_FILE) $(BO_INCLUDE_DIR) -rf

%.o: %.c
	$(CC) -c $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm $(BO_INCLUDE_DIR)/$(INCLUDE_FILE) -rf
	rm $(OBJS) -rf
