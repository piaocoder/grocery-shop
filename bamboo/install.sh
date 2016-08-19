#!/bin/bash - 
#===============================================================================
#
#          FILE: install.sh
# 
#         USAGE: ./install.sh 
# 
#   DESCRIPTION: Install or update all configure. Unlessbamm who is owener to all.
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: unlessbamboo (?), unlessbamboo@gmail.com
#  ORGANIZATION: 
#       CREATED: 2016年01月15日 17:09
#      REVISION:  ---
#===============================================================================
# include base.sh
. env/base.sh

set -x


G_CUR_PATH=$(cd $(dirname $0);pwd)
if [[ $? != 0 ]];then
    err "Set absolute path failed!"
fi



update_local()
{
    local localDir="local"
    local localBash="local.sh"
    
    if [[ ! -d ${localDir} ]];then
        err "Not exists ${localDir}."
    fi
    cd ${localDir}

    if [[ ! -f ${localBash} ]];then
        err "Execute ${localBash} failed."
    fi

    bash ${localBash}
    if [[ $? != 0 ]];then
        err "Execute ${localBash} failed."
    fi

    cd -
}



#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  initialize
#   DESCRIPTION:  初始化所有的工作环境，执行env下所有的shell脚本
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
initialize()
{
    DATA_DIR=/data/
    local subDir=("log" "shell" "python")

    if [[ ! -d "${DATA_DIR}" ]];then
        sudo mkdir ${DATA_DIR}
        if [[ $? != 0 ]];then
            err "Mkdir ${DATA_DIR} failed."
        fi
        sudo chown bamboo:bamboo /data/ -R
        if [[ $? != 0 ]];then
            err "Change ${DATA_DIR} authority failed."
        fi
    fi

    cd ${DATA_DIR}
    for dir in "${subDir}";do
        if [[ ! -d ${dir} ]];then
            mkdir ${dir}
            if [[ $? != 0 ]];then
                err "Mkdir ${dir} failed."
            fi
        fi
    done
    cd -
}


update_env()
{
    targetDir="env"
    envFile="env.sh"

    if [[ ! -d "${targetDir}" ]];then
        err "Not exists ${targetDir} directory."
    fi
    cd "${targetDir}"

    if [[ ! -f "${envFile}" ]];then
        err "Not exists ${envFile} directory."
    fi
    bash ${envFile} $1
    if [[ $? != 0 ]];then
        err "Execute ${envFile} failed."
    fi

    cd -
}


update_vim()
{
    targetDir="vim"
    binFile="vim.sh"
    
    if [[ ! -d "${targetDir}" ]];then
        err "Not exists ${targetDir}."
    fi
    cd "${targetDir}"

    if [[ ! -f ${binFile} ]];then
        err "Not exists ${binFile} filename."
    fi

    bash ${binFile}
    if [[ $? != 0 ]];then
        err "Execute ${binFile} failed."
    fi

    cd -
}



update_sshkey()
{
    keyDir="sshkey"
    keyBin="sshkey.sh"
    
    if [[ ! -d ${keyDir} ]];then
        err "Not exists ${keyDir} directory." 
    fi
    cd ${keyDir}

    if [[ ! -f ${keyBin} ]];then
        err "Not exists ${keyBin} filename."
    fi

    bash ${keyBin}
    if [[ $? != 0 ]];then
        err "Execute ${keyBin} failed."
    fi

    cd -
}



main()
{
    initialize
    # update env
    update_env main
    # update local
    update_local
    # update vim
    update_vim
    # update sshkey
    update_sshkey
}

case "$1" in
    normal)
        main;;
    ld)
        update_env ld;;
    *)
        main;;
esac
