#!/bin/bash - 
#===============================================================================
#
#          FILE: install.sh
# 
#         USAGE: ./install.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: unlessbamboo (?), unlessbamboo@gmail.com
#  ORGANIZATION: 
#       CREATED: 2016年01月25日 10:21
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

cp dailyTask.sh /home/bin
cp github.tar.gz github_tar.sh /home/bin

