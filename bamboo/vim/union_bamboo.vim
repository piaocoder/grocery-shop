""""""""""""""""""""""""""""""""""""""""""""""""
" C/python语言tags 路径设置
""""""""""""""""""""""""""""""""""""""""""""""""
if has("tags")                                                                
    set tags+=tags,/usr/lib/gcc/tags,/usr/include/tags,/usr/local/include/tags
    set tags+=tags,/usr/local/python/lib/python2.7
else
    set tags=tags,/usr/lib/gcc/tags,/usr/include/tags,/usr/local/include/tags
    set tags=tags,/usr/local/python/lib/python2.7
endif
                                                                              
""""""""""""""""""""""""""""""""""""""""""""""""
" C语言path 路径设置
""""""""""""""""""""""""""""""""""""""""""""""""
set path+=.,/usr/include/,/usr/lib/gcc,/usr/local/include
