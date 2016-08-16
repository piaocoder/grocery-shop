" Python语言tags 路径设置
" 根据不同的python版本生成不同的bamboo文件
if has("tags")
    set tags+=tags,/usr/lib/python2.7/tags
else
    set tags=tags,/usr/lib/python2.7/tags
endif
