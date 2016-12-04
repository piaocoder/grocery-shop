---
title: vim-surround  
date:  2016-10-09 19:00:00  
tags: vim   
---

欢迎来到狂想的个人实验室。  
github：[unlessbamboo](https://github.com/unlessbamboo)


### 1 Configure
``` vim
	surrround命令(s表示surround，周边)：
		Normal mode命令列表：
			ds      delete a surrounding
			cs      change a surrounding
			ys      add a surrounding，Not copy!
			yS      add a surrounding and place the surrounded
					text on a new line + indent it
			yss     add a surrounding to the whole line
			ySs     add a surrounding to the whole line, pleade it
					on a new line + indent it
						ySS<div>:
							<div>
								source
							</div>

		Visual mode命令:
			s       add a surrounding
			S       add a surrounding but place text on new line

		Insert mode命令,不会包括任何字符串，仅仅建立""：
			<c-g>s   add a surrounding
			<c-g>S   add a surrounding + new line + indent

	内文本编辑：
		ci/di/yi
		ca/da/ya
	PS:Note the difference between ya and ys, after not copy

```


### 2 example
对某一个单词添加爽引号：
```vim
    Origin string:Hello wolrd
    Command or Key operate: ysw"
    Result string: "Hello" world
```
