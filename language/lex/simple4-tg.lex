/*
    简单的温度控制器
    命令执行：
        转换Lex文件：
            lex simple4-tg.lex
        根据yacc文件生成对应的.h/.c代码：
            yacc -d simple4-tg.y
        编译
            cc lex.yy.c y.tab.c -o simple4-tg
            此时不再需要-ll，因为本身已经存在main函数，不需要libl提供

        将yacc作为Lex的下游，用于解析从Lex输出的流数据
            运行：
                ./simple4-tg
            输入：
                heat on
                head off
                target temperature 10

*/

%{
#include <stdio.h>
#include "y.tab.h"
/* 否则提示找不到yyval变量 */
extern YYSTYPE yylval;
%}

%%

[0-9]+ return NUMBER;
heat return TOKHEAT;
on|off return STATE;
target return TOKTARGET;
temperature return TOKTEMPERATURE;
\n /* ignore end of line */;
[ \t]+ /* ignore whitespace */
%%
