#!/bin/bash - 
#===============================================================================
#
#          FILE: backup.sh
# 
#         USAGE: ./backup.sh 
# 
#   DESCRIPTION: 备份系统，请以root身份执行，目前设定为备份到
#                   移动硬盘上。
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2016年12月08日 12:18
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error


# 备份
tar vzcpf \
    /media/bamboo/backup/ubuntu_`date +%Y%m%d_%H`.tar.gz \
    --exclude=/proc --exclude=/dev --exclude=/mnt \
    --exclude=/media --exclude=/lost+found \
    --exclude=/cdrom --exclude=/tmp --exclude=/sys \
    --exclude=/home/bamboo/.cache --exclude=/run / \
    > /media/bamboo/backup/ubuntu_`date +%Y%m%d_%H`.log \
    2> /media/bamboo/backup/ubuntu_`date +%Y%m%d_%H`.error


# 恢复
resume()
{
    # 先备份/boot和/etc/fstab
    # 之后解压缩
    su - root
    tar vxzpf ubuntu.tar.gz -C /
}
