#ifndef _SRC_COMMON_H_
#define _SRC_COMMON_H_
#include "zlog.h"

#include <time.h>
#include <pthread.h>
#include <string.h>
#include <mysql/mysql.h>
#include <unistd.h>

#if !defined(__bool_true_false_are_defined) && !defined(__cplusplus)
typedef int bool;
#define true 1
#define false 0
#define __bool_true_false_are_defined
#endif
typedef unsigned int        uint32_t;
typedef unsigned short      uint16_t;

#define DEBUG                          false

#define LOG_CONF_PATH                            "/apps/gcc/conf/gcc.ini"
#define DB_BUFF_NUM                    128

#define COMMON_NUMBER                  64
#define COMMON_NAME_SIZE               128
#define COMMON_PATH_SIZE               256
#define COMMON_SIZE                    256
#define COMMON_PACKAGE_SIZE            1024
#define COMMON_UNIT_SIZE               1024
#define COMMON_MAX_SIZE                2048

typedef struct bo_value             bo_value_t;
typedef struct bo_out_queue         bo_out_queue_t;
typedef struct bo_tree_node         bo_tree_node_t;
typedef struct bo_conf              bo_conf_t;

struct bo_tree_node {
    uint16_t                type:4;         // type
    uint16_t                key:12;         // key
    uint16_t                height:16;      // 树高度
    int                     value;       
    bo_tree_node_t         *left;
    bo_tree_node_t         *right;
};

struct bo_conf {
    // log
    char                    confDir[COMMON_PATH_SIZE];
    char                    zlogConf[COMMON_PATH_SIZE];
    char                    errorName[COMMON_NAME_SIZE];
    char                    debugName[COMMON_NAME_SIZE];
};

struct bo_value {
    // conf
    struct bo_conf             boConf;
    
    struct bo_tree_node      **privatedArray;

    // logging
    zlog_category_t           *debug;
    zlog_category_t           *error;
};


/** 
 * @brief   s1 = now - now->second
 * 
 * @param   now: a time_t value
 * 
 * @return  time_t
 */
static inline int clean_second_of_time(time_t now)
{
    struct tm               local;

    localtime_r(&now, &local);
    return now-local.tm_sec;
}

#define bo_prinf(fmt, ...) printf("%d:"fmt ,getpid(), ##__VA_ARGS__ )
#define DEBUG_MSG(...) do {\
        bo_prinf("<DEBUG@PID%d@%s:%d:%s()>: ", getpid(), \
                __FILE__, __LINE__, __PRETTY_FUNCTION__); \
        bo_prinf(__VA_ARGS__); } while (0)

#endif
