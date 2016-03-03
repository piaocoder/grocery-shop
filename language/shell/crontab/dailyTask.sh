#!/bin/bash - 
#===============================================================================
#
#          FILE: dailyTask.sh
# 
#         USAGE: ./dailyTask.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: unlessbamboo (?), unlessbamboo@gmail.com
#  ORGANIZATION: 
#       CREATED: 2016年01月13日 16:08
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an err

#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  err
#   DESCRIPTION:  display err msg
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
err()                                               
{
    local   stdfile="/data/logs/crontab.log"
    if [[ ! -f "${stdfile}" ]];then
        touch "${stdfile}"
    fi
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@"
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@" >>"${stdfile}"
    exit 1
}

#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  tar_grocery_shop
#   DESCRIPTION:  压缩grocery_shop文件，生成grocery_shop-2016-01-01.tar.gz格式
#    PARAMETERS:  
#       RETURNS:  true or false
#-------------------------------------------------------------------------------
tar_grocery_shop()
{
    local   parent_dir="/tmp/"
    local   src_dir="grocery-shop"
    local   src_path=$(cd ~/grocery-shop;pwd)
    local   dst_path="/mnt/hgfs/download/share"
    local   tar_file="grocery_shop-$(date +'%Y-%m-%d').tar.gz"

    if [[ ! -d ${src_path} || ! -d ${dst_path} ]];then
        err "不存在目录${src_path} 或者 ${dst_path}."
    fi

    cp ${src_path} ${parent_dir} -rf

    cd "${parent_dir}" && tar zcf "${tar_file}" "${src_dir}"
    if [[ $? != 0 ]];then
        err "压缩文件失败."
    fi
    
    mv "${tar_file}" "${dst_path}"
    if [[ $? != 0 ]];then
        err "移动文件失败."
    fi

    cd -
}


#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  tar_vim
#   DESCRIPTION:  压缩.vim .vimrc文件，生成vim-2016-01-01.tar.gz格式
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
tar_vim()
{
    local   parent_dir=$(cd ~;pwd)
    local   src1_dir=".vim/"
    local   src2_file=".vimrc"
    local   dst_dir="/mnt/hgfs/download/share/"
    local   tar_file="vim-$(date +'%Y-%m-%d').tar.gz"

    cd "${parent_dir}"
    if [[ $? != 0 ]];then
        err "进入用户根目录失败."
    fi

    if [[ ! -d "${src1_dir}" || ! -d "${dst_dir}" ]];then
        err "不存在目录${src1_dir} 或者 ${dst_dir}."
        exit 1
    fi

    tar zcf "${tar_file}" "${src1_dir}" "${src2_file}"
    if [[ $? != 0 ]];then
        err "压缩文件失败."
    fi
    
    mv "${tar_file}" "${dst_dir}"
    if [[ $? != 0 ]];then
        err "移动文件失败."
    fi

    cd -
}

main()
{
    tar_grocery_shop
    tar_vim
}

main
