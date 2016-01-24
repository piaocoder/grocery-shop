CC=gcc
CFLAGS=-g -Wall

all:

exe:example.c
	$(CC) $(CFLAGS) $^ -o $@
strtok:strtok.c
	$(CC) $(CFLAGS) $^ -o $@

strEscape:strEscape.c
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm *.o exe -rf
