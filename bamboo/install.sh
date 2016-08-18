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

#set -o nounset                              # Treat unset variables as an error
set -x

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

G_CUR_PATH=$(cd $(dirname $0);pwd)
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
    src_file="shitserver-x86_64.conf"
    dst_file="/etc/ld.so.conf.d/shitserver-x86_64.conf"
    target_dir="shell"

    if [[ ! -d "${target_dir}" ]];then
        err "Not exists ${target_dir}."
    fi
    cd "${target_dir}"

    if [[ ! -f ${src_file} ]];then
        err "Not exists ${src_file}"
    fi
    cp "${src_file}" "${dst_file}" -rf
    if [[ $? != 0 ]];then
        err "Copy ${src_file} to ${dst_file} failed."
    fi

    # 执行ldconfig，将新的路径载入高速缓存中
    ldconfig

    cd -
}

#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  update_bamboo_profile
#   DESCRIPTION:  更新shell的基本配置信息
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
update_bamboo_profile()
{
    src_file=".bamboo_profile"
    dst_file="${HOME}/.bamboo_profile"
    target_dir="shell"
    
    if [[ ! -d "${target_dir}" ]];then
        err "Not exists ${target_dir}."
    fi
    cd ${target_dir}

    absolute_path="${G_CUR_PATH}/${target_dir}/${src_file}"
    if [[ ! -f ${absolute_path} ]];then
        err "Not exists ${absolute_path}"
    fi
    ln -sf ${absolute_path} ${dst_file}
    if [[ $? != 0 ]];then
        err "Link ${src_file} to ${dst_file} failed."
    fi

    cd -
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
    src_file="filenametags"
    dst_file="${HOME}/.local/bin/filenametags"
    target_dir="shell"
    
    if [[ ! -d "${target_dir}" ]];then
        err "Not exists ${target_dir}."
    fi
    cd ${target_dir}

    absolute_path="${G_CUR_PATH}/${target_dir}/${src_file}"
    if [[ ! -f ${absolute_path} ]];then
        err "Not exists ${absolute_path}"
    fi
    ln -sf ${absolute_path} ${dst_file}
    
    if [[ $? != 0 ]];then
        err "Link ${src_file} to ${dst_file} failed."
    fi

    cd -
}

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
    target_dir="vim"
    gcc_file="gcc*.vim"
    union_file="union*.vim"
    python_file="python*.vim"
    gcc_dir="${HOME}/grocery-shop/language/gcc/"
    python_dir="${HOME}/grocery-shop/language/python/"
    job_dir="${HOME}/work/job/ossdev/"
    algo_dir="${HOME}/grocery-shop/algorithm/"
    data_construct_dir="${HOME}/grocery-shop/data-structure/"

    if [[ ! -d "${target_dir}" ]];then
        err "Not exists ${target_dir}."
    fi
    cd "${target_dir}"

    # init
    vim_config_init

    # gcc
    if [[ -d "${gcc_dir}" ]];then
        cp ${gcc_file} "${gcc_dir}/bamboo.vim" -rf
        if [[ $? != 0 ]];then
            err "Copy ${gcc_file} to ${gcc_dir} failed."
        fi
    fi

    # python
    if [[ -d "${python_dir}" ]];then
        cp ${python_file} "${python_dir}/bamboo.vim" -rf
        if [[ $? != 0 ]];then
            err "Copy ${python_file} to ${python_dir} failed."
        fi
    fi

    # union
    if [[ -d "${job_dir}" ]];then
        cp ${union_file} "${job_dir}/bamboo.vim" -rf
        if [[ $? != 0 ]];then
            err "Copy ${union_file} to ${job_dir} failed."
        fi
    fi

    if [[ -d "${algo_dir}" ]];then
        cp ${union_file} "${algo_dir}/bamboo.vim" -rf
        if [[ $? != 0 ]];then
            err "Copy ${union_file} to ${algo_dir} failed."
        fi
    fi

    if [[ -d "${data_construct_dir}" ]];then
        cp ${union_file} "${data_construct_dir}/bamboo.vim" -rf
        if [[ $? != 0 ]];then
            err "Copy ${union_file} to ${data_construct_dir} failed."
        fi
    fi

    cd -
}



update_local()
{
    local localDir="local"
    local localBash="local.sh"
    
    if [[ ! -d ${localDir} ]];then
        err "Not exists ${localDir}."
    fi

    cd ${localDir}
    if [[ -f ${localBash} ]];then
        bash ${localBash}
        if [[ $? != 0 ]];then
            err "Execute ${localBash} failed."
        fi
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
    DATA_DIR=/data/
    DATA_DIR_LOG=/data/log/

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

    if [[ ! -d ${DATA_DIR_LOG} ]];then
        mkdir ${DATA_DIR_LOG}
        if [[ $? != 0 ]];then
            err "Mkdir ${DATA_DIR_LOG} failed."
        fi
    fi

    if [[ ! -d "${TARGET_DIR}" ]];then
        err "Not exists ${TARGET_DIR}."
    fi
    cd ${TARGET_DIR}

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

    update_bamboo_profile
    update_filenametags
    update_local

    update_vim_profile
}

case "$1" in
    normal)
        main;;
    ldconfig)
        update_ld_config;;
    *)
        main;;
esac
