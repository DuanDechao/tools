#!/bin/bash
if [ $# -ne 3 ]; then
    echo "Usage: start_docker_server.sh serverName region branch, eg: start_docker_server.sh cehua1 kr develop"
    exit
fi

name=$1
region=$2
echo $region
branch=$3

export SERVERHOME="/home/g66_oversea"
export SERVERNAME="g66_$region""_""$name"
echo $SERVERNAME
export SERVERROOT="$SERVERHOME/$SERVERNAME"

cd $SERVERROOT
git switch $branch
docker exec -it $SERVERNAME /bin/bash $SERVERHOME/bin/start_server_supervisor.sh

