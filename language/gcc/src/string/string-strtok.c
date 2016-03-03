#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MSC_VARS_MATCH_SIZE 512
#define MAX_EXPRESSION_SIZE 256
typedef int int_array4_t[4];
typedef struct msc_rule_condition {               
    int          cmd;                   /* unused*/
    int          op;   
    int_array4_t trfns;
    char         vars[MSC_VARS_MATCH_SIZE];
    char         expression[MAX_EXPRESSION_SIZE];
    char         tail[0];             /* just for easy to move data */
} msc_rule_condition;

int main(int argc, char **argv)
{
    char        str[] = "shit||geg|xxxx";
    char        *str1 = NULL;
    char        *split = "|";
    char        *p = NULL;
    char        *pre = str;
    int         len = strlen(str);

    printf("%s \n", strtok(str, split));
    while ((p=strtok(NULL, split))) {
        printf("%s\n", p);
    }
    write(STDOUT_FILENO, pre, len);
    printf("\n");

    // 如果没有匹配到，返回原值。
    str1 = (char*)calloc(128, 0);
    strcpy(str1, "shit|xxx|;geg|;xxxx;");
    while ((p=strsep(&str1, ";|")) != NULL) {
        printf("-------------%s, %lu\n", p, strlen(p));
    }

    printf("Length structure is %lu\n", sizeof(msc_rule_condition));

    return 0;
}
