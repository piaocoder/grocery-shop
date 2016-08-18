#!/bin/bash

# 系统初始化脚本

sudo apt-get install aptitude
sudo aptitude install git
sudo aptitude install vim

sudo aptitude install openssh-server openssh-client

sudo aptitude install git
cd ~ && git clone git@github.com:unlessbamboo/grocery-shop.git

sudo aptitude install -y curl wget
sudo aptitude install -y zsh gitcore
cd ~ && sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
chsh -s `which zsh`
echo "
if [[ -f ~/.bamboo_profile ]];then
    . ~/.bamboo_profile
fi" >> ~/.zshrc
sudo init 6


git clone git://github.com/yyuu/pyenv.git  ~/.pyenv
exec $SHELL -l


# tmux
# ubuntu 16.04
sudo aptitude install tmux
rm -rf ~/.tmux && git clone https://github.com/Big-universe-group/.tmux.git
cd ~ && ln -sf .tmux/.tmux.conf && ln -sf .tmux/.tmux.conf.local .tmux.conf.local

# powerline
pip install --user git+git://github.com/Lokaltog/powerline
cd /tmp/
wget https://github.com/Lokaltog/powerline/raw/develop/font/PowerlineSymbols.otf
wget https://github.com/Lokaltog/powerline/raw/develop/font/10-powerline-symbols.conf
mkdir -p ~/.fonts/ && mv PowerlineSymbols.otf ~/.fonts/
fc-cache -vf ~/.fonts
mkdir -p ~/.config/fontconfig/conf.d/ && mv 10-powerline-symbols.conf ~/.config/fontconfig/conf.d/
# 系统终端显示语言
cd ~/Downloads && git clone https://github.com/powerline/fonts.git
cd fonts && ./install.sh




cd /tmp/ && wget https://bootstrap.pypa.io/get-pip.py --no-check-certificate
sudo python get-pip.py 
mkdir ~/.pip
echo "[global]
index-url = http://pypi.douban.com/simple
trusted-host = pypi.douban.com
[install]
use-mirrors = true
install-option=--prefix=~/.local
mirrors = http://pypi.douban.com" >~/.pip/pip.conf


