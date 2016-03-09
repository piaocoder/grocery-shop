#!/bin/sh

make_func()
{
    make clean
    make
    rm -rf /data/dump/*
    ls /data/dump/
}

start_func()
{
    make clean
    make
    rm -rf /data/dump/*
    for i in $(seq 1) 
    do 
        ./boserver
        if [ $? -ne 0 ] 
        then
            break
        fi
    done
    ls /data/dump/
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
