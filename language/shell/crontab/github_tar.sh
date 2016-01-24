#!/bin/bash - 
#===============================================================================
#
#          FILE: github_tar.sh
# 
#         USAGE: ./github_tar.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: unlessbamboo (?), unlessbamboo@gmail.com
#  ORGANIZATION: 
#       CREATED: 01/24/2016 04:08
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

cd /home/bin/
tar zxf github.tar.gz
bash github_check.sh
rm github_check.sh
