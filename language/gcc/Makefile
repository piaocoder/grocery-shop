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

all:.copy
	for filename in $(SUBDIRS); do \
		if test -d "$$filename" ; then \
			(cd $$filename; $(MAKE) $@);\
			if [ $$? -ne 0 ]; then\
				exit 1; \
			fi; \
		fi; \
	done

.copy:
	cp libs $(BUILD)/ -rf
	cp include $(BUILD)/ -rf
	cp conf $(BUILD)/ -rf
	cp doc $(BUILD)/ -rf

clean:
	for filename in $(SUBDIRS); do \
		if test -d "$$filename" ; then \
			(cd $$filename; $(MAKE) $@); \
		fi; \
	done
	rm bin/* -rf

install:
	for filename in $(SUBDIRS); do \
		if test -d "$$filename"; then \
			(cd $$filename; $(MAKE) $@); \
		fi; \
	done
	# copy execute file to build
	rm bin/*.o -rf
	cp bin $(BUILD)/ -rf
	# cp build directory to install-dir
	mkdir -p $(INSTALLDIR)
	cp build/* $(INSTALLDIR) -rf
