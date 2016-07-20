1，安装yaml
    1）普通版本
        pip install pyyaml
    2）C版本（速度更快）
        见官网说明

2，语法
    1）multiple document
        ---
            某一个document的值
        ...
        ---
            ...
        ...

    2）列表
        a）普通
            - H1
            - H2
            - H3
            - H4
        b）嵌套
            -
                -H1
                -H2
                -H3
            -
                -S1
                -S2
                -S3
        c）嵌套另一种（减少缩进）
            # 注意左对齐
            - -H1
              -H2
              -H3
            - - -S1
                -S2
                -S3

    3）字典
        a）普通
            key1: 0
            key2: 1

        b）复杂可hash字典
            # 注意保持两者同样的缩进
            ? !!python/tuple [0, 0]
            : The tuple
        c）嵌套
            同列表的嵌套

    4）标量
        a）格式：
            plain(普通),signal-quoted('),
            double-quoted("),literal(|),folded(>)

    5）锚点（&）和引用（*）
        left hand: &A(设置锚点A)
            name: bifeng
            weight: 120
        right hand: *A(引用)
        
    6）独立标签tags和对应的python types
        a）格式
            null 或者 !!null

        b）对应表
			===========standard yaml tags===================
			!!null							None
			!!bool							bool
			!!int							int or long (int in Python 3)
			!!float							float
			!!binary						str (bytes in Python 3)
			!!timestamp						datetime.datetime

			!!omap, !!pairs					list of pairs
			!!set							set
			!!str							str or unicode (str in Python 3)
			!!seq							list
			!!map							dict
			Python-specific 				tags	
			!!python/none					None
			!!python/bool					bool
			!!python/bytes					(bytes in Python 3)
			!!python/str					str (str in Python 3)
			!!python/unicode				unicode (str in Python 3)
			!!python/int					int
			!!python/long					long (int in Python 3)
			!!python/float					float
			!!python/complex				complex
			!!python/list					list
			!!python/tuple					tuple
			!!python/dict					dict
			===============Complex Python tag=================
			!!python/name:module.name		module.name
			!!python/module:package.module	package.module
			!!python/object:module.cls		module.cls instance
			!!python/object/new:module.cls	module.cls instance
			!!python/object/apply:module.f	value of f(...)


    7）对象
        ---->普通
            a）目标
                任何可序列化的对象（pickleable）
            b）格式
                !!python/object:module.Class{ attribute: value, ...}
            c）例子：
                !!python/object:__main__.Bamboo
                name: bamboo
            hp: 2000
        ---->支持pickle协议
            !!python/object/new:module.Class
            !!python/object/apply:module.function
