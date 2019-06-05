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

export PYTHON=`has_command python2.7 && echo python2.7 || echo python`

export SERVERHOME="/home/g66_oversea"
export SERVERROOT="$SERVERHOME/server"
export ENGINEROOT="$SERVERROOT/engine"
export SERVERCONF="$SERVERHOME/conf/server.conf"
export SUPERVISORCONF="$SERVERHOME/conf/supervisor.conf"
export PYTHONPATH="$PYTHONPATH:$ENGINEROOT/Lib:$ENGINEROOT:$SERVERROOT/script"

cd $SERVERROOT/bin
python $SERVERHOME/bin/server_supervisor_controller.py START $SUPERVISORCONF

