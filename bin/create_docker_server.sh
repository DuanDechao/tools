#!/bin/bash

#trap 'kill $(jobs -p)' SIGINT SIGTERM EXIT
has_command() {
    command -v $1 >/dev/null 2>&1
}

full_path() {
    if has_command greadlink; then
        echo `greadlink -f $1`
    else
        echo `readlink -f $1`
    fi
}

PYTHON=`has_command python2.7 && echo python2.7 || echo python`
export SERVERHOME="/home/g66_oversea"

if [ $# -ne 2 ]; then
    echo "Usage: create_docker_server.sh serverName region eg: ./create_docker_server.sh cehua1 kr"
    exit
fi
cd $SERVERHOME/conf
python $SERVERHOME/conf/create_docker_server.py $1 $2

export SERVERROOT="$SERVERHOME/g66_$2""_""$1"
export ENGINEROOT="$SERVERROOT/engine"
export SERVERCONF="$SERVERHOME/conf/g66_$2""_""$1.conf"
export PYTHONPATH="$PYTHONPATH:$ENGINEROOT/Lib:$ENGINEROOT:$SERVERROOT/script"

python $SERVERROOT/tools/script/init_database.py --config=$SERVERCONF

