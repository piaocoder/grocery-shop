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

set -o nounset                              # Treat unset variables as an error
set -x

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
#          NAME:  update_bash_profile
#   DESCRIPTION:  更新shell的基本配置信息
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
update_bash_profile()
{
    src_file="bash_profile"
    dst_file="${HOME}/.bash_profile"
    target_dir="shell"
    
    if [[ ! -d "${target_dir}" ]];then
        err "Not exists ${target_dir}."
    fi
    cd "${target_dir}"
    pwd

    cp "${src_file}" "${dst_file}" -rf
    if [[ $? != 0 ]];then
        err "Copy ${src_file} to ${dst_file} failed."
    fi

    cd -
}

#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  update_filenametags
#   DESCRIPTION:  Cp filenametags to /home/bin. 
#                 It will to be used generate tags.
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
update_filenametags()
{
    src_file="filenametags"
    dst_file="/home/bin/filenametags"
    target_dir="shell"
    
    if [[ ! -d "${target_dir}" ]];then
        err "Not exists ${target_dir}."
    fi
    cd "${target_dir}"
    pwd

    cp "${src_file}" "${dst_file}" -rf
    if [[ $? != 0 ]];then
        err "Copy ${src_file} to ${dst_file} failed."
    fi

    cd -
}

#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  update_bash_profile
#   DESCRIPTION:  更新vim的编程设置，不包括vimrc
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
update_vim_profile()
{
    target_dir="vim"
    gcc_file="gcc*.vim"
    union_file="union*.vim"
    python_file="python*.vim"
    gcc_dir="${HOME}/grocery-shop/language/gcc/"
    python_dir="${HOME}/grocery-shop/language/python/"
    job_dir="${HOME}/work/job/jobdev/"

    if [[ ! -d "${target_dir}" ]];then
        err "Not exists ${target_dir}."
    fi
    cd "${target_dir}"

    if [[ ! -d "${gcc_dir}" || ! -d "${python_dir}" || \
        ! -d "${job_dir}" ]];then
        err "Not exists directory:${gcc_dir} or ${python_dir} or ${job_dir}"
    fi
    
    # gcc
    cp ${gcc_file} "${gcc_dir}/bamboo.vim" -rf
    if [[ $? != 0 ]];then
        err "Copy ${gcc_file} to ${gcc_dir} failed."
    fi

    # python
    cp ${python_file} "${python_dir}/bamboo.vim" -rf
    if [[ $? != 0 ]];then
        err "Copy ${python_file} to ${python_dir} failed."
    fi

    # union
    cp ${union_file} "${job_dir}/bamboo.vim" -rf
    if [[ $? != 0 ]];then
        err "Copy ${union_file} to ${job_dir} failed."
    fi

    cd -
}


#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  initialize_env
#   DESCRIPTION:  初始化所有的工作环境，执行env下所有的shell脚本
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
initialize_env()
{
    TARGET_DIR=env

    if [[ ! -d "${TARGET_DIR}" ]];then
        err "Not exists ${TARGET_DIR}."
    fi
    cd ${TARGET_DIR}
    pwd

    shellList=$(ls)
    for file in "${shellList}";do
        bash "${file}"
        if [[ $? != 0 ]];then
            err "Execute ${file} scripts failed."
        fi
    done

    cd -
}


main()
{
    initialize_env

    update_bash_profile
    update_filenametags

    update_vim_profile
}
main
