#!/bin/bash - 
#===============================================================================
#
#          FILE: bamboo.sh
# 
#         USAGE: ./bamboo.sh 
# 
#   DESCRIPTION: 
#           shell library files
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2016年06月10日 09:35
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
    local   stdfile="${HOME}/.local/data/shell.log"
    if [[ ! -f "${stdfile}" ]];then
        touch "${stdfile}"
    fi
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@"
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@" >>"${stdfile}"
    exit 1
}


