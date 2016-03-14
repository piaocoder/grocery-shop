" C/python语言tags 路径设置
" 根据不同的python版本生成不同的bamboo文件
if has("tags")
    set tags+=tags,/usr/lib/gcc/tags,/usr/include/tags,/usr/local/include/tags
    set tags+=tags,/usr/lib/python2.7/tags,/usr/lib64/python2.7/tags
else
    set tags=tags,/usr/lib/gcc/tags,/usr/include/tags,/usr/local/include/tags
    set tags=tags,/usr/lib/python2.7/tags,/usr/lib64/python2.7/tags
endif

" C语言path 路径设置
set path+=.,/usr/include/,/usr/lib/gcc,/usr/local/include
