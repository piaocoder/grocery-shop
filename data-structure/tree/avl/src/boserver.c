/*
 * 
 *  bo server version: 1.0
 *  bo server main handle
 *
 */
#include "common.h"
#include "boinit.h"
#include "avltree.h"

#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <math.h>
#include <fcntl.h>
#include <signal.h>

bo_value_t               g_bo;

int main(int argc, char **argv)
{
    int                      rst;

    memset(&g_bo, 0, sizeof(bo_value_t));

    rst = main_init(&g_bo);
    if (!rst) {
        return rst;
    }

    return true;
}


