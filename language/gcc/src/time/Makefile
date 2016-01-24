CC=gcc
CFLAGS=-g -Wall
TARGETS=configTime.o getCurrentDay getCurrentTime getRandTime periodicTime \
		transformTime compareTime

all:$(TARGETS)

configTime.o:configTime.c
	$(CC) $(CFLAGS) -c $^ -o $@
periodicTime:periodicTime.c
	$(CC) $(CFLAGS) $^ configTime.o -o $@
getCurrentDay:getCurrentDay.c
	$(CC) $(CFLAGS) $^ configTime.o -o $@
getCurrentTime:getCurrentTime.c
	$(CC) $(CFLAGS) $^ configTime.o -o $@
getRandTime:getRandTime.c
	$(CC) $(CFLAGS) $^ -o $@
transformTime:transformTime.c
	$(CC) $(CFLAGS) $^ configTime.o -o $@

compareTime:compareTime.c
	$(CC) $(CFLAGS) $^ configTime.o -o $@

clean:
	rm *.o $(TARGETS) -rf
