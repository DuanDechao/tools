#!/bin/bash
sudo apt-get update
sudo apt-get install -y apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    lsb-release \
    software-properties-common

curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/debian/gpg | sudo apt-key add -
sudo add-apt-repository \
       "deb [arch=amd64] https://mirrors.ustc.edu.cn/docker-ce/linux/debian \
          $(lsb_release -cs) \
             stable"
sudo apt-get update
sudo apt-get install -y docker-ce
echo 'export DOCKER_OPTS="--registry-mirror=http://hub-mirror.c.163.com"' >> /etc/default/docker
docker build -t omega:server ./docker/
usermod -g docker g66_oversea
