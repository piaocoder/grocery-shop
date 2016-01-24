#!/bin/bash - 
#===============================================================================
#
#          FILE: nginxinstall.sh
# 
#         USAGE: ./nginxinstall.sh 
# 
#   DESCRIPTION: Adds the special nginx-third-part packages embedded in nginx code
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: unlessbamboo (?), unlessbamboo@gmail.com
#  ORGANIZATION: 
#       CREATED: 01/24/2016 01:02
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
    local   stdfile="/data/logs/shell.log"
    if [[ ! -f "${stdfile}" ]];then
        touch "${stdfile}"
    fi
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@"
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@" >>"${stdfile}"
    exit 1
}


#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  test_env
#   DESCRIPTION:  test environment
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
test_env()
{
    ROOT_DIR="~/Downloads/"
    PREFIX_DIR="/apps/nginx"
    MODULE_SRC="filter.tar.gz"
    NGINX_SRC="tengine-2.0.3.tar.gz"

    cd "${ROOT_DIR}"
    if [[ $? != 0 ]]; then
        err "解压${ROOT_DIR}失败."
    fi

    if [[ ! -f "${MODULE_SRC}" ]];then
        err "不存在目录${MODULE_SRC}。"
    fi

    if [[ ! -f "${NGINX_SRC}" ]];then
        err "不存在目录${NGINX_SRC}。"
    fi

    if [[ ! -d "${PREFIX_DIR}" ]]; then
        err "不存在目录${PREFIX_DIR}。"
    fi
}

install_pkg()
{
    readonly ROOT_DIR="~/Downloads/"
    PREFIX_DIR="/apps/nginx"
    MODULE_SRC="filter.tar.gz"
    NGINX_SRC="tengine-2.0.3.tar.gz"
    MODULE_DIR="filter"
    NGINX_DIR="tengine"

    cd "${ROOT_DIR}"
    
    tar zxf "${NGINX_SRC}"
    if [[ $? != 0 ]]; then
        err "解压${NGINX_SRC}失败."
    fi

    tar zxf "${MODULE_SRC}"
    if [[ $? != 0 ]]; then
        err "解压${MODULE_SRC}失败."
    fi

    if [[ ! -d "${NGINX_DIR}" ]];then
        err "解压后为发现目录${NGINX_DIR}."
    fi

    if [[ ! -d "${MODULE_DIR}" ]];then
        err "解压后为发现目录${MODULE_DIR}."
    fi

    cd "${NGINX_DIR}"
    ./configure --prefix="${PREFIX_DIR}" \
        --add-module=${ROOT_DIR}/${MODULE_DIR} && \
        make && sudo make install
    if [[ $? != 0 ]]; then
        err "编译nginx失败."
    fi
    cd -

    sudo /etc/init.d/nginx restart 
    if [[ $? != 0 ]]; then
        err "重启nginx进程失败."
    fi

    cd -
}


#-------------------------------------------------------------------------------
# case command
#-------------------------------------------------------------------------------
case ${1} in
    test)
        test_env;;

    install)
        test_env;
        install_pkg;;

    *)
        test_env;;

esac    # --- end of case ---
