#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <glob.h>
#include <sys/stat.h>
#include <sys/types.h>

int main(int argc, char **argv)
{
    //glob_t      buf;
    //int         i = 0;
    //char        *abc = NULL;

    //glob("/home/temp/*.c", GLOB_NOSORT, NULL, &buf);
    //for (i=0; i<buf.gl_pathc; i++) {
    //    printf("%s\n", buf.gl_pathv[i]);
    //}

    //*abc = '2';

    //globfree(&buf);

    mkdir("/tmp/ageg/", 0777);
    return 0;
}
