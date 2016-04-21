%{
#include <stdio.h>
#include <string.h>
/*新的类型*/
#define YYSTYPE char *

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
        | commands command SEMICOLON
        ;

command:
       zone_set
       ;

zone_set:
        /*zone字段，quotedname zonecontent, 即zone "quote" {}时*/
        ZONETOK quotedname zonecontent
        {
            printf("Complete zone for '%s' found\n", $2);
        }
        ;

zonecontent:OBRACE zonestatements EBRACE
           /*quotedname在碰到"file"时触发，并将"file"赋值给quotedname*/
           quotedname:QUOTE FILENAME QUOTE
           {
              /*$$表示quotedname，将FILENAME赋值给quotedname*/
              $$ = $2
           }
           ;

zonestatements:zonestatements zonestatement SEMICOLON
              /*zones结构可以递归*/
              ;

zonestatement:statements
             /* 或结构, "|" */
             |FILETOK quotedname
             {
                printf("A zonefile name '%s' was encountered\n", $2);
             }
             ;

block:OBRACE zonestatements EBRACE SEMICOLON
     ;

statements:statements statement
          ;

statement:WORD | bock | quotedname
         ;


%%
