#!/bin/bash - 
#===============================================================================
#
#          FILE: restart.sh
# 
#         USAGE: ./restart.sh 
# 
#   DESCRIPTION: 重启djangoserver服务器
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2016年03月11日 11:45
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
    local   stdfile="/data/logs/family-install.log"
    if [[ ! -f "${stdfile}" ]];then
        touch "${stdfile}"
    fi
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@"
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@" >>"${stdfile}"
    exit 1
}


#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  kill_old_pid
#   DESCRIPTION:  
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
kill_old_pid()
{
    # 不能使用“”，不然执行失败，哎（例如shell上：sh ps -ef也失败）
    pidList=`/bin/ps -ef|grep '/usr/bin/python /usr/bin/gunicorn'|grep 'family.wsgi'|grep -v grep| awk '{print \$2}'`

    for pid in ${pidList};do
        kill ${pid}
    done
}


#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  run_server
#   DESCRIPTION:  启动
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
run_server()
{
    nohup gunicorn -b 0.0.0.0:8787 --workers=4 --worker-connections 50 \
        --max-requests 10 --keep-alive 20 -D family.wsgi 2>&1 &
}


case $1 in
    start)
        kill_old_pid
        run_server;;
    stop)
        kill_old_pid;;
    restart)
        kill_old_pid
        run_server;;
    *)
        kill_old_pid;;
esac
