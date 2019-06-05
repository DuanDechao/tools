#!/bin/bash
cp ./.bashrc ~/
source ~/.bashrc

mkdir -p ~/.vim/bundle
cp ./comm.vim ~/.vim/
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/vundle
touch ~/.vimrc
echo "source ~/.vim/comm.vim" >>  ~/.vimrc
echo "set nu" >> ~/.vimrc




