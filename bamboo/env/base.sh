#!/bin/bash - 
#===============================================================================
#
#          FILE: base.sh
# 
#         USAGE: ./base.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2016年07月05日 10:34
#      REVISION:  ---
#===============================================================================


#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  err
#   DESCRIPTION:  display err msg
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
err()
{
    local   stddir="/data/log/"
    local   stdfile="${stddir}/install.log"

    if [[ ! -f ${stdfile} ]];then
        if [[ ! -d ${stddir} ]];then
            mkdir -p ${stddir}
            if [[ $? != 0 ]];then
                echo -e "\033[0;45;1m"\
                    "+++++++["\
                    "$(date +'%Y-%m-%dT%H:%M:%S%z')]:"\
                    "mkdir ${stddir} failed.\033[0m"
                exit 1
            fi
        fi
        touch ${stdfile}
    fi
    echo -e "\033[0;45;1m"\
        "+++++++[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@"\
        "\033[0m"
    echo -e "\033[0;45;1m"\
        "+++++++[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@"\
        "\033[0m" >> "${stdfile}"
    exit 1
}


MY_SYSTEM=`uname`
LINUX_SYSTEM="Linux"
MAC_SYSTEM="Darwin"
