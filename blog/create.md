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
        curl -o- https://raw.github.com/creationix/nvm/master/install.sh | bash
        and then,you will find bottom lines at .zshrc:
            export NVM_DIR="/home/bamboo/.nvm"
            [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"  # This loads nvm
        May be you must re-perform:
            source ~/.zshrc
            

    4)install node.js
        sudo nvm install 4

