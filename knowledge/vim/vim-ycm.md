---
title: ycm  
date:  2016-10-20 20:00:00  
tags: vim   
---


### 1 Introduction
#### 1.1 Options
选项介绍
#### 1.2 Command
主要命令
#### 1.3 Subcommand
子命令


### 2 Options
#### 2.1 触发
```vim
    " 开启自动不全的最少单词数，默认为2
    let g:ycm_min_num_of_chars_for_completion=3
    " 开启ycm补全以及semantic语法检查，默认1
    let g:ycm_auto_trigger=1
```
#### 2.2 文件类型
用于设置指定的文件类型是否进行ycm操作或者语法检查
```vim
    " This options controls for which Vim filetypes should YCM be turned on.
    " Default: {'*': 1}
    let g:ycm_filetype_whitelist={'*': 1}

    " This options controls for which vim filetypes should YCM be turn off.
    " Default: {see next line}
    let g:ycm_filetype_blacklist = {
          \ 'tagbar' : 1,
          \ 'qf' : 1,
          \ 'notes' : 1,
          \ 'markdown' : 1,
          \ 'unite' : 1,
          \ 'text' : 1,
          \ 'vimwiki' : 1,
          \ 'pandoc' : 1,
          \ 'infolog' : 1,
          \ 'mail' : 1
          \}

    " This option controls which vim filetype should the YCM semantic completion 
    " engine(语义补全器，例如jedi）be turned off
    " Default: [see next line]
    let g:ycm_filetype_specific_completion_to_disable = {
          \ 'gitcommit': 1
          \}
```
#### 2.3 补全
```vim
    " YCM will show the completion menu even when typing inside strings
    " 变量内的值补全
    " Default:1
    let g:ycm_complete_in_strings = 1

    " YCM's identifier completer will collect identifiers(ID标识信息) from strings
    " and comments.（从变量值和注释中收集自动补全信息）
    " Default:0
    let g:ycm_collect_identifiers_from_comments_and_strings = 0

    " YCM's identified completer will collect identifiers from tags files.
    " The only support tag format is the Exuberant Ctag Format. Ctags needs to be
    " called with the --field=+l option.（是否从tags中收集补全信息
    " Default:0
    let g:ycm_collect_identifiers_from_tags_files = 1
```
#### 2.4 编译和注释
```vim
    " When set, this option also makes YCM remove all Syntastic checkers set for
    " the c, cpp, objc and objcpp filetypes since this would conflict with YCM's
    " own diagnostics(诊断) UI.
    " If you're using YCM's identifier completer in C-family languages but cannot
    " use the clang-based semantic语义 completer for those languages and want to use
    " the GCC Syntastic checkers, unset this option.
    " 仅仅适用于C-family，关闭ycm自带的syntastic，默认开启
    " Default: 1
    let g:ycm_show_diagnostics_ui = 0

    " These are YCM option description at bottom.
    " Ycm will populate(填充) the location list automatically every time it get
    " new dianostic(诊断) data.
    " Default:0
    let g:ycm_always_populate_location_list = 0

    " :YcmDiags will automatically open the location list after forcing a
    " compilpation(强制性编译) and filling the list with diagnostic(诊断) data
    " Default:1
    let g:ycm_open_loclist_on_ycm_diags = 1

    " YCM will show the completion menu(补全菜单) even when typing inside
    " comment(注释)
    " Default:0
    let g:ycm_complete_in_comments = 0
```
#### 2.5 python相关
```vim
    " YCM will by default search for an appropriate Python interperter on your
    " system. You can use this option to override that behavior and force the 
    " use of a spcical interpreter of you choosing.
    " Default:''
    let g:ycm_server_python_interpreter = 'python3'


    " This options specifies the python interpreter to use the python to run the
    " jedi library.注意哦
    " Default:''
    let g:ycm_python_binary_path = 'python'
```
#### 2.6 其他
```vim
    " The logging level that the ycm completer servers uses.
    " Default: info
    " Otehrs:debug/info/warning/error/critical
    let g:ycm_server_log_level = 'info'

    " YCM will use the preview window at the top of file to store detailed
    " information about the current candidate(候选)(but only the candicate came
    " from the semantic语义 engine)
    " 例如：输入函数名后会有整个函数定义出现
    " Default:0
    let g:ycm_add_preview_to_completeopt = 1
    " 是否在补全后自动关闭preview windows
    let g:ycm_autoclose_preview_window_after_completion = 1
    " 是否在补全插入时自动关闭preview windows，可以不设置
    let g:ycm_autoclose_preview_window_after_insertion = 0

    " This options controls maximux number of diagnostics(诊断) shown to the user
    " when errors and warnings are detected in the file.
    " 仅仅在C-family semantic completion engine中有效
    " Default:30
    let g:ycm_max_diagnostics_to_display = 30

    " This options controls the key mappings used to select the first completion strings.
    " Default:['TAB', 'DOWN']
    let g:ycm_key_list_select_completion = ['<TAB>', '<Down>']

    " This options controls the key mapping used to select the previous completion
    " strings.
    " Default:['S-TAB', 'UP']
    let g:ycm_key_list_previous_completion = ['<S-TAB>', '<Up>']

    " This options controls the key mappings used to invoke the completion menu
    " for semantic completion.
    " By default, semantic completion is trigged automatically after typing ./->
    " Default:<C-Space>
    let g:ycm_key_invoke_completion = '<C-Space>'

    " This options controls the key mappings used to show full diagnostic(诊断的)
    " text when the user's cursor is on the line with the diagnostic.
    " It basically calls :YcmShowDetailedDiagnostic
    " Default:<leader>d
    let g:ycm_key_detailed_diagnostics = '<leader>d'

    " Normally, YCM serach for a .ycm_extra_conf.py file for the compilation
    " flags.
    " This options special a fallback path to a config file which is used if no
    " .ycm_extra_conf.py is found.
    " Default:''
    let g:ycm_global_ycm_extra_conf = '~/.vim/data/ycm/.ycm_extra_conf.py'

    " YCM will ask once per .ycm_extra_conf.py file if it is safe to be loaded.
    " This is to prevent execution of malicious code(执行恶意代码) from a 
    " .ycm_extra_conf.py file you didn't write.
    " 每次启动代码后都会有一个确认选项进行提示操作
    " Defalt:1
    let g:ycm_confirm_extra_conf = 1

    " By default, YCM filepath completion will interpret(解释) relative path like ../ as
    " being relative(相对的) to the folder of the file of the current active
    " buffers.
    " Setting this option will force YCM to always interpret relative paths as
    " being relative to Vim's current working directory.
    " Default:0
    let g:ycm_filepath_completion_use_working_dir = 0

    " This options controle the character-based triggers for the various
    " semantic(语义) completion engines.
    " Default:[see next line]
    let g:ycm_semantic_triggers =  {
      \   'c' : ['->', '.'],
      \   'objc' : ['->', '.', 're!\[[_a-zA-Z]+\w*\s', 're!^\s*[^\W\d]\w*\s',
      \             're!\[.*\]\s'],
      \   'ocaml' : ['.', '#'],
      \   'cpp,objcpp' : ['->', '.', '::'],
      \   'perl' : ['->'],
      \   'php' : ['->', '::'],
      \   'cs,java,javascript,typescript,d,python,perl6,scala,vb,elixir,go' : ['.'],
      \   'ruby' : ['.', '::'],
      \   'lua' : ['.', ':'],
      \   'erlang' : [':'],
      \ }

    " By default, YCM will query the UltiSnips plugin for possible completions of
    " snippet(代码片段) triggers.This options will turn the behavior off.
    " Default:1
    let g:ycm_use_ultisnips_completer = 1
```


### 3 Command
```vim
    " :YcmDiags
    " Calling this commands will fill vims' locationlist with erros and warinings
    " if any were detected in your file and the open it.
    " 关于locationlist见vim_glassory.md文档

    " :YcmRestartServer
    " Restart your completion server.

    " :YcmShowDetailedDiagnostic
    " 见上面 g:ycm_key_detailed_diagnostics中的说明

    " :YcmDebugInfo
    " This will print out various debug information for current file.
    " 类似SynstaticInfo

    " :YcmToggleLogs
    " This command automatically opens in windows the stdout and stderr logfiles
    " written by the ycmd server.

    " :YcmCompleter
    " This command gives access to a number of additional IDE-like features in
    " YCM. For example:GoTo语义,type information类型信息，Reactoring and 
    " Fixit(重构和Fix命令)
    " 1）参数格式
    "   if the first argument is of the form ft=... the completer for that file
    "   type will be used (for example: ft=cpp), else the native completer of
    "   current buffer will be used.
    "
    " 2）second argument
    "   输入:YcmCompleter获取支持的第二个参数，见下文
```


### 4 SubCommand
```vim
    " Function: Replace ctags and cscople plugins functions.
    " look jumplist
    <Ctrl-O>        jump back
    <Ctrl-I>        jump forward

    " Looks up the current line for a header and jump to it
    " GoToInclude
    " Support in filetypes: c/cpp/objc/objcpp

    " Looks up the symbol(符号) under the cursor and jumps to the declration(声明)  
    " GoToDeclaration
    " Support in filetypes: c/cpp/objc/objcpp/cs/go/python/rust

    " Look up the symbol under the cursor and jumps to its definition(定义)
    " GoToDefinition
    " Support in filetypes:
    "   C/Cpp/objc/objcpp/cs/go/python/javascript/rust/typescript

    " This command tries to perform the "most sensible(明智，理智）" GoTo operation it can.
    " Currently, this means that it tries to look up the symbol under the cursor
    " and jumps to its definition if possible(首先); if the definition is not accessible
    " from the current translation unit, jumps to the symbol's declaration(其次). For
    " C/C++/Objective-C, it first tries to look up the current line for a header
    " and jump to it. For C#, implementations are also considered and preferred.
    "
    " GoTo
    "
    " Supported in filetypes: c, cpp, objc, objcpp, cs, go, javascript, python, rust
    " 自动判断和悬在，一般映射该键
    nnoremap <leader>jd :YcmCompleter GoTo<cr>

    " Echos the type of the variable or method under the cursor, and where it
    " differs, the derived(派生) type.
    " 返回类型以及和不同定义的派生类型
    " For example:
    "   std::string s
    " Invoking this command on s return std::string => std::basic_string<char>
    "
    " GetType
    " Supported in filetypes: c, cpp, objc, objcpp, javascript, typescript

    " Displays the preview(预览) window populated(填充) with quick info about 
    " the identifier under the cursor. Like:
    "   The type or declaration of identifier.
    "   Doxygen/javaDoc comments
    "   pythond docstrings
    "   etc.
    " 
    " GetDoc
    " Supported in filetypes: c, cpp, objc, objcpp, cs, python, typescript,
    " javascript
```


### 5 Refactoring and Fixit Commands
Nothing! Repair the following contents in the future.
