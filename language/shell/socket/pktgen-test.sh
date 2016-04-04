#!/bin/bash - 
#===============================================================================
#
#          FILE: pktgen-test.sh
# 
#         USAGE: ./pktgen-test.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 2016年04月01日 11:05
#      REVISION:  ---
#===============================================================================
set -o nounset                              # Treat unset variables as an error


#modprobe pktgen
if [[ `lsmod | grep pktgen` == "" ]];then
   modprobe pktgen
fi

if [[ $1 == "" ]];then
   pktsize=550
else
   pktsize=$1
fi


function pgset() {
    local result

    echo $1 > $PGDEV

    result=`cat $PGDEV | fgrep "Result: OK:"`
    if [ "$result" = "" ]; then
         cat $PGDEV | fgrep Result:
    fi
}


function pg() {
    echo inject > $PGDEV
    cat $PGDEV
}


# On UP systems only one thread exists -- so just add devices
# We use eth0, eth0
echo "Adding devices to run".
PGDEV=/proc/net/pktgen/kpktgend_0
# 删除该线程0上的所有端口，并将eth0绑定到线程0上面
pgset "rem_device_all"
pgset "add_device eth0"
pgset "max_before_softirq 1"

# Configure the individual devices
echo "Configuring devices"


PGDEV=/proc/net/pktgen/eth0
pgset "count 100000"
pgset "clone_skb 100000"
pgset "pkt_size $pktsize"
#pgset "src_mac A0:36:9F:7B:2D:84"
pgset "src_mac 40:8d:5c:a9:0a:f4"
pgset "flag IPSRC_RND"

# dst为最终的目的地址
pgset "dst 192.168.199.155"
# 通过l2fwd的输出显示可以查看和了解mac地址
#pgset "dst_mac A0:36:9F:7B:6D:50"
pgset "dst_mac 9C:5C:8E:C0:4E:D7"

echo "Note，pkgsize:$pktsize"
echo "Running... ctrl^C to stop"

# Time to run
# 所有的线程开始发送数据
PGDEV=/proc/net/pktgen/pgctrl
pgset "start"

echo "Done"
