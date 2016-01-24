CC=gcc
CFLAGS=-g -Wall
TARGETS=readConfig

all:$(TARGETS)

readConfig:readConfig.c
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm *.o $(TARGETS) -rf
