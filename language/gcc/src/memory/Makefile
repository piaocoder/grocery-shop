CC=gcc
CFLAGS=-g -O0 -Wall

all:exe memoryCompilation memoryDistribute

exe:example.c
	$(CC) $(CFLAGS) $^ -o $@
memoryDistribute:memoryDistribute.c
	$(CC) $(CFLAGS) $^ -o $@
memoryCompilation:memoryCompilation.c
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm *.o exe -rf
