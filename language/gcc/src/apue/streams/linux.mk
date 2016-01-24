include ../Make.defines.linux
EXTRA=
CC=gcc

PROGS = #strlist t_isastream

all:	${PROGS} spipe.o sendfd.o recvfd.o cliconn.o servlisten.o servaccept.o \
		ptyopen.o isastream.o t_isastream strlist

spipe.o:	spipe.c

sendfd.o:	sendfd.c

recvfd.o:	recvfd.c

isastream.o:	isastream.c

cliconn.o:	cliconn.c

servlisten.o:	servlisten.c

servaccept.o:	servaccept.c

ptyopen.o:	ptyopen.c

t_isastream:t_isastream.c                   
	gcc $^ -lapue -o $@

strlist:strlist.c                   
	gcc $^ -lapue -o $@

clean:
	rm -f ${PROGS} ${TEMPFILES} *.o

