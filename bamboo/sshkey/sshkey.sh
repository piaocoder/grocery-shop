#!/bin/bash - 
#===============================================================================
#
#          FILE: sshkey.sh
# 
#         USAGE: ./sshkey.sh 
# 
#   DESCRIPTION: 公钥的部署以及配置
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2016年08月19日 09:45
#      REVISION:  ---
#===============================================================================
# include base.sh
. ../env/base.sh

set -o nounset                              # Treat unset variables as an error



ssh_key_init()
{
    sshKeyDir="$HOME/.ssh/"

    which ssh-keygen
    if [[ $? != 0 ]];then
        if [[ "${MY_SYSTEM}" == ${LINUX_SYSTEM} ]];then
            sudo aptitude install ssh
        elif [[ ${MY_SYSTEM} == ${MAC_SYSTEM} ]];then
            brew install ssh
        else
            err "Un-recognized syste."
        fi
        if [[ $? != 0 ]];then
            err "Install ssh by apt failed."
        fi
    fi

    if [[ ! -d "${sshKeyDir}" ]];then
        ssh-keygen -t rsa -C "Add rsa"
        if [[ $? != 0 ]];then
            err "Generate ssh-keygen failed."
        fi
    fi
}


add_public_key()
{
    publicKey="unlessbamboo.pub"
    privateKey="unlessbamboo"
    sshKeyDir="$HOME/.ssh/"
    sshAuthorized="${sshKeyDir}/authorized_keys"

    if [[ ! -f "${publicKey}" ]];then
        err "Not exists ${publicKey} filename."
    fi

    cat ${publicKey} >> ${sshAuthorized}
    if [[ $? != 0 ]];then
        err "Add publich key to ${sshAuthorized} failed."
    fi

}


modify_permission()
{
    sshKeyDir="$HOME/.ssh/"
    publicKey="${sshKeyDir}/unlessbamboo.pub"
    privateKey="${sshKeyDir}/unlessbamboo"

    if [[ -f ${privateKey} ]];then
        chmod 600 ${privateKey}
        if [[ $? != 0 ]];then
            err "Modify file ${privateKey} permissions failed."
        fi
    fi

    if [[ -f ${publicKey} ]];then
        chmod 644 ${publicKey}
        if [[ $? != 0 ]];then
            err "Modify file ${publicKey} permissions failed."
        fi
    fi
}


ssh_key_init
add_public_key
modify_permission
