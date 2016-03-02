#ifndef  _CONFIGIO_H_
#define  _CONFIGIO_H_
#include <stdio.h>
#include <stdlib.h>
#include <string.h> 

#define  MYLOVE         "AGE"
#define  FILENAME       "./filedir/uncacheTest.b"

/*
 * 功能：清除缓存
 */
void clear_stdbuf();

int get_specified_sring(const char *src, char *dst, const char *module);

/*
 * 功能：替换st中的子串orig为repl串
 */
char *replace_one(char *st, char *orig, char *repl);

/*
 * 功能：替换st中的所有子串orig为repl串
 */
char *replace_str2(const char *str, const char *old, const char *new);

#endif
