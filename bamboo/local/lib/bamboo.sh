#!/bin/bash - 
#===============================================================================
#
#          FILE: bamboo.sh
# 
#         USAGE: ./bamboo.sh 
# 
#   DESCRIPTION: 
#           My own shell library.
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2016年06月12日 19:46
#      REVISION:  ---
#===============================================================================

errorDir="/data/log/"
errorFile="${errorDir}/shell.log"

#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  err
#   DESCRIPTION:  打印错误信息
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
err()
{
    if [[ ! -f ${errorFile} ]];then
        if [[ ! -d ${errorDir} ]];then
            mkdir -p ${errorDir}
            if [[ $? != 0 ]];then
                echo -e "\033[0;45;1m"\
                    "+++++++["\
                    "$(date +'%Y-%m-%dT%H:%M:%S%z')]:"\
                    "mkdir ${errorDir} failed.\033[0m"
                exit 1
            fi
        fi
        echo "" > ${errorFile}
    fi
    echo -e "\033[0;45;1m"\
        "+++++++[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@"\
        "\033[0m"
    echo -e "\033[0;45;1m"\
        "+++++++[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@"\
        "\033[0m" >> "${errorFile}"
    exit 1
}

