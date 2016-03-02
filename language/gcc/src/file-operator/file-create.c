#include "file.h"

#define FILE_FIRST  "./filedir/testdir/subdir/wahha"
#define FILE_SECOND  "./filedir/testdir/subdir2/"

static int                                                                       
alarmd_createdir(const char *directory)
{                                                                                
    int             i = 0;                                                       
    int             iRet = -1;                                                   
    int             iLen = 0;                                                    
    char            dirBuf[512] = {0};                                           
                                                                                 
    if(NULL == directory){                                                       
        return -1;                                                               
    }                                                                            
                                                                                 
    // copy directory string                                                     
    iLen = strlen(directory);                                                    
    memcpy(dirBuf, directory, iLen);                                             
                                                                                 
    for (i=0; i<=iLen; i++) {                                                    
        if (dirBuf[i] == '\\' || dirBuf[i] == '/') {                             
            dirBuf[i] = '\0';                                                    
                                                                                 
            // first '/'                                                         
            if (strlen(dirBuf) == 0) {                                           
                dirBuf[i] = '/';                                                 
                continue;                                                        
            }                                                                    
                                                                                 
            if ((iRet = access(dirBuf,  F_OK)) == -1) {                          
                if ((iRet = mkdir(dirBuf, 0777)) == -1) {                        
                    printf("Check-Dir:create directory %s failed.\n", dirBuf);   
                    return iRet;                                                 
                }                                                                
            }                                                                    
            // change '\0' to '/' and converst '\\' to '/'                       
            dirBuf[i] = '/';                                                     
        }                                                                        
    }                                                                         
                                                                              
    if (access(dirBuf, F_OK) == -1) {                                         
        if (mkdir(dirBuf, 0777) < 0) {                                        
            printf("Check-Dir:create directory %s failed.\n", dirBuf);        
            return -1;                                                        
        }                                                                     
    }                                                                         
                                                                              
    return 0;                                                                 
}                                                                             

int
main(int argc, char **argv)
{
    if (alarmd_createdir(FILE_FIRST) < 0) {
        return -1;
    }

    if (alarmd_createdir(FILE_SECOND) < 0) {
        return -1;
    }

    return 0;
}


