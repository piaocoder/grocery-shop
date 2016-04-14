#!/bin/bash - 
#===============================================================================
#
#          FILE: nsd.sh
# 
#         USAGE: ./nsd.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2016年04月12日 10:47
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  err
#   DESCRIPTION:  display err msg
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
err()                                               
{
    local   stdfile="/data/logs/crontab.log"
    if [[ ! -f "${stdfile}" ]];then
        touch "${stdfile}"
    fi
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@"
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@" >>"${stdfile}"
    exit 1
}

start()
{
    nsd
}

stop()
{
    pid_file="/apps/nsd/var/db/nsd/nsd.pid"
    # stop
    if [[ -f "${pid_file}" ]];then
        cat ${pid_file} | xargs -i kill {}
    fi
}

restart()
{
    stop
    # 睡眠
    sleep 1
    start
}


case "$1" in
    start)
        start;;
    stop)
        stop;;
    restart)
        restart;;
    *)
        restart;;
esac 
