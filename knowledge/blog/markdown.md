# <center>Markdown Knowledges</center>
##### <p align="right">----这是一个markdown的说明书哦</p>

### 1 What is markdown?
-----------------------
&emsp;  Markdown的目标——一种适用于网络的书写语言，不注重排版。

&emsp;  所有涉及排版的问题，Markdown本身兼容HTML，可以使用HTML的
排版语法来实现缩进/对齐等等功能。

  
### 2 Indent and layout
-----------------------
#### 2.1 缩进

#### 2.1.1 空格
*   半方大的空格：&ensp;或者&#8194;（一个空格）
*   全方大的空格：&emsp;或者&#8195;（两个空格）
*   不断行的空白：&nbsp;或者&#160;（首行缩进）

#### 2.1.2 html代码
&emsp;  可以通过插入html代码，例如<a>    内容</a>的方式来进行首行
缩进，从而提升文章的缩进效果。


#### 2.2 布局
&emsp;  通过各种html标签以及相应的元素来进行排版布局：
>
        <center>题目</center>
        <h3 aligin="rigin">             ---副标题<h3>
        <a>     缩进<a>
&emsp; 上面的代码如果原样写入到markdown文件中，就会产生你想要的布局效果


### 3 Blcok element
------------------

#### 3.1 段落
#### 3.1.1 定义
&emsp; Markdown段落：一个或者多个连续的文本行组成，其中每一个段落的前后
都必须存在一个空行（tab/空格等空白符）。

#### 3.1.2 换行
&emsp; Markdown不支持普通意义上的换行符，如果需要实现换行效果有如下
几种选择：  
*   使用html标签\<br \/\>
*   每一次换行时：两个空格 + 换行符
*   使用“区块引用”或者“列表”，但是格式可能有变动

#### 3.2 区块引用
#### 3.2.1 定义
&emsp; Block quotes使用类似email中的“>”引用方式来进行布局设置

#### 3.2.2 嵌套和内嵌
&emsp; 区块引用支持嵌套操作：
<pre><code>
    > This is first level of quoting.
    >
    > > This is nested blockquote.
    >
    > Back to the first level.
</code></pre>

&emsp; 注意嵌套前后加上空白,输出结果为：
> This is first level of quoting.
>
> > This is nested blockquote.
>
> Back to the first level.

#### 3.2.3 内嵌其他Markdown语法
&emsp; Block quotes中可以引入其他语法，例如标题/列表/代码区块等
<pre><code>
    > #### 标题
    >
    >> 1.   order list 1
    >> 2.   order list 2
    >
    > code:
    >
    >> 利用pre和code来实现
        func() {
           echo "I am a shell code."
        }
</code></pre>
&emsp; 输出结果为:

> #### 我是标题
>
> > 1.   order list 1
> > 2.   order list 2
>
> code:
>
> > <pre><code>
    func() {
        echo "I am a shell code."
    }
</code></pre>

#### 3.3 代码区块
#### 3.3.1 定义
&emsp; 原样的输出某些既定格式的代码（html/python/php等等）.  
*   利用\<pre\>和\<code\>标签来实现上述的功能，注意
上述标签组合不支持内嵌本身哦，即\<pre\>\<code\>内部不能存在自身。  
*   利用\`反引号或者双重\`\`来实现。  
*   利用缩进来实现。  

#### 3.3.2 例子
&emsp; Markdown使用标签或者Tab缩进来完成“代码区块”的编排。   
&emsp; tab缩进之后再插入一个空行即可，当然，也可以使用标签：

    def test():
        print 'I am a pythoinc.'

#### 3.3.2 转换
&emsp; Code block中的&, <, >会自动切换成HTML实体，从而插入HTML原始码，
经过如下转换：
> 原始html码 --> markdown转换 ---> 网页上输出为html原始码

&emsp; 最终的输出如下：

    <div class="bamboo">
        HTML测试。
    </div>

PS：Markdown本身的某些语法不会切换，从而插入markdown代码。

#### 3.4 分割线
分割线\*（必须三个以上，可以连续）：
* * *
减号分割线（有空格）
- - -
下划线(有空格)
_ _ _



### 4 Sections element
---------------------
#### 4.1 链接

#### 4.1.1 格式
[链接文字] + 目标链接

#### 4.1.2 行内式
格式：[我是链接] + (URL, "Title")，其中title可以忽略  
例子：  
>
    [bamboo链接] (URL "unuse")

上面的输出为:
[bamboo链接](http://www.unusebamboo.com "unuse") 

        
#### 4.1.3 参考式
##### 4.1.3.1 格式
链接格式： [link] [id]  
目标格式： [id]: URL "title"  
其中id可以不填入任何信息，默认为隐式链接

##### 4.1.3.2 例子
>
    [bamboo链接] [id1]  

    [id1]: URL "unusebamboo"   
上面的输出结果（注意空格）为:
    [bambo新链接] [123456]  

[123456]: http://www.unusebamboo.com/ "unusebamboo"

##### 4.1.3.3 过程
*   方括号[链接] + [id]
*   方括号[id] + 冒号 + 缩进 + URL + title

#### 4.1.4 业内跳转
##### 4.1.4.1 过程
*   定义锚
    <span id="jump">Hello world!</span>
*   使用markdown语法(不能存在空格)：
    [业内跳转] (#jump)

##### 4.1.4.2 实例
<span id="jump">Hello world!</span>
[业内跳转](#jump)


### 4.2 强调
所有被\*或者\_包围的符号，默认会转为html中的\< em\>标签；  
如果是双重\*或者\_，则会转化为\< strong \>标签；  
>
    *单重*
    **双重**
上面的输出结果为：  
    &emsp; *单重*  
    &emsp; **双重**


### 4.3 图片
#### 4.3.1 分类
*   行内式(不能存在空格)  
    ![alt text] (/path/to/img.jpg "title")
*   参考式  
    ![alt text] [id]  
    [id]: URL "title"


### 4.4 字体
#### 4.4.1 颜色字号
```html
    <font face="黑体">我是黑体字</font>
    <font size=72 face="黑体">我是黑体字, 字号72</font>
    <font color=red size=72 face="黑体">我是黑体字, 字号72, 颜色红色</font>
```
