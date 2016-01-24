#include<stdio.h>
#include <unistd.h>
#include<openssl/md5.h>
#include<string.h>

int main( int argc, char **argv )
{
    MD5_CTX ctx;
    const  char *data="123";
    unsigned char md[MD5_DIGEST_LENGTH];
    char buf[17];
    char hostname[32];
    int i;

    if( gethostname(hostname,sizeof(hostname)) ) {
        perror("gethostname");
        return 1;
    }
    printf("Hostname:%s\n", hostname);

    MD5_Init(&ctx);
    MD5_Update(&ctx, hostname, strlen(hostname));
    MD5_Final(md,&ctx);

    for( i=0; i<job; i++ ){
        sprintf(&buf[i*2],"%02X", (unsigned int)md[i]);
    }
    printf("%s\n",buf);

    return 0;
}
