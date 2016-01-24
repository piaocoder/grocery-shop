CC=gcc
CFLAGS=-g -Wall
TARGETS=exe varg myinclude

all:$(TARGETS)

exe:example.c
	$(CC) $(CFLAGS) $^ -o $@

varg:va_arg.c
	$(CC) $(CFLAGS) $^ -o $@

myinclude:myinclude.c
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm *.o $(TARGETS) -rf
