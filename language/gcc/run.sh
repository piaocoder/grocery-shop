#!/bin/sh

make_func()
{
    if [ -d "/data/dump/" ];then
        rm -rf /data/dump/*
    fi
    make clean
    python compile.py
    make && make install
    if [ $? -ne 0 ];then
        echo "Compile code occur error++++++++++"
        exit $?
    fi
}

start_func()
{
    make_func
    for i in $(seq 1) 
    do 
        /apps/boserver/bin/boserver
        if [ $? -ne 0 ] 
        then
            break
        fi
    done
}

case $1 in
    make)
        make_func
        ;;
    restart)
        start_func
        ;;
    *)
        start_func
        ;;
esac
