#!/bin/bash

work_dir=$(cd `dirname $0`; pwd)
cp {work_dir}/.bashrc /root/
source /root/.bashrc

mkdir -p /root/.vim/bundle
cp {work_dir}/comm.vim /root/.vim/
git clone https://github.com/VundleVim/Vundle.vim.git /root/.vim/bundle/vundle
touch /root/.vimrc
echo "source /root/.vim/comm.vim" >>  /root/.vimrc
echo "set nu" >> /root/.vimrc




