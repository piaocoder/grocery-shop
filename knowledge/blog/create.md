1,Tools
    Use hexo and github, change to an independent blog Later.


2,Install hexo
    1)install npm
        sudo aptitude instal npm
        Note:Cuz the binary name in ubuntu is nodejs instead of node, so
            do an extra job:
                sudo ln -s /usr/bin/nodejs /usr/bin/node
            Otherwise,the later work could not be completed successfully.

    2)install hexo-cli
        sudo npm install hexo-cli -g

    3)install nvm
            wget https://raw.github.com/creationix/nvm/master/install.sh
            bash ./install.sh
        and then,you will find bottom lines at .zshrc:
            export NVM_DIR="/home/bamboo/.nvm"
            [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"  # This loads nvm
        May be you must re-perform:
            source ~/.zshrc
            

    4)install node.js
        sudo nvm install 4


3，Create github project and open github pages
    1)create project
        Repository must be 用户名.github.io
        Open gh-pages function.

    2)you can write a index.html and access to bottow web site:
        printf "<h1>GotGitHub's HomePage</h1>It works.\n" > index.html
        https://用户名.github.io/

4,Create hexo project(Test hexo, this project will be merge to github after)
    1) create hexo project
        hexo init unlessbamboo.github.io

    2) install web
        git support:
            npm install hexo-deployer-git --save
        other:
            npm install

    3) test hexo at localhost
        hexo generate
        hexo server
        Access to http://localhost:4000/

5,push localhost hexo project to github and combine with github pages
    1) configure:_config.yml
        deploy:
            type: git
            repo: git@github.com:unlessbamboo/unlessbamboo.github.io.git
            branch: master

    2) pull code
        hexo clean && hexo generate && hexo deploy

6,install a new themes(indigo)
    1) Reference: 
        https://github.com/yscoder/hexo-theme-indigo/wiki
    
    2) install
        a) themes
            git clone git@github.com:yscoder/hexo-theme-indigo.git themes/indigo
        b) less
            npm install hexo-renderer-less --save
        c) feed
            npm install hexo-generator-feed --save
        d) json-content
            npm install hexo-generator-json-content --save
        f) tags
            hexo new page tags

    3) configure

    4) Test at localhost
        hexo clean && hexo generate && hexo server

    5) Deploy to github
        hexo deploy

    6) Re-access web site
            https://unlessbamboo.github.io
        and you can find different themes.


7,use personal domains
    1) create CNAME
        cd source && echo "www.unusebamboo.com" > CNAME && cd -

    2) get http://unlessbamboo.github.io ip
            dig -t -a http://unlessbamboo.github.io   
        Note: May be two A records.

    3) Add A record at your dns service providers.
        A:IP
            @——A——ip1
            @——A--IP2
            www--CNAME--github.map.fastly.net.

    4) waitting some minutes and access your personal web site.
        What a beautiful day!


8,reference web site and summary after
    github pages知识：http://www.worldhello.net/gotgithub/03-project-hosting/050-homepage.html#dedicate-domain
    hexo 主页： https://hexo.io/zh-cn/docs/themes.html
    备用主题：
        http://www.ezlippi.com/blog/2016/02/jekyll-to-hexo.html
        http://yanceywang.com/2015/07/30/Ubuntu+Hexo+GithubPages%E6%90%AD%E5%BB%BA%E9%9D%99%E6%80%81%E5%8D%9A%E5%AE%A2/
        http://sunwhut.com/2015/10/30/buildBlog/?hmsr=toutiao.io&utm_medium=toutiao.io&utm_source=toutiao.io


9,Change code hosting, from github.com to git.coding.net
    1）修改_config.yml
        repo地址更改
    2）在coding上添加项目的coding-pages分支（以后所有的代码都必须在该分支上更改）
        feature:coding-pages
    3）更改pages设置
    4）更改dns配置
