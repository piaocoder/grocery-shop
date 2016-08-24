---
    Ag(The Silver Searcher)
---

## 介绍和引用
### 1,Introduction
Ag——A code search tools similar to ack, with a focus on speed.  
Install:
>   sudo aptitude install silversearcher-ag

vim.ag——This plugin allow you use ag from vim, and shows results on a split window.
Install:
>   Use pathogen

### 2,reference
<https://github.com/rking/ag.vim>  
<https://github.com/ggreer/the_silver_searcher>


## Configure
``` vim
    " Custom ag name and path(If you install Ag with source code.)
    let g:ag_prg="<custom-ag-path-goes-here> --vimgrep"
    
    " Configure ag.vim to alwarys start searching from your project root instead of the cwd.
    let g:ag_working_path_mode="r"
```


## Usage
Search recursively in some path for the special pattern.
### 1,Command format
> Ag [options] {pattern} [{directory}]，命令行上的操作

### 2,Other cmd
Ag —— grep
AgAdd —— grepadd
LAg —— lgrep
LAgAdd —— lgrepadd

### 3,Escape
> Ag '\\\#define' foo to search for #define foo
Other special character are handled in the same way.

### 4,quick windows keyboard
>
    e    to open file and close the quickfix window
    o    to open (same as enter)
    go   to preview file (open but maintain focus on ag.vim results)
    t    to open in new tab
    T    to open in new tab silently
    h    to open in horizontal split
    H    to open in horizontal split silently
    v    to open in vertical split
    gv   to open in vertical split silently
    q    to close the quickfix window
