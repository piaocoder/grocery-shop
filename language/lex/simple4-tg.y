%{
#include <stdio.h>
#include <string.h>

/*
    yacc发现错误时调用
*/
void yyerror()
{
}

/* 
    返回1表示输入结束
*/
int yywrap(void)
{
    return 1;
}

int main()
{
    /* yyparse不断的从文件中读取数据，直到EOF */
    yyparse();

    return 0;
}
%}

/*
    token从Lex中获取，从而实现lex和yacc的结合
*/
%token NUMBER TOKHEAT STATE TOKTARGET TOKTEMPERATURE

/*
    根据下面的Rule section 生成y.tab.h
*/
%%
commands: /* empty */
        | commands command
        ;

command: heat_switch
       | target_set
       ;

heat_switch:
           /* 标识符(TOKHEAT)/temperature/数字组成 */
           TOKHEAT STATE
           {
                printf("\tHeat turned on or off\n");
           }
           ;

target_set:
           TOKTARGET TOKTEMPERATURE NUMBER
           {
                printf("\tTemperature set\n");
           }
           ;
%%
