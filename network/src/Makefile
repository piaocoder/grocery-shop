#
#
#   dns 
#
#
include $(BO_NETWORK_DIR)/mk/vars.mk
include $(BO_NETWORK_DIR)/mk/compile.mk

TARGET=print.o sniff sniff2

all: $(TARGET)

sniff: sniff.c structures.h print.c print.h
    $(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

sniff2: sniff.c structures.h
    $(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm -rf $(TARGET)

install:
	cp $(TARGET) $(BO_NETWORK_BINS_DIR)
