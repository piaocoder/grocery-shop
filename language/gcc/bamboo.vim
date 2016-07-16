""""""""""""""""""""""""""""""""""""""""""""""""
" C语言tags 路径设置
""""""""""""""""""""""""""""""""""""""""""""""""
if has("tags")
    set tags+=tags,/usr/lib/gcc/tags,/usr/include/tags,/usr/local/include/tags
    set tags+=/data/tags/headers-tags,/data/tags/system-tags
else
    set tags=tags,/usr/lib/gcc/tags,/usr/include/tags,/usr/local/include/tags
    set tags+=/data/tags/headers-tags,/data/tags/system-tags
endif

""""""""""""""""""""""""""""""""""""""""""""""""
" C语言path 路径设置
""""""""""""""""""""""""""""""""""""""""""""""""
set path+=.,/usr/include/,/usr/lib/gcc,/usr/local/include

