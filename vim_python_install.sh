#!/bin/bash
# install vim python ide

echo '============================================'
echo 'hi Brian.H , here is a gift for you from YX.'
echo '============================================'
sleep 3

echo '==============================='
echo 'start to install dependences...'
if [[ `cat /etc/redhat-release` =~ "Cent" ]]
then
    echo 'install on Centos...'
    yum install -y vim ctags git python-pip curl
elif [[ `cat /etc/issue` =~ "Ubuntu" ]]
then
    echo 'install on Ubuntu...'
    apt-get install vim exuberant-ctags git python-pip curl
else
    echo 'system is not Centos or Ubuntu. you should install dependency yourself...  -_- '
fi

sudo pip install dbgp vim-debug pep8 flake8 pyflakes isort
sleep 2

echo '==============================='
echo 'start to download vimrc file...'
cp ~/.vimrc /tmp/vimrc.bak
curl -O https://raw.githubusercontent.com/fisadev/fisa-vim-config/master/.vimrc
mv .vimrc ~/.vimrc

echo '==============================='
echo 'start to install vim plugins...'
vim +BundleClean +BundleInstall! +qa
sudo chown $USER ~/.vim/
sleep 2

echo '==============================='
echo 'reset shell...'
sleep 2
reset

echo '========================================'
echo '     ok , enjoy your VIM ide now.       '
echo '=================bye!==================='
