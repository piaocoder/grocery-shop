#
#
#	bo gcc 1.0
#	src directory
#
#
include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

LDFLAGS+=-L$(BO_LIBS_DIR)/lib/ \
		 $(BO_LIBS_DIR)/$(LIBTARGET) 
CFLAGS+=-I$(BO_LIBS_INCLUDE_DIR)/ -I$(BO_INCLUDE_DIR)/

SUBDIRS = base64 array coredump daemon execl file-operator \
		  hash io-operator libev loop macro memory openssl \
		  orphan-process pci ptrace python read-config \
		  regex signal sizeof socket string struct \
		  syntax time xml zombie-process

all:.compile

.compile:	
	for filename in $(SUBDIRS); do \
		if test -d "$$filename" ; then \
			(cd $$filename; $(MAKE)); \
			if [ $$? -ne 0 ]; then\
				exit 1; \
			fi; \
		fi; \
	done

clean:
	for filename in $(SUBDIRS); do \
		if test -d "$$filename" ; then \
			(cd $$filename; $(MAKE) clean); \
			if [ $$? -ne 0 ]; then\
				exit 1; \
			fi; \
		fi; \
	done

install:
	for filename in $(SUBDIRS); do \
		if test -d "$$filename"; then \
			(cd $$filename; $(MAKE) $@); \
		fi; \
	done
