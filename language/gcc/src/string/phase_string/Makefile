CC=gcc
CFLAGS=-g -Wall
TARGETS=exe strtok strEscape

all:$(TARGETS)

exe:example.c
	$(CC) $(CFLAGS) $^ -o $@
strtok:strtok.c
	$(CC) $(CFLAGS) $^ -o $@

strEscape:strEscape.c
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm *.o $(TARGETS) -rf
