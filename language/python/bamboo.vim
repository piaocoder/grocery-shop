" Python语言tags 路径设置
" 根据不同的python版本生成不同的bamboo文件
if has("tags")
    set tags+=tags,/usr/lib/python2.7/tags
    set tags+=/data/virtualenv/logparse/lib/python2.7/tags
    set tags+=/usr/local/levelDB/include/tags
    set tags+=/usr/src/linux-headers-4.2.0-35/tags,/usr/include/tags
else
    set tags=tags,/usr/lib/python2.7/tags
    set tags+=/data/virtualenv/logparse/lib/python2.7/tags
    set tags+=/usr/local/levelDB/include/tags
    set tags+=/usr/src/linux-headers-4.2.0-35/tags,/usr/include/tags
endif


" syntastic路径查找设置
"
let g:syntastic_c_include_dirs = ['include', 
            \ 'src',
            \ '/usr/local/levelDB/include',
            \ '/usr/local/BerkeleyDB.4.8/include',
            \ '/home/bamboo/work/dpdns/log-analysis/'
            \]
let g:syntastic_cpp_include_dirs = ['include', 
            \ 'src',
            \ '/usr/local/levelDB/include',
            \ '/usr/local/BerkeleyDB.4.8/include',
            \ '/home/bamboo/work/dpdns/log-analysis'
            \]
let b:syntastic_c_cflags = '-I/usr/local/BerkeleyDB.4.8/include
            \ -I/usr/local/levelDB/include '
let b:syntastic_cpp_cflags = '-I/usr/local/BerkeleyDB.4.8/include
            \ -I/usr/local/levelDB/include '
