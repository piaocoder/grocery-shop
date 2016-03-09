#include "boinit.h"
#include "ini.h"
#include "avltree.h"

#include <stdlib.h>

bool boinit_conf_check(bo_value_t *bo)
{
    bo_conf_t           *conf = &bo->boConf;

    // log
    if (conf->confDir[0] == '\0') {
        zlog_info(bo->error, "Config, log-confDir opt not validate.");
        return false;
    }
    if (conf->zlogConf[0] == '\0') {
        zlog_info(bo->error, "Config, log-zlogconf opt not validate.");
        return false;
    }
    if (conf->errorName[0] == '\0') {
        zlog_info(bo->error, "Config, log-error opt not validate.");
        return false;
    }
    if (conf->debugName[0] == '\0') {
        zlog_info(bo->error, "Config, log-debug opt not validate.");
        return false;
    }

    return true;
}

bool boinit_conf_handler(void* user, const char* section, 
                            const char* name, const char* value)
{
    bo_conf_t         *pconfig = (bo_conf_t*)user;

    #define MATCH(s, n) strcmp(section, s) == 0 && strcmp(name, n) == 0
    // log
    if (MATCH("log", "confdir")) {
        strcpy(pconfig->confDir, value);
    } else if (MATCH("log", "zlogconf")) {
        strcpy(pconfig->zlogConf, value);
    } else if (MATCH("log", "error")) {
        strcpy(pconfig->errorName, value);
    } else if (MATCH("log", "debug")) {
        strcpy(pconfig->debugName, value);

    } else {
        DEBUG_MSG("Exists unidentification(%s-%s-%s)?\n", 
                    section, name, value);
        return 1;
    }

    return 0;
}

bool boinit_conf_init(bo_value_t *bo) 
{
    // assignment
    if (ini_parse(LOG_CONF_PATH, boinit_conf_handler,&bo->boConf) < 0) {
        DEBUG_MSG("Initialize configure failed.\n");
        return false;
    }

    return true;
}

bool boinit_log_init(bo_value_t *bo)
{
    int                      rst;
    char                     buff[COMMON_PATH_SIZE];

    // log
    snprintf(buff, COMMON_PATH_SIZE, "%s/%s", bo->boConf.confDir, 
                bo->boConf.zlogConf);
    rst = zlog_init(buff);
    if (rst) {
        DEBUG_MSG("Initialize log configure failed, conf:%s.\n", buff);
        return false;
    }
    bo->debug = zlog_get_category(bo->boConf.debugName);
    if (NULL == bo->debug) {
        DEBUG_MSG("Get bo_debug category failed.\n");
        return false;
    }
    bo->error = zlog_get_category(bo->boConf.errorName);
    if (NULL == bo->error) {
        DEBUG_MSG("Get bo_error category failed.\n");
        return false;
    }

    return true;
}

bool main_init(bo_value_t *bo)
{
    int             rst;

    rst = boinit_conf_init(bo);
    if (!rst) {
        return false;
    }

    rst = boinit_log_init(bo);
    if (!rst) {
        return false;
    }

    rst = boinit_conf_check(bo);
    if (!rst) {
        return false;
    }

    return true;
}

