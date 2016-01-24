CC=gcc
CFLAGS=-g -Wall

TARGET=unixSocketClient unixSystem server client unixSocketServer 
LDFLAGS=/usr/local/libev/lib/libev.a -lpthread
CFLAGS=-g -Wall -I/usr/local/libev/include/

all:$(TARGET)

unixSocketClient:unixSocketClient.c
	$(CC) $(CFLAGS) $^  $(LDFLAGS) -o $@

unixSystem:unixSystem.c
	$(CC)  $^  -o $@

unixSocketServer:unixSocketServer.c
	$(CC) $(CFLAGS) $^  $(LDFLAGS) -o $@


client:client.c
	$(CC) $(CFLAGS) $^  $(LDFLAGS) -o $@

server:server.c
	$(CC) $(CFLAGS) $^  $(LDFLAGS) -o $@

clean:
	rm *.o $(TARGET) -rf
