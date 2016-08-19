#!/bin/bash - 
#===============================================================================
#
#          FILE: env.sh
# 
#         USAGE: ./env.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2016年08月19日 07:58
#      REVISION:  ---
#===============================================================================
# include
. base.sh


ENV_G_CUR_PATH=$(cd $(dirname $0);pwd)
if [[ $? != 0 ]];then
    err "Set absolute path failed!"
fi


#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  upate_ld_config
#   DESCRIPTION:  更新ldconfig文件，添加新的链接库
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
update_ld_config()
{
    srcFile="shitserver-x86_64.conf"
    dstFile="/etc/ld.so.conf.d/shitserver-x86_64.conf"

    if [[ ! -f ${srcFile} ]];then
        err "Not exists ${srcFile}"
    fi
    cp "${srcFile}" "${dstFile}" -rf
    if [[ $? != 0 ]];then
        err "Copy ${srcFile} to ${dstFile} failed."
    fi

    # 执行ldconfig，将新的路径载入高速缓存中
    ldconfig

}


#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  update_filenametags
#   DESCRIPTION:  Cp filenametags to .local/bin/. 
#                 It will to be used generate tags.
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
update_filenametags()
{
    srcFile="filenametags"
    dstFile="${HOME}/.local/bin/filenametags"
    
    absolute_path="${ENV_G_CUR_PATH}/${srcFile}"
    if [[ ! -f ${absolute_path} ]];then
        err "Not exists ${absolute_path}"
    fi

    ln -sf ${absolute_path} ${dstFile}
    if [[ $? != 0 ]];then
        err "Link ${srcFile} to ${dstFile} failed."
    fi
}


#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  update_bamboo_profile
#   DESCRIPTION:  更新shell的基本配置信息
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
update_bamboo_profile()
{
    srcFile=".bamboo_profile"
    dstFile="${HOME}/.bamboo_profile"
    absolute_path="${ENV_G_CUR_PATH}/${srcFile}"

    if [[ ! -f ${absolute_path} ]];then
        err "Not exists ${absolute_path} file."
    fi
    ln -sf ${absolute_path} ${dstFile}
    if [[ $? != 0 ]];then
        err "Link ${srcFile} to ${dstFile} failed."
    fi
}


update_base_header()
{
    shellDir="/data/shell/"
    baseFile="base.sh"
    
    ln -sf ${ENV_G_CUR_PATH}/${baseFile} ${shellDir}
    if [[ $? != 0 ]];then
        err "Link ${baseFile} failed."
    fi
}



main()
{
    update_bamboo_profile
    update_filenametags
    update_base_header
}


case "$1" in
    normal)
        main;;
    ld)
        update_ld_config;;
    *)
        main;;
esac
