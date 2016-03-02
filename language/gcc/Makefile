#
#
#	bo server 1.0
#	sub dir Makefile
#
#
include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

# 编译时配置
INSTALLDIR=/apps/boserver
BUILD=./build

SUBDIRS = src

all:
	for filename in $(SUBDIRS); do \
		if test -d "$$filename" ; then \
			(cd $$filename; $(MAKE) $@);\
			if [ $$? -ne 0 ]; then\
				exit 1; \
			fi; \
		fi; \
	done
	cp libs/* $(BUILD)/libs/ -rf
	cp include/* $(BUILD)/include/ -rf
	cp bin/* $(BUILD)/bin/ -rf

clean:
	for filename in $(SUBDIRS); do \
		if test -d "$$filename" ; then \
			(cd $$filename; $(MAKE) $@); \
		fi; \
	done

install:
	for filename in $(SUBDIRS); do \
		if test -d "$$filename"; then \
			(cd $$filename; $(MAKE) $@); \
		fi; \
	done
	mkdir -p $(INSTALLDIR)
	cp build/* $(INSTALLDIR) -rf
