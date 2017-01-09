#!/bin/bash - 
#===============================================================================
#
#          FILE: local.sh
# 
#         USAGE: ./local.sh 
# 
#   DESCRIPTION: 
#           local 目录的设置
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: The current file is dependent upon update_local
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2016年06月13日 15:13
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
    local   stdfile="/data/log/bamboo-install.log"
    if [[ ! -f "${stdfile}" ]];then
        touch "${stdfile}"
    fi
    echo "+++++++[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@"
    echo "+++++++[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@" >>"${stdfile}"
    exit 1
}


#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  _update_local
#   DESCRIPTION:  
#           拷贝当前子目录到$HOME/.local目录下
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
_update_local()
{
    local subArr=("bin")
    for dir in "${subArr[@]}";do
        cp -rf ${dir} $HOME/.local/
        if [[ $? != 0 ]];then
            err "Copy ${dir} to ~/.local/ failed."
        fi
    done
}



update_local_env()
{
    local dstDir="${HOME}/.local"
    local subArr=("bin")

    if [[ ! -d ${dstDir} ]];then
        mkdir -p ${dstDir}
        if [[ $? != 0 ]];then
            err "Mkdir ${dstDir} failed!"
        fi
    fi

    cd ${dstDir}
    for sub in ${subArr[@]};do
        if [[ ! -d ${sub} ]];then
            mkdir -p ${sub}
            if [[ $? != 0 ]];then
                err "Mkdir ${sub} failed!"
            fi
        fi
    done
    
    cd -
}


update_local_env
_update_local
