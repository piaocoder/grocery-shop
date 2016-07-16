#!/bin/zsh - 
#===============================================================================
#
#          FILE: session.sh
# 
#         USAGE: ./session.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2016年07月03日 23:41
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

#SESSIONNAME="script"

session()
{
    sessionname=$1
    tmux has-session -t $sessionname &> /dev/null

    if [ $? != 0 ] 
     then
        tmux new-session -s $sessionname -n script -d
        tmux send-keys -t $sessionname "~/bin/script" C-m 
    fi

    tmux attach -t $sessionname
}

session $1
