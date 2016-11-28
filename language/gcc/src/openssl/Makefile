#
#	bo gcc 2.0
#		更改代码目录结构
#
# 	2016年 03月 02日 星期三 11:37:55 CST
#
include $(BO_DIR)/mk/vars.mk
include $(BO_DIR)/mk/compile.mk

TARGET=crypt.o hex.o symmetry.o crypt-3decs crypt-3decs-ecb \
	   crypt-aes crypt-aes-test  crypt-base64 crypt-des \
	   crypt-openssl crypt-rc4 crypt-simple-test \
	   crypt-symmetry-test

LDFLAGS+=-lcrypto -lz -lssl -lm

all:$(TARGET)

crypt.o:crypt.c
	$(CC) -c $(CFLAGS) $^ $(LDFLAGS) -o $@

hex.o:hex.c
	$(CC) -c $(CFLAGS) $^ $(LDFLAGS) -o $@

symmetry.o:symmetry.c
	$(CC) -c $(CFLAGS) $^ $(LDFLAGS) -o $@

crypt-3decs:crypt-3decs.c
	$(CC) $(CFLAGS) $^ crypt.o $(LDFLAGS) -o $@

crypt-3decs-ecb:crypt-3decs-ecb.c
	$(CC) $(CFLAGS) $^ crypt.o hex.o $(LDFLAGS) -o $@

crypt-aes:crypt-aes.c
	$(CC) $(CFLAGS) $^ crypt.o $(LDFLAGS) -o $@

crypt-aes-test:crypt-aes-test.c
	$(CC) $(CFLAGS) $^ crypt.o $(LDFLAGS) -o $@

crypt-base64:crypt-base64.c
	$(CC) $(CFLAGS) $^ crypt.o $(LDFLAGS) -o $@

crypt-des:crypt-des.c
	$(CC) $(CFLAGS) $^ crypt.o $(LDFLAGS) -o $@

crypt-openssl:crypt-openssl.c
	$(CC) $(CFLAGS) $^ crypt.o $(LDFLAGS) -o $@

crypt-rc4:crypt-rc4.c
	$(CC) $(CFLAGS) $^ crypt.o $(LDFLAGS) -o $@

crypt-simple-test:crypt-simple-test.c
	$(CC) $(CFLAGS) $^ crypt.o symmetry.o $(LDFLAGS) -o $@

crypt-symmetry-test:crypt-symmetry-test.c
	$(CC) $(CFLAGS) $^ crypt.o symmetry.o $(LDFLAGS) -o $@

clean:
	rm $(TARGET) -rf

install:
	cp $(TARGET) $(BO_BINS_DIR)
