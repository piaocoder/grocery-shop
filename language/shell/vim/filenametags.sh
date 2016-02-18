#!/bin/bash - 
#===============================================================================
#
#          FILE: test.sh
# 
#         USAGE: ./test.sh 
# 
#   DESCRIPTION: 生成tags值以便lookupfile插件使用
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: unlessbamboo (?), unlessbamboo@gmail.com
#  ORGANIZATION: 
#       CREATED: 2016年01月15日 15:56
#      REVISION:  ---
#===============================================================================

set -o nounset          # Treat unset variables as an error

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

generateTags()
{
    # generate tag file for lookupfile plugin
    echo -e "!_TAG_FILE_SORTED\t2\t/2=foldcase/" > filenametags
    find . -not -regex '.*\.\(png\|gif\|pyc\|jpg\|js\|css\)' \
        -not -regex '.*\.\(ttf\|html\|class\|pyc\|pyo\)' \
        -not -regex '.*\.\(swp\|swo\)' \
        -not -iwholename '*.svn*' \
        -type f -printf "%f\t%p\t1\n" | \
        sort -f >>filenametags
}

generateTags
