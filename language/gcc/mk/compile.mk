#
#
#
#	bo server 1.0
#	compile variable define
#
#

MYSQL_LIB=`mysql_config --libs`
MYSQL_CFLAGS=`mysql_config --cflags`

#CFLAGS=-g -ggdb3 -Wall -pg $(MYSQL_CFLAGS) -I/$(BO_INCLUDE_DIR)/
#CFLAGS=-g -ggdb3 -Wall $(MYSQL_CFLAGS) -I/$(BO_INCLUDE_DIR)/
CFLAGS=-g -ggdb3 -Wall -I/$(BO_INCLUDE_DIR)/
#LDFLAGS=$(MYSQL_LIB) -L$(BO_LIBS_DIR)/lib/ -lzlog -lpthread -ltcmalloc
# LDFLAGS=$(MYSQL_LIB) -L$(BO_LIBS_DIR)/lib/ -lzlog -lpthread
LDFLAGS=-L$(BO_LIBS_DIR)/lib/ -lzlog -lpthread

CC=gcc
