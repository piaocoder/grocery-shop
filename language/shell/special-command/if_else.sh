#!/bin/sh

# æµè¯ä¸æå½ä»¤[
if [ 0 ];then
    echo "0 is true"
else
    echo "0 is false"
fi

if [ -1 ]; then
    echo "-1 is true"
else
    echo "-1 is false"
fi

if [ 1 ]; then
    echo "1 is true"
else
    echo "1 is false"
fi


if [  ]; then
    echo "NULL is true"
else
    echo "NULL is false"
fi

if [ $false ]; then
    echo "false is true"
else
    echo "false is false"
fi

if [ $true ]; then
    echo "true is true"
else
    echo "true is true"
fi

if [ 400>=5050 ]; then
    echo "((0)) is true"
else
    echo "((0)) is false"
fi

if [ $1 = 'test' ]; then
    echo "compare parameter of first"
fi

if [ $1 != 'test' ]; then
    echo "compare parameter of first not equal to destination"
fi
