/*
    解析某一个文件并输出，该文件给我们讲解了Lex如果解析一个配置或者C文件
    输入：
        ./simple3-parse < bamboo.conf
*/

%{
#include <stdio.h>
%}

%%

[a-zA-Z][a-zA-Z0-9]* printf("WORD");
[a-zA-Z0-9\/.-]+ printf("FILENAME");
\" printf("QUOTE");
\{ printf("Obrace");
\} printf("Ebrace");
; printf("Semicolon");
\n printf("\n");
[ \t]+
%%
