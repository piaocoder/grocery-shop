---
title: ctrlp  
date:  2016-10-15 22:00:00  
tags: vim  
---

欢迎来到狂想的个人实验室。  
github：[unlessbamboo](https://github.com/unlessbamboo)


### 1 Basic Usage
#### 1.1 command
```vim
    " Function
    " Full path fuzzy file(模糊搜索文件)，文件类型有：
    "       file/buffer/mru(命令)/tag等

    " Basic Usage
    " 1, Invoke CtrlP in find file mode：
    "   :CtrlP
    " or 
    "   :Ctrlp [Starting-directory]
    nnoremap <leader>p :CtrlP<cr>
    " 2, find buffer  mode
    nnoremap <leader>b :CtrlPBuffer
    " 3, fine MRU mode
    nnoremap <leader>m :CtrlPMRU
    " 4, Search in Files,Buffers,MRU files at the same time
    nnoremap <leader>i :CtrlPMixed
```
#### 1.2 inner command
```vim
    " Once CtrlP is open. Use:
    " <F5>      刷新缓存
    " <c-f> and <c-b> to cycle between modes
    " <c-d> to switch to filename only search instead of full path
    " <c-r> to switch to regexp mode.
    " <c-j>, <c-k> 在匹配结果中上下移动 
    " <c-t> or <c-v>, <c-x> to open the selected entry in a new tab or in a
    " new split.
    " <c-n>, <c-p> to select the next/previous string in the prompt's history.
    " <c-y> to create a new file and its parent directories.
    " <c-z> to mark/unmark multiple files and <c-o> to open them

    " .. or more dots to go up the directory tree.
    " :25  25行
```


### 2, Basic Option
```gcc
    " Change the default mapping to invoke CtrlP
    let g:ctrlp_map = '<leader>p'
    let g:ctrlp_cmd = 'CtrlP'

    " 设置本地工作目录
    " 'c'       当前文件所在的目录
    " 'r'       最近的包含如下：.git/.hg/.svn/.bzr/_darcs的祖先目录
    " 'a'       祖先兄弟目录
    " 0         disable
    let g:ctrlp_working_path_mode = 'ra'

    " Exclude files and directories
    set wildignore+=*/tmp/*,*.so,*.swp,*.zip     " MacOSX/Linux
    set wildignore+=*\\tmp\\*,*.swp,*.zip,*.exe  " Windows

    let g:ctrlp_custom_ignore = '\v[\/]\.(git|hg|svn)$'
    let g:ctrlp_custom_ignore = {
      \ 'dir':  '\v[\/]\.(git|hg|svn)$',
      \ 'file': '\v\.(exe|so|dll)$',
      \ 'link': 'some_bad_symbolic_links',
      \ }

    " Use a custom file listing command:
    let g:ctrlp_user_command = 'find %s -type f'        " MacOSX/Linux
    let g:ctrlp_user_command = 'dir %s /-n /b /s /a-d'  " Windows
```
