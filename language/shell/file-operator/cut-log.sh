#!/bin/bash - 
#===============================================================================
#
#          FILE: cut-log.sh
# 
#         USAGE: ./cut-log.sh 
# 
#   DESCRIPTION: 切割日志
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2016年03月15日 08:38
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error


cut_log()
{
    access_log=/opt/job/logs/access.log
    access_https_log=/opt/job/logs/access_https.log
    access_dir=/opt/job/logs/
    # access.log.2014-08-20
    log_name="access.`date +%F`"
    # access_https.2014-08-20
    log_name1="access_https.`date +%F`"

    ip=192.168.1.103
    ddir=/data/job_logs
    yesterday=$(date  +"%Y%m%d")
    #yesterday=$(date  +"%Y%m%d" -d  "-1 days")

    cd $access_dir
    tar zcvf $log_name.`hostname`.tar.gz $access_log
    tar zcvf $log_name1.`hostname`.tar.gz $access_log
    > $access_log
    > $access_https_log

    ssh $ip "mkdir $ddir/$yesterday"
    scp $log_name.`hostname`.tar.gz $ip:/$ddir/$yesterday/
    scp $log_name1.`hostname`.tar.gz $ip:/$ddir/$yesterday/
    ssh $ip "chown -R rd.rd $ddir/$yesterday"
}


cut_log
