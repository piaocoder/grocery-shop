#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <glob.h>

void display(char *test) 
{
    char    coredump = test[0];  

    printf("%c\n", coredump);  
}

int main(int argc, char **argv)
{
    char    *abc = "abc";  
    char    *test = NULL;

    printf("This is a test!\n");
    printf("%s\n", abc);  

    display(test);

    return 0; 
}
