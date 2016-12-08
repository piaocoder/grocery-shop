---
title: Synstatic的配置  
date:  2016-10-17 23:00:00  
tags: vim  
---


欢迎来到狂想的个人实验室。  
github：[unlessbamboo](https://github.com/unlessbamboo)


### 1 命令说明
```vim
    " 显示当前的状态(激活还是禁用)/可用的checkers
    SyntasticInfo
    " 手动调用语法检查.默认错误信息不会输出到 quickfix
    SyntasticCheck
    " 错误输出到 quickfix, 并拉起errors窗口
    Errors
    " 关闭错误窗口, 但是不会清空错误，很重要哦
    " 因为以前的python代码实在太多警告了，（~_~）
    lclose
    " 清空错误信息     
    SyntasticReset
    " 激活/禁用模式间切换
    SyntasticToggleMode
    " 错误间跳转，不需要跳到 quickfix 窗口
    lnext 
    lprevious
```


### 2 配置选项
```vim
    " 必要配置1
    " 和powerline状态栏冲突，所以关闭下面的三个选项，导致某些输出信息不再status line显示                                             
    " set statusline+=%#warningmsg#                                       
    " set statusline+=%{SyntasticStatuslineFlag()}                         
    | set statusline+=%*                                                   

    " 必要配置2--错误标注（和SyntasticStatuslineFlag()配合）             
    let g:syntastic_error_symbol = 'EE'                                 
    let g:syntastic_style_error_symbol = 'E>'                           
    let g:syntastic_warning_symbol = 'WW'                               
    let g:syntastic_style_warning_symbol = 'W>'                         

    " 不需要手动调用 SyntasticSetTocList. 默认1                         
    let g:syntastic_always_populate_loc_list = 1                         
    " 自动拉起关闭错误窗口.                                             
    " 0不自动. 1自动拉起关闭. 2 自动关闭. 3 自动拉起 默认2, 建议为1     
    let g:syntastic_auto_loc_list = 1                                   
    " 打开文件时做语法检查, 默认 0                                       
    let g:syntastic_check_on_open = 1                                   
    " 报错时做语法检查, 默认 1                                           
    let g:syntastic_check_on_wq = 0                                     


    " 对输出做排序, 默认1                                               
    let g:syntastic_sort_aggregated_errors=1                             

    " 输出错误来源. 默认1                                               
    let g:syntastic_id_checkers=1                                       
    " 在命令行显示当前行的错误信息. 默认1                               
    let g:syntastic_echo_current_error=1                                 
    " 行号左边显示错误标记. 默认1                                       
    let g:syntastic_enable_sign=1                                       
    " 鼠标悬停时显示当前行错误信息. 默认1, 改为0                         
    let g:syntastic_enable_balloons=0                                   
    " 开启错误信息语法高亮, 默认1                                       
    let g:syntastic_enable_highlighting=1  
                                
    " 默认1, 设为0加快缓冲速度。                                         
    let g:syntastic_cursor_columns=1                                     
    " 将非标准filetype映射到标准文件.                                     
    let g:syntastic_filetype_map=1                                       
    " 配置每个filetype和全局默认默认                                     
    let g:syntastic_mode_map=1                                           
    " 默认0                                                               
    let g:syntastic_auto_jump=0                                           

    " 添加不想被检查的文件.                                               
    let g:syntastic_ignore_file=[]                                       
    " 设置要忽略的错误                                                   
    let g:syntastic_quiet_messages=[]                                     


    " 合并错误, 默认 0，1则调用所有check, 并合并结果.                     
    " How can I display all errors from all checkers together?           
    let g:syntastic_aggregate_errors=0                                   
    " Syntastic supports several checkers for my filetype                 
    "   通用格式：let g:syntastic_<filetype>_checkers = ['<checker-name>']
    "   命令检查：也可以使用:SyntasticCheck phpcs phpmd来进行             
    let g:syntastic_python_checkers = ['pylint']                         
    let g:syntastic_php_checkers = ['php', 'phpcs', 'phpmd']   
```


### 3 GCC配置
```vim
" 1,一旦出现找不到某一个头文件，请先使用syntsticInfo命令查看文件类型
" 2,gcc和g++配置不要混合使用
"
" gcc/g++ 语句支持：help syntastic-checkers获取更多信息
" Check header files
let g:syntastic_c_check_header = 1
let b:syntastic_c_cflags = '-I/include -I/usr/src/linux-headers-4.2.0-42-generic/include/'
let g:syntastic_c_include_dirs = []
let g:syntastic__compiler_options = ''
" 增加config的查找路径，这些配置文件中包含CFLAGS或者include目录等信息
let g:syntastic_c_config_file = ''
" 移除某些错误信息
" let g:syntastic_c_remove_include_errors = 1
" 错误输出格式
let g:syntastic_c_errorformat = "%f:%l%c: %trror: %m"
" C编译器
let g:syntastic_c_compiler = "gcc"
```

### 4 g++配置
```vim
let g:syntastic_cpp_check_header = 1
let b:syntastic_cpp_cflags = '-I/include -I/usr/src/linux-headers-4.2.0-42-generic/include/'
let g:syntastic_cpp_include_dirs = []                                                       
" 编译器选项
let g:syntastic_cpp_compiler_options = '-std=c++11'
" Enable header files being re-checked on every file write.
let g:syntastic_cpp_auto_refresh_includes = 1
" let g:syntastic_cpp_remove_include_errors = 1
let g:syntastic_cpp_errorformat = "%f:%l%c: %trror: %m"
let g:syntastic_cpp_compiler = "g++"
```


### 5 python配置
```
" python checkers检查，如果速度过慢，可以使用pyflakes或者pep8
let g:syntastic_python_checkers=['pylint']
" 最终版本，忽略某些错误，该变量还有其他用途
let g:syntastic_python_pylint_args = '--disable=C0111,R0903,C0301'
let g:syntastic_python_flake8_args='--ignore=E501,E402'
```


### 6 shell配置
```
" shell检查(shellcheckers)
" let b:syntastic_checkers=['shellcheckers']
let g:syntastic_sh_checkers=['shellcheckers']
```
