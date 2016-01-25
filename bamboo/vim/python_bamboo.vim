""""""""""""""""""""""""""""""""""""""""""""""""
" Python语言tags 路径设置
""""""""""""""""""""""""""""""""""""""""""""""""""
"if has("tags")                                  
    "set tags+=tags,/usr/lib/python2.6/tags,usr/lib64/python2.6/tags
"else
    "set tags=tags,/usr/lib/python2.6/tags,usr/lib64/python2.6/tags
"endif
if has("tags")                                  
    set tags+=tags,/usr/local/python/lib/python2.7
else
    set tags=tags,/usr/local/python/lib/python2.7
endif
