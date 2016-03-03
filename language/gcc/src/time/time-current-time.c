#include "time-config.h"
#include <stdio.h>    
#include <sys/time.h>      

long getCurrentTime()    
{    
   struct timeval tv;    
   gettimeofday(&tv,NULL);    
   printf("%ld\n", tv.tv_usec);
   printf("%ld\n", tv.tv_sec);
   return tv.tv_sec * 1000000 + tv.tv_usec;    
}    
    
int main()    
{    
    printf("c/c++ program:%ld\n",getCurrentTime());    
    return 0;    
} 
