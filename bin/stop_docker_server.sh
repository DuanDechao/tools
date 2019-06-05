#!/bin/bash
if [ $# -ne 2 ]; then
    echo "Usage: create_docker_server.sh serverName region"
fi

name=$1
region=$2

export SERVERHOME="/home/g66_oversea"
export SERVERNAME="g66_$region""_""$name"
export SERVERROOT="$SERVERHOME/$SERVERNAME"
docker exec -it $SERVERNAME /bin/bash $SERVERHOME/bin/stop_server_supervisor.sh

