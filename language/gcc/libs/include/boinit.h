#ifndef _SRC_BO_INIT_H_
#define _SRC_BO_INIT_H_
#include "common.h"

bool boinit_conf_check(bo_value_t *bo);
bool boinit_conf_init(bo_value_t *bo); 
bool boinit_log_init(bo_value_t *bo);

bool main_init(bo_value_t *bo);

#endif
