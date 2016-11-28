#
#
#	BO server 1.0
#	base64 impl
#
#

include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

CFLAGS+=-I$(BO_PACKAGES_DIR)/include/ -I$(BO_INCLUDE_DIR)/ \
		-I$(BO_LIBS_INCLUDE_DIR)/

INCLUDE_FILE=base64.h
OBJS=base64.o

all:$(OBJS) .move

.move:
	cp $(INCLUDE_FILE) $(BO_INCLUDE_DIR) -rf

%.o: %.c
	$(CC) -c $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm $(BO_INCLUDE_DIR)/$(INCLUDE_FILE) -rf
	rm $(OBJS) -rf
