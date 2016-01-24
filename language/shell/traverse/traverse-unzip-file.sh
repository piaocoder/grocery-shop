#!/bin/sh

# è§£åç¼©
unzip()
{
    find ./ -name '*.tar.gz' | while read fname
    do
        echo "è§£åæä»¶:$fname"
        tar zxf $fname
    done

    find ./ -name '*.zip' | while read fname
    do
        echo "è§£åæä»¶:$fname"
        unzip $fname
    done
}

# å®è£pythonæ¨¡å
install()
{
    for dir in `ls`
    do
        if [ -d $dir ];then
            cd $dir
            python setup.py install --user
            cd ..
        fi
    done
}


case "$1" in
    normal)
        unzip
        install
        ;;
    *)
        echo "Usage: $0 {normal}"
        exit 1;
esac
