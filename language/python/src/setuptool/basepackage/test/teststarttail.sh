#!/bin/bash - 
#===============================================================================
#
#          FILE: starttail.sh
# 
#         USAGE: ./starttail.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#      REVISION:  ---
#===============================================================================


# write
python basepackage/test/writetaillog.py > time1.log & 2>&1

# read old
python basepackage/test/testtaillog-old.py > time2.log & 2>&1

# read pyinotify
python basepackage/test/testtaillog.py > time3.log & 2>&1

# read subprocess
#python basepackage/test/testtaillog-suprocess.py > time4.log & 2>&1

# read select
#python basepackage/test/testtaillog-select.py > time5.log & 2>&1
