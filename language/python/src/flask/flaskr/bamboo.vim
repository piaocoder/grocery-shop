" C/python语言tags 路径设置
" 根据不同的python版本生成不同的bamboo文件
if has("tags")
    set tags+=tags,/usr/lib/gcc/tags,/usr/include/tags,/usr/local/include/tags
    set tags+=../venv/tags
else
    set tags=tags,/usr/lib/gcc/tags,/usr/include/tags,/usr/local/include/tags
    set tags+=/lib/python2.7/tags
    set tags+=../venv/tags
endif
