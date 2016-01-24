#!/bin/bash - 
#===============================================================================
#
#          FILE: usebin.sh
# 
#         USAGE: ./usebin.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: unlessbamboo (?), unlessbamboo@gmail.com
#  ORGANIZATION: 
#       CREATED: 2016年01月23日 11:57
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
    local   stdfile="/data/logs/bamboo-install.log"
    if [[ ! -f "${stdfile}" ]];then
        touch "${stdfile}"
    fi
    echo "+++++++[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@"
    echo "+++++++[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@" >>"${stdfile}"
    exit 1
}


#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  user_bin_init
#   DESCRIPTION:  init user bin directory
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
user_bin_init()
{
    BINDIR="/home/bin/"

    if [[ ! -d "${BINDIR}" ]];then
        mkdir -p "${BINDIR}"
    fi
    if [[ $? != 0 ]];then
        err "Make new directory ${BINDIR} failed."
    fi
}


main()
{
    user_bin_init
}
main
