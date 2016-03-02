#
#
#	bo server 1.0
#	src directory
#
#
include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

LDFLAGS+=-L$(BO_LIBS_DIR)/lib/ -ljson-c \
		 -L$(BO_LIBS_DIR)/lib/ -lcurl \
		 $(BO_LIBS_DIR)/$(LIBTARGET) 
CFLAGS+=-I$(BO_LIBS_DIR)/include/ \
		-I$(BO_INCLUDE_DIR)/

TARGET=boserver
LIBTARGET=libboserver.a

SUBDIRS = inih avl boinit 
SERVER_OBJS=avl/avltree.o boinit/boinit.o inih/ini.o

all:$(LIBTARGET) $(TARGET)

$(SERVER_OBJS):
	for filename in $(SUBDIRS); do \
		if test -d "$$filename" ; then \
			(cd $$filename; $(MAKE)); \
			if [ $$? -ne 0 ]; then\
				exit 1; \
			fi; \
		fi; \
	done

%.o: %.c
	$(CC) -c $(CFLAGS) $^ $(LDFLAGS) -o $@

$(LIBTARGET):$(SERVER_OBJS)
	rm $(LIBTARGET) -f
	$(AR) cru $@ $^
	cp $(LIBTARGET) $(BO_LIBS_DIR)/ -rf

$(TARGET):boserver.c 
	$(CC) $(CFLAGS) $^ $(OTHEROBJS) $(LDFLAGS) -o $@;
	cp $(TARGET) $(BO_BINS_DIR)/ -rf

clean:
	for filename in $(SUBDIRS); do \
		if test -d "$$filename" ; then \
			(cd $$filename; $(MAKE) clean); \
			if [ $$? -ne 0 ]; then\
				exit 1; \
			fi; \
		fi; \
	done
	rm $(LIBTARGET) $(TARGET) -rf
	rm $(BO_BINS_DIR)/$(TARGET) -rf
	rm $(TARGET) -rf

install:
	cp $(TARGET) $(BO_BINS_DIR) -rf
	cp $(LIBTARGET) $(BO_LIBS_DIR)/ -rf
