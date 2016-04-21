/*
    展示如何在lex中使用正则表达式
    匹配规则：
        先匹配前面的，之后在往下匹配，输出：
            0——NUMBERS
            0a——NUMBERS Alphabet
*/

%{
#include <stdio.h>
%}

%%

[0123456789]+ printf("NUMBERs\n");
[a-zA-Z][a-zA-Z0-9]* printf("Alphabet\n");
%%
