!/bin/bash

wget https://github.com/vim/vim/archive/v8.1.1766.tar.gz
tar -zxvf  v8.1.1766.tar.gz
cd vim-8.1.1766/

yum install -y ruby ruby-devel lua lua-devel luajit \
	luajit-devel ctags git python python-devel \
	python36 python36-devel tcl-devel \
	perl perl-devel perl-Extutils-ParseXS \
	perl-ExtUtils-XSpp perl-ExtUtils-CBuilder \
	perl-ExtUtils-Embed libX* ncurses-devel gtk2-devel

./configure --with-features=huge \
	--enable-fontset \
	--enable-multibyte \
	--enable-rubyinterp \
	--enable-python3interp \
	--with-python3-config-dir=/usr/lib64/python3.6/config-3.6m-x86_64-linux-gnu \
	--enable-luainterp \
    --enable-gui=gtk2 \
	--enable-cscope \
	--prefix=/usr/local && make && make install

alias vim='/usr/local/bin/vim'
echo "alias vim='/usr/local/bin/vim' " >> ~/.bashrc
rm -rf vim-8.1.1766