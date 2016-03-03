#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<assert.h>
#include<errno.h>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>

#define KEYVALLEN 100
 
/*
 * func:left space clear.
 * return:
 *      if szOutput is equal to szInput:
 *          return NULL.
 *          the value of szOutput doesn't change.
 *      else:
 *          delete left space.
 *          return pointer.
 */
char * left_trim(char * szOutput, const char *szInput)
{
    if (szInput == NULL || szOutput == NULL || szOutput == szInput) {
        return NULL;
    }

    for (; *szInput != '\0' && isspace(*szInput); ++szInput){
        ;
    }

    return strcpy(szOutput, szInput);
}
 
/*
 * func:right space clear.
 */
char *right_trim(char *szOutput, const char *szInput)
{
    char *p = NULL;

    if (szInput == NULL || szOutput == NULL || szOutput == szInput) {
        return NULL;
    }

    strcpy(szOutput, szInput);
    // 下界点
    for(p = szOutput + strlen(szOutput) - 1; p >= szOutput && isspace(*p); --p){
     ;
    }
    *(++p) = '\0';
    return szOutput;
}
 
/*
 * func:clear left and right space.
 */
char * both_trim(char * szOutput, const char * szInput)
{
    char *p = NULL;

    if (szInput == NULL || szOutput == NULL) {
        return NULL;
    }

    if (left_trim(szOutput, szInput) == NULL) {
        return NULL;
    }

    for (p = szOutput + strlen(szOutput) - 1;p >= szOutput && isspace(*p); --p){
     ;
    }
    *(++p) = '\0';

    return szOutput;
}

/*                                                                  
 * func:get specified string                                        
 *      获取src字符串中，不包含module字符之前的子串.
 */                                                                 
static int                                                          
get_specified_sring(const char *src, char *dst, const char *module) 
{                                                                   
    const char      *temp = src;                                    

    if (!src || !dst || !module) {
        return -1;
    }
                                                                    
    while (*temp != '\0') {                                         
        if (strchr(module, *temp) != NULL) {                        
            break;                                                  
        }                                                           
        temp++;                                                     
    }                                                               
    strncpy(dst, src, temp-src);                                    
    dst[temp-src] = '\0';                                           
                                                                    
    return 0;                                                       
}                                                                   
 
/*                                                                          
 * func:get value by key and section                                        
 * argu:                                                                    
 *      value   store result                                                
 */                                                                         
int section_get_value_by_key(FILE *fp, char *section, char *key, char *value )    
{                                                                           
    char appname[32],keyname[32];                                           
    char *buf,*c;                                                           
    char buf_i[KEYVALLEN], buf_o[KEYVALLEN];                                
    int found=0; /* 1 section 2 key */                                      
                                                                            
    if ( fp == NULL || section == NULL || key == NULL || value == NULL ) {  
        return -1;                                                          
    }                                                                       
                                                                            
    fseek( fp, 0, SEEK_SET );                                               
    memset( appname, 0, sizeof(appname) );                                  
    sprintf( appname,"[%s]", section );                                     
                                                                            
    while( !feof(fp) && fgets(buf_i, KEYVALLEN, fp )!=NULL ){               
        if (left_trim(buf_o, buf_i) == NULL) {                              
            return -1;                                                      
        }                                                                   
        if (strlen(buf_o) <= 0) {                                           
            continue;                                                       
        }                                                                   
                                                                            
        buf = buf_o;                                                        
                                                                            
        if( found == 0 ){                                                   
            if( buf[0] != '[' ) {                                           
                continue;                                                   
            } else if ( strncmp(buf,appname,strlen(appname))==0 ){                     
                found = 1;                                                             
                continue;                                                              
            }                                                                          
                                                                                       
        } else if( found == 1 ) {                                                      
            if( buf[0] == '#' ){                                                       
                continue;                                                              
            } else if ( buf[0] == '[' ) {                                              
                break;                                                                 
            } else {                                                                   
                if( (c = (char*)strchr(buf, '=')) == NULL )                            
                    continue;                                                          
                                                                                       
                memset( keyname, 0, sizeof(keyname) );                                 
                get_specified_sring(buf, keyname, "\t =");                             
                if (strcmp(keyname, key) == 0) {                                       
                    get_specified_sring(++c, value, "\n");                             
                    //sscanf( ++c, "%[^\n]", value );                                  
                    char *value_o = (char *)malloc(strlen(value) + 1);                 
                    if(value_o != NULL){                                               
                        memset(value_o, 0, strlen(value) + 1);                         
                        // delete space                                                
                        if (both_trim(value_o, value) == NULL) {                       
                            return -1;                                                 
                        }                                                              
                        if(value_o && strlen(value_o) > 0)                             
                            strcpy(value, value_o);                                    
                        free(value_o);                                                 
                        value_o = NULL;                                                
                    }                                                                  
                    found = 2;                                                         
                    break;                                                             
                } else {                                                               
                    continue;                       
                }                                   
            }                                       
        }//if-else if- else                         
    }//while                                        
                                                    
    if( found == 2 ) {                              
        return 0;                                   
    }                                               
    return -1;                                      
}                                                   

/*
 * func:读取配置文件中的键值，没有section字段分布
 * argu:
 *      value   store result 
 */
int get_value_by_key(FILE *fp, char *key, char *value)
{
    char        keyname[32];
    char        *buf = NULL, *pos = NULL;
    char        *temp = NULL, *tempValue = NULL;
    char        buf_i[KEYVALLEN], buf_o[KEYVALLEN];

    if (fp == NULL || key == NULL || value == NULL) {
        return -1;
    }
    
    /* init */
    fseek(fp, 0, SEEK_SET);
    buf_i[0] = '\0';
    buf_o[0] = '\0';
    temp = value;

    /* main loop */
    while (!feof(fp) && fgets(buf_i, KEYVALLEN, fp) != NULL) {
        if (left_trim(buf_o, buf_i) == NULL) {
            printf("ReadConfig:Call left_trim return illegal value.\n");
            return -1;
        }
        // space line
        if (strlen(buf_o) <= 0) {
            continue;
        }

        buf = NULL;
        buf = buf_o;

        if (buf[0] == '#') {            //comments line
            continue;
        } else if (buf[0] == '[') {   // illegal keyname
            printf("ReadConfig:Illegal format line.\n");
            break;
        } else {
            // get left value of '='
            if ((pos = (char*)strchr(buf, '=')) == NULL) {
                continue;               // value are too long
            }

            // handle left value of '='
            if (get_specified_sring(buf, keyname, "\t =") < 0) {
                printf("ReadConfig:call get_specified_sring failed.\n");
                break;
            }

            // handle right value of '=' when find correct keyname
            if (strcmp(keyname, key) == 0) {
                if (get_specified_sring(++pos, temp, "\n") < 0) {
                    printf("ReadConfig:call get_specified_sring failed.\n");
                    break;
                }
                tempValue = (char *)malloc(strlen(temp) + 1);
                if (tempValue == NULL) {
                    printf("ReadConfig:lack of memory.\n");
                    break;
                }
                memset(tempValue, 0, sizeof(tempValue));

                // delete space 
                if (both_trim(tempValue, temp) == NULL) {
                    printf("ReadConfig:Call both_trim return illegal value.\n");
                    return -1;
                }
                if (strlen(tempValue) > 0) {
                    strcpy(value, tempValue);
                }
                free(tempValue);
                tempValue = NULL;
                return 0;
            }
        }
    }//while

    return -1;
}

int
main(int argc, char **argv) 
{
    char        mode[32] = {0};
    int         ret = -1;
    FILE        *fp;

    // section 和 key 获取 value
    printf("==================start==================\n");
    printf("=====================================\n");
    printf("根据sction和key获取value值:\n");
    fp = fopen("/root/waf/a.info", "r");
    if (fp == NULL) {
        printf("打开文件%s失败!\n", "/root/waf/a.info");
        goto second;
    }
    ret = section_get_value_by_key(fp, "History", "policy", mode);
    if (ret < 0) {
        printf("发生错误!\n");
        fclose(fp);
        fp = NULL;
        return ret;
    }
    fclose(fp);
    fp = NULL;
    printf("section=%s key=%s value=%s\n","History", "policy", mode);
    printf("=====================================\n");
    printf("=================end===================\n\n");

second:
    // key 获取 value
    printf("==================start==================\n");
    printf("=====================================\n");
    printf("根据获取value值:\n");
    fp = fopen("./option.conf", "r");
    if (fp == NULL) {
        printf("打开文件%s失败!\n", "./option.conf");
    }
    ret = get_value_by_key(fp, "TOPWAF_EXPIRE", mode);
    if (ret < 0) {
        printf("发生错误!\n");
        fclose(fp);
        fp = NULL;
        return ret;
    }
    fclose(fp);
    fp = NULL;
    printf("key=%s value=%s\n", "TOPWAF_EXPIRE", mode);
    printf("=====================================\n");
    printf("=================end===================\n\n");
    return 0;
}
