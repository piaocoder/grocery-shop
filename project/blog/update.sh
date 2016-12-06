#!/bin/bash - 
#===============================================================================
#
#          FILE: update.sh
# 
#         USAGE: ./update.sh 
# 
#   DESCRIPTION: 更新所有markdown文件，并部署新的网站到服务器上
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2016年12月06日 16:05
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error


BLOGZIP="blog.tar.gz"
BLOGPARENT="${HOME}/Public/"
BLOGDIR="${HOME}/Public/blog/"


copy_md() 
#---  FUNCTION  ----------------------------------------------------------------
#          NAME:  copy_md
#   DESCRIPTION:  该函数会删除~/Public/blog文件夹，请注意
#    PARAMETERS:  
#       RETURNS:  
#-------------------------------------------------------------------------------
{
    # 解压缩
    if [[ ! -f ${BLOGZIP} ]];then
        echo "Not found ${BLOGZIP}."
        exit -1
    fi

    rm -rf ${BLOGDIR} && tar zxf ${BLOGZIP} -C ${BLOGPARENT}
    if [[ $? != 0 ]];then
        echo "unzip ${BLOGZIP} failed."
        exit -1
    fi

    declare temppost="${BLOGDIR}/source/_posts/"
    if [[ ! -d ${temppost} ]];then
        echo "Not found ${temppost}."
        exit -1
    fi

    # come in
    cd ${temppost}

    # copy markdown
    ls $mygcc/doc/* | xargs -i ln -f {} .
    if [[ $? != 0 ]];then
        echo "Copy gcc markdown failed."
        exit -1
    fi
    ls ${HOME}/grocery-shop/knowledge/vim/* | xargs -i ln -f {} .
    if [[ $? != 0 ]];then
        echo "Copy vim markdown failed."
        exit -1
    fi

    # come out
    cd -
}


hexo_upload()
{
    # come in
    cd ${BLOGDIR}

    # 进行hexo操作
    hexo clean
    hexo g --silent
    if [[ $? != 0 ]];then
        echo "hexo genearte failed."
        exit -1
    fi
    hexo d --silent
    if [[ $? != 0 ]];then
        echo "hexo deploy failed."
        exit -1
    fi

    # 后续清理工作
    hexo clean
    cd -
}


teardown()
{
    # come in
    cd ${BLOGPARENT}
    tar zcf ${BLOGZIP} blog
    if [[ $? != 0 ]];then
        echo "zip file failed."
        exit -1
    fi
    # come out
    cd -

    # move tar.gz
    rm -rf ${BLOGZIP}
    mv ${BLOGPARENT}/${BLOGZIP} .
}



copy_md
hexo_upload
teardown
echo
echo "xxxxxxxxxxxxxxxxxxxxxxSuccessfulxxxxxxxxxxxxxxxxxx"
echo
