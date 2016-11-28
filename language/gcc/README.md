1,The step of install package:
    1,Set shell env:
        export BO_DIR=`pwd`
    
    2,Set execute environment
        1) look chapter 3 and sure all dependency library are 
            installed.
        2) mkdir some directories.
            python compile.py

    3,compile and install:
        make
        sudo make install

    4,When you execute binary files at sub-directory, you may be 
        occur error:Can not find share library. So you must be 
        set LIBRARY_PATH or ldconfig

2,Default,all execute package will be copy into bin/ 
    or /apps/$(package)/bin/,go it.


3,Dependency library:
    libev:
        Ubuntu: sudo aptitude install libev-dev

    python：
        Default install, python's version is python2.6. if
        your python's version is different from this, you 
        must be change some Makefile, just do it.

    openssl:
        Ubuntu: sudo aptitude install libssl-dev

    libxml2, libxst:
        Ubuntu: sudo aptitude install libxml2-dev libxslt1-dev 

    mysql header and libs:
        Ubuntu: sudo aptitude install libmysql++-dev

    pcre libs:
        Ubuntu: sudo aptitude install libpcre++-dev
