""""""""""""""""""""""""""""""""""""""""""""""""
" Python语言tags 路径设置
""""""""""""""""""""""""""""""""""""""""""""""""""
if has("tags")                                  
    set tags+=tags,/usr/lib/python2.7/tags,usr/lib64/python2.7/tags
else
    set tags=tags,/usr/lib/python2.7/tags,usr/lib64/python2.7/tags
endif
