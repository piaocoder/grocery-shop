CC=gcc

TARGETS=first second

CTARGETS:= $(foreach x, $(TARGETS), $(addprefix $(x),.c))

CFLAGS=-g -Wall 

all:$(TARGETS)
	# 使用循环，生成每一个可执行文件
	for temp in $(TARGETS); do\
		$(CC) $(CFLAGS) $(addprefix $$temp,.c) -o $$temp; \
	done

clean:
	rm *.o $(TARGETS) -rf

