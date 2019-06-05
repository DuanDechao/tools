FROM debian:jessie

ENV LANG C.UTF-8

ENV PYTHONIOENCODING UTF-8

COPY sources.list /etc/apt/


#安装依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
                build-essential \
                tk-dev \
                wget \
                ca-certificates \
                python-pip \
                subversion \
                python-dev \
                vim \
                rsyslog \
        && rm -rf /var/lib/apt/lists/*

#安装python,需要带上-lz编译
ENV GPG_KEY C01E1CAD5EA2C4F0B8E3571504C367C218ADD4FF
ENV PYTHON_VERSION 2.7.9

RUN set -ex \
        \
        && wget -O python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz" \
        && export GNUPGHOME="$(mktemp -d)" \
        && mkdir -p /usr/src/python \
        && tar -xJC /usr/src/python --strip-components=1 -f python.tar.xz \
        && rm python.tar.xz \
        \
        && cd /usr/src/python \
        && gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)" \
        && ./configure \
            --build="$gnuArch" \
            --enable-shared \
            --enable-unicode=ucs4 \
        && sed -i "s/^LIBS=/& -lz/g" Makefile \
        && make -j "$(nproc)" \
        && make install \
        && ldconfig \
        \
        && find /usr/local -depth \
            \( \
                \( -type d -a \( -name test -o -name tests \) \) \
                -o \
                \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
            \) -exec rm -rf '{}' + \
        && rm -rf /usr/src/python \
        \
        && python2 --version

RUN pip install virtualenv \
    pymongo==2.8.1 \
    pycrypto==2.6.1

RUN easy_install supervisor

COPY packages.pth /usr/local/lib/python2.7/site-packages/

RUN apt-get update && apt-get install -y supervisor

RUN apt-get install -y g++
RUN apt-get install -y git
RUN apt-get install -y cmake

CMD ["/bin/bash"]
