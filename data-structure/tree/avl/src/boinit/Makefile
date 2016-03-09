#
#
#	bo server 1.0
#	inih impl
#
#

include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

LDFLAGS+=-L$(BO_LIBS_DIR)/lib/ -ljson-c \
		 -L$(BO_LIBS_DIR)/lib/ -lcurl 
CFLAGS+=-I$(BO_LIBS_DIR)/include/ \
		-I$(BO_INCLUDE_DIR)/

INCLUDE_FILE=boinit.h
OBJS=boinit.o

all:$(OBJS) .move

.move:
	cp $(INCLUDE_FILE) $(BO_INCLUDE_DIR) -rf

%.o: %.c
	$(CC) -c $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm $(BO_INCLUDE_DIR)/$(INCLUDE_FILE) -rf
	rm $(OBJS) -rf
