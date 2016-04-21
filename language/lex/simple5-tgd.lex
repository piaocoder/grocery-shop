/*
    simple4的升级版，用于处理某些参数，并返回特定的值
        例如NUMBER对应正则：
                直接将字符串转为int并返回
            STATE:
                匹配字符串，并返回0/1

        编译：
            lex simple5-tgd.lex
            yacc -d simple5-tgd.y
            cc lex.yy.c y.tab.c -o simple5-tgd

        输入：
            heat on 或者 off
            target temperature 10
*/

%{
#include <stdio.h>
#include "y.tab.h"
%}

%%
[0-9]+ yylval = atoi(yytext); return NUMBER;
heat return TOKHEAT;
on|off yylval = !strcmp(yytext, "on"); return STATE;
target return TOKTARGET;
temperature return TOKTEMPERATURE;
\n /* ignore end of line */
[ \t]+ /* ignore whitespace */

%%
