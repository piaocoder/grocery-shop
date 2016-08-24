---
    Doxygen and DoxygenToolkit
---


## Introduction
### 1, Description
对C/C++的代码注释，以及一键化自动生成文档

### 2, Reference
<https://github.com/vim-scripts/DoxygenToolkit.vim>


## Configure
### 1,Keymap shortkuts
``` vim
    " 函数和类注释，进行键的映射(输入,fg，即输出如下的字段)
    nmap <leader>fg :Dox<cr>
    " 插入文件名，作者时间                                 
    nmap <leader>fa :DoxAuthor<cr>
    " 插件license注释
    nmap <leader>fl :DoxLic<cr>
    " 跳过文档的编写，不知道干什么的
    " nmap <leader>fu :DoxUndoc<cr>
    " 块注释
    nmap <leader>fb :DoxBlock<cr>
```

### 2, C-configure
``` vim
    " for C++ style, change the '@' to '\'
    let g:DoxygenToolkit_commentType = "C"
    " 高亮显示
    let g:doxygen_enhanced_color = 1

    " 用于设置注释简写的信息，一般为函数名
    "   例如：/// @brief func1
    let g:DoxygenToolkit_briefTag_pre = "@brief "
    "let g:DoxygenToolkit_briefTag_post = "endding"
    let g:DoxygenToolkit_briefTag_funcName = "yes"

    " 模板参数
    let g:DoxygenToolkit_templateParamTag_pre = "@tparam "
    " 普通函数参数
    let g:DoxygenToolkit_paramTag_pre = "@param "
    " 返回值
    let g:DoxygenToolkit_returnTag = "@return "
    let g:DoxygenToolkit_maxFunctionProtoLines = 30

    " 宏定义
    let g:DoxygenToolkit_blockTag = "@name "
    let g:DoxygenToolkit_undocTag="DOXIGEN_SKIP_BLOCK"
    " let g:DoxygenToolkit_blockHeader = "--------------------------------------------"
    " let g:DoxygenToolkit_blockFooter = "--------------------------------------------"
    " 类定义
    let g:DoxygenToolkit_classTag = "@class "

    " 文件头的输出信息
    let g:DoxygenToolkit_fileTag = "@file "
    let g:DoxygenToolkit_dateTag = "@date "
    let g:DoxygenToolkit_authorTag = "@author "
    let g:DoxygenToolkit_versionTag = "@version "
    let g:DoxygenToolkit_licenseTag="unlessbamboo"
    let g:DoxygenToolkit_authorName = "unlessbamboo@gmail.com"
```

### 3, c++-configure
``` vim
    " for C++ style, change the '@' to '\'
    let g:DoxygenToolkit_commentType = "C++"
    " 高亮显示
    let g:doxygen_enhanced_color = 1

    " 用于设置注释简写的信息，一般为函数名
    "   例如：/// @brief func1
    let g:DoxygenToolkit_briefTag_pre = "\\brief "
    "let g:DoxygenToolkit_briefTag_post = "endding"
    let g:DoxygenToolkit_briefTag_funcName = "yes"

    " 模板参数
    let g:DoxygenToolkit_templateParamTag_pre = "\\tparam "
    " 普通函数参数
    let g:DoxygenToolkit_paramTag_pre = "\\param "
    " @exception is also valid，C++中函数存在此类用法
    let g:DoxygenToolkit_throwTag_pre = "\\throw "
    " 返回值
    let g:DoxygenToolkit_returnTag = "\\return "
    let g:DoxygenToolkit_maxFunctionProtoLines = 30

    " 宏定义
    let g:DoxygenToolkit_blockTag = "\\name "
    let g:DoxygenToolkit_undocTag="DOXIGEN_SKIP_BLOCK"
    let g:DoxygenToolkit_blockHeader = "--------------------------------------------"
    let g:DoxygenToolkit_blockFooter = "--------------------------------------------"
    " 类定义
    let g:DoxygenToolkit_classTag = "\\class "

    " 文件头的输出信息
    let g:DoxygenToolkit_fileTag = "\\file "
    let g:DoxygenToolkit_dateTag = "\\date "
    let g:DoxygenToolkit_authorTag = "\\author "
    let g:DoxygenToolkit_versionTag = "\\version "
    let g:DoxygenToolkit_licenseTag="unlessbamboo"
    let g:DoxygenToolkit_authorName = "unlessbamboo@gmail.com"
```
