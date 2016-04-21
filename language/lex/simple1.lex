/*
编译流程
    1，lex simpl1.lex，生成lex.yy.c文件
    2，cc lex.yy.c -o simple1 -ll
执行流程
    ./simple1
        输入stop，产生相应输出
        输入非stop/start，产生原有数据
*/

%{
#include <stdio.h>
%}

%%

stop printf("Stop command received.\n");
start printf("Start command received.\n");
%%
