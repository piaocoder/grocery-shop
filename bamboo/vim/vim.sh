#!/bin/bash - 
#===============================================================================
#
#          FILE: vim.sh
# 
#         USAGE: ./vim.sh 
# 
#   DESCRIPTION: vim相关配置
#           1，初始化vim相关环境
#           2，拷贝相应file.vim到相应目录，实现个性化vim（后期建议杀出）
#           3，自动化部署.vim目录
#           4，govim见local/bin目录
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2016年08月19日 08:57
#      REVISION:  ---
#===============================================================================

#include 
. ../env/base.sh


#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  vim_config_init
#   DESCRIPTION:  执行vim目录下的脚本，进行.vim文件的初始化
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
vim_config_init()
{
    which python-config
    if [[ $? != 0 ]];then
        sudo aptitude install python-dev
        if [[ $? != 0 ]];then
            err "Install python-dev failed."
        fi
    fi
    which python3-config
    if [[ $? != 0 ]];then
        sudo aptitude install python3-dev
        if [[ $? != 0 ]];then
            err "Install python3-dev failed."
        fi
    fi
    tags_file="generate-tags.py"
    $(python ${tags_file})
    if [[ $? != 0 ]];then
        err "Execute ${tags_file} scripts failed."
    fi
}

#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  update_vim_profile
#   DESCRIPTION:  更新vim的编程设置，不包括vimrc
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
update_vim_profile()
{
    gcc_file="gcc*.vim"
    union_file="union*.vim"
    python_file="python*.vim"
    gcc_dir="${HOME}/grocery-shop/language/gcc/"
    python_dir="${HOME}/grocery-shop/language/python/"
    job_dir="${HOME}/work/job/ossdev/"
    algo_dir="${HOME}/grocery-shop/algorithm/"
    data_construct_dir="${HOME}/grocery-shop/data-structure/"

    # gcc
    if [[ -d "${gcc_dir}" ]];then
        cp -rf ${gcc_file} "${gcc_dir}/bamboo.vim"
        if [[ $? != 0 ]];then
            err "Copy ${gcc_file} to ${gcc_dir} failed."
        fi
    fi

    # python
    if [[ -d "${python_dir}" ]];then
        cp -rf ${python_file} "${python_dir}/bamboo.vim"
        if [[ $? != 0 ]];then
            err "Copy ${python_file} to ${python_dir} failed."
        fi
    fi

    # union
    if [[ -d "${job_dir}" ]];then
        cp -rf ${union_file} "${job_dir}/bamboo.vim"
        if [[ $? != 0 ]];then
            err "Copy ${union_file} to ${job_dir} failed."
        fi
    fi

    if [[ -d "${algo_dir}" ]];then
        cp -rf ${union_file} "${algo_dir}/bamboo.vim"
        if [[ $? != 0 ]];then
            err "Copy ${union_file} to ${algo_dir} failed."
        fi
    fi

    if [[ -d "${data_construct_dir}" ]];then
        cp -rf ${union_file} "${data_construct_dir}/bamboo.vim"
        if [[ $? != 0 ]];then
            err "Copy ${union_file} to ${data_construct_dir} failed."
        fi
    fi
}


# init
vim_config_init
update_vim_profile
