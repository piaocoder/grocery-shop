CC=gcc
CFLAGS=-g -Wall -lpthread

TARGET=ev_time.o evBreak evMultiple evPeriodic
LDFLAGS=/usr/local/libev/lib/libev.a -lpthread
CFLAGS=-g -Wall -I/usr/local/libev/include/

all:$(TARGET)

ev_time.o:ev_time.c
	$(CC) $(CFLAGS) -c $^ -o $@

evBreak:evBreak.c
	$(CC) $(CFLAGS) $^  $(LDFLAGS) -o $@

evMultiple:evMultiple.c
	$(CC) $(CFLAGS) $^  ev_time.o $(LDFLAGS) -o $@

evPeriodic:evPeriodic.c
	$(CC) $(CFLAGS) $^  ev_time.o $(LDFLAGS) -o $@

clean:
	rm *.o $(TARGET) -rf
