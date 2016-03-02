#!/bin/bash - 
#===============================================================================
#
#          FILE: python-tags.sh
# 
#         USAGE: ./python-tags.sh 
# 
#   DESCRIPTION: 
#           因为pyenv的原因或者python多版本的原因，对于tags文件的加载可能会
#           发生错误，比如使用python2.7时，加载的tags文件却是/usr/lib/python2.6
#           下面的tags文件，导致vim的使用出现问题。
#           解决：
#               使用python-config和python --version来自定义的修改*.vim文件
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 03/02/2016 17:07
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
#          NAME:  get_python_version
#   DESCRIPTION:  获取python版本
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
get_python_version()
{

}
