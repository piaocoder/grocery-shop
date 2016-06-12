#!/bin/sh
/**
* @file rename.sh
* @brief    rename all .txt to .log
* @author unlessbamboo
* @version 1.0
* @date 2016-05-17
*/


result=`find ./ -name "*.txt"`
for i in $result
do
    mv $i ${i%$1}$2
done
