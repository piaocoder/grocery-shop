CC=gcc
CFLAGS=-g -Wall
TARGET=fileConfig.o fileSort fileTmp fileJudge fileRW filePath fileRwUncache testfcntl
TARGET+=fileCreate

all:$(TARGET)

fileConfig.o:fileConfig.c
	$(CC) -c $(CFLAGS) $^ -o $@

testfcntl:testfcntl.c
	$(CC) $(CFLAGS) $^ fileConfig.o -o $@

filePath:filePath.c
	$(CC) $(CFLAGS) $^ fileConfig.o -o $@

fileRW:fileRW.c
	$(CC) $(CFLAGS) $^ fileConfig.o -o $@

fileRwUncache:fileRwUncache.c
	$(CC) $(CFLAGS) $^ fileConfig.o -o $@

fileSort:fileSort.c
	$(CC) $(CFLAGS) $^ fileConfig.o -o $@

fileTmp:fileTmp.c
	$(CC) $(CFLAGS) $^ fileConfig.o -o $@

fileJudge:fileJudge.c
	$(CC) $(CFLAGS) $^ fileConfig.o -o $@

fileCreate:fileCreate.c
	$(CC) $(CFLAGS) $^ fileConfig.o -o $@

clean:
	rm *.o $(TARGET) -rf
