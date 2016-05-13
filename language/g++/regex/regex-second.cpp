extern "C" {
#include <pcre.h>
#include <stdio.h>
#include <string.h>
}
 
/*
 * 执行命令：./regex-second 127.0.0.1 127.0.0.1/23 \"gelgejlge-lxjgle-\"{
 */
int main(int argc, char ** argv)
{
    const char * pPattern = "^(?:(?:25[0-5]|2[0-4][0-9]"
        "|[01]?[0-9][0-9]?)\\.){3}"
        "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$";
    const char * p1Pattern = "^((?:(?:25[0-5]|2[0-4][0-9]"
        "|[01]?[0-9][0-9]?)\\.){3}"
        "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))"
        "/([0-9]|[1-2][0-9]|3[0-2])$";
    const char * p2Pattern = "^\"([a-zA-Z][a-zA-Z-]*?)\"{[ ]*?$";
    const char * pErrMsg = NULL;
    const char  *subMatchStr = NULL;
    char   buf[256];
    char * pText = NULL;;
    pcre * pPcre = NULL;
    int eOffset = -1;
    int nOffset[256];
    int ret;

    if (argc != 4) {
        printf("Unvalidate argument!\n");
        return 0;
    }
    pText = argv[1];
 
    if (NULL == (pPcre = pcre_compile(pPattern, 0, &pErrMsg, &eOffset, NULL))) {   
        printf("ErrMsg=%s, Offset=%d\n", pErrMsg, eOffset);
        return 1;
    } else {   
        if (pcre_exec(pPcre, NULL, pText, strlen(pText), 0, 0, NULL, 0) < 0) {   
            printf("%s doesn't match %s\n", pText, pPattern);
        } else {   
            printf("%s matches %s\n", pText, pPattern);
        }
    }

    // 127.0.0.1/32
    pText = argv[2];
    if (NULL == (pPcre = pcre_compile(p1Pattern, 0, &pErrMsg, &eOffset, NULL))) {   
        printf("ErrMsg=%s, Offset=%d\n", pErrMsg, eOffset);
        return 1;
    } else {   
        ret = pcre_exec(pPcre, NULL, pText, strlen(pText), 0, 0, (int*)&nOffset, 256);
        if (ret < 0) {   
            printf("%s doesn't match %s\n", pText, p1Pattern);
        } else {   
            printf("%s matches %s, matchNumber=%d\n", 
                    pText, p1Pattern, ret);
            int i;
            for (i=0; i<ret; i++) {
                printf("位置：%d\n", nOffset[2*i]);
            }
            pcre_get_substring(pText, nOffset, ret, 1, &(subMatchStr));
            printf("匹配的Ip地址：%s\n", subMatchStr);
        }
    }

    // "guangdong-tel"{，shell's value is equal to \"gelgejlge-lxjgle-\"{
    pText = argv[3];
    strcpy(buf, pText);
    if (NULL == (pPcre = pcre_compile(p2Pattern, 0, &pErrMsg, &eOffset, NULL))) {   
        printf("ErrMsg=%s, Offset=%d\n", pErrMsg, eOffset);
        return 1;
    } else {   
        ret = pcre_exec(pPcre, NULL, buf, strlen(buf), 0, 0, (int*)&nOffset, 256);
        if (ret < 0) {   
            printf("%s doesn't match %s\n", buf, p2Pattern);
        } else {   
            printf("%s matches %s\n", buf, p2Pattern);
            int i;
            for (i=0; i<ret; i++) {
                printf("位置：%d\n", nOffset[2*i]);
            }
            pcre_get_substring(buf, nOffset, ret, 1, &(subMatchStr));
            printf("匹配的position地址：%s\n", subMatchStr);
        }
    }

    pcre_free(pPcre);
    return 0;
}
