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
source /data/shell/base.sh

set -o nounset                              # Treat unset variables as an error



ssh_key_init()
{
    sshKeyDir="$HOME/.ssh/"

    which ssh-keygen
    if [[ $? != 0 ]];then
        sudo aptitude install ssh
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


ssh_key_init
add_public_key
