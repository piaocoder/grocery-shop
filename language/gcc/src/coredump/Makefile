include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

TARGET=coredump-test

all:$(TARGET)

coredump-test:coredump-test.c
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm $(TARGET) -rf

install:
	cp $(TARGET) $(BO_BINS_DIR)
