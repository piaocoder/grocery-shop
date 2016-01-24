CC=gcc
CFLAGS=-g -Wall 
LDFLAGS=-lcrypto -lm
TARGETS=simple_openssl simple_rc4 simple_crypt base64 simple_3des simple_3ds_ecb  simple_des 
all:$(TARGETS)

#hex.o:hex.c
#	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@
#
#symmetry_crypt_simple.o:symmetry_crypt_simple.c
#	$(CC) $(CFLAGS) $^ $(LDFLAGS) -c -o $@

simple_aes:simple_aes.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

simple_openssl:simple_openssl.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

simple_rc4:simple_rc4.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

simple_crypt:simple_crypt.c crypt.c symmetry_crypt.c symmetry_crypt_simple.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

base64:base64.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

simple_3des:simple_3des.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

simple_3ds_ecb:simple_3ds_ecb.c hex.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

simple_des:simple_des.c hex.c
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm *.o $(TARGETS) -rf
