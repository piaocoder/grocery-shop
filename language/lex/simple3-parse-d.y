/*
*/

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
/*%token NUMBER TOKHEAT STATE TOKTARGET TOKTEMPERATURE*/
%token ZONETOK FILETOK WORD FILENAME QUOTE OBRACE EBRACE
%token SEMICOLON


/*
    根据下面的Rule section 生成y.tab.h
*/
%%
commands: 
        /* empty,表明commands本身可以为空 
            可能存在如下语法：
                zone "." {
                    ...
                };
                zone1 "." {
                    ...
                };
                ...
            其中
                command 代表 zone “." { ... }
                semicolon是一个终端符号，代表分号
            递归语法：
                rule    :   endCase(基本退出条件)
                        |   rule endCase
                必须存在基本退出条件，否则死循环
        */
        | commands command SEMICOLON
        ;

command:zone_set
       ;

zone_set:ZONETOK quotedname zonecontent 
        {
            /*
               终端符号：zone字段——zone1
               非终端符号：quotedname —— "quote"
               非终端符号：zonecontent —— {}
            */
            printf("Complete zone for '%s' found\n", $2);
        }
        ;

zonecontent:OBRACE zonestatements EBRACE
           /*
            终端符号：{
            非终端符号：zonestatements
            终端符号：}
           */
           ;

quotedname:QUOTE FILENAME QUOTE 
          {
              /*
              终端符号："
              终端符号：文件名或者其他字符串(yylval)
              终端符号："
              功能：
                  quotedname在碰到"file"时触发，
                  并将"file"赋值给quotedname
                  $$表示quotedname，
                  将FILENAME赋值给quotedname
              */
              $$ = $2
          }
          ;

zonestatements:
              /*
              zonestatement:表示分号之前的表达式
              semicolon:分号
              代表多行，每一行以分号结尾
              */
              |zonestatements zonestatement SEMICOLON
              ;

zonestatement:statements
             /*
                行分两种：file指明文件，其他格式
             */
             |FILETOK quotedname
             {
                printf("A zonefile name '%s' was encountered\n", $2);
             }
             ;

block:OBRACE zonestatements SEMICOLON EBRACE
     /* 行中的 { null; }格式 */
     ;

statements:
          |statements statement
          ;

statement:WORD | block | quotedname
         ;


%%
