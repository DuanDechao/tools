#!/bin/bash

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
CURR_PATH=$(pwd)
export SERVERHOME="/home/g66_oversea"
export SERVERROOT="$SERVERHOME/server"
export ENGINEROOT="$SERVERROOT/engine"
export SERVERCONF=${1:-$SERVERHOME/conf/server.conf}
export GMNAME=${2:-gamemanager}
export RUNTAGFILE="/home/g66_oversea/log/server/server.log"
export PYTHONPATH="$PYTHONPATH:$ENGINEROOT/Lib:$ENGINEROOT:$SERVERROOT/script"
export SUPERVISORCONF="$SERVERHOME/conf/supervisor.conf"

gm_op() {
    OP=$1
    echo $OP ...
    python $ENGINEROOT/tools/AdminClient.py --configfile $SERVERCONF --gamemanager $GMNAME --ctrl $OP 2>&1 | nl
    echo
}

wait_entity_save() {
    GAMES=`grep 'game[0-9]*":' $SERVERCONF | cut '-d"' -f2`
    PROC_COUNT=0
    STOP_READY_COUNT=0
    for GAME_NAME in $GAMES ; do
        PROC_COUNT=$((PROC_COUNT+1))
        grep " - $GAME_NAME - .*all entities saved done" $RUNTAGFILE | awk '{ print $3 " " $4; }' | while read log ; do
            ENTITY_SAVE_TS=`date -d "${log:0:19}" +%s 2>/dev/null`
            [ $? -ne 0 ] && continue

            if [ "$ENTITY_SAVE_TS" -ge "${ENTITY_SAVE_START_TS:-0}" ]
            then
                echo " $GAME_NAME stopped: $ENTITY_SAVE_TS, $ENTITY_SAVE_START_TS"
                return 1
            fi
        done
        if [ $? -eq 1 ] ; then
            STOP_READY_COUNT=$((STOP_READY_COUNT+1))
        fi
    done
    echo "  stopped/total: $STOP_READY_COUNT/$PROC_COUNT"
    [ "$STOP_READY_COUNT" -eq "$PROC_COUNT" ] && return 0 || return 1
}


gm_op FORBID_NEW_CONNECTION ; sleep 1
gm_op IGNORE_CLIENT_ENTITY_MSG ; sleep 1
gm_op DISCONNECT_ALL_CONNECTION ; sleep 1
gm_op NOTIFY_SERVER_CLOSING ; sleep 1
gm_op NOTIFY_SERVER_CLOSED ; sleep 1

python $SERVERHOME/bin/server_supervisor_controller.py STOP $SUPERVISORCONF

#export ENTITY_SAVE_START_TS=`date +%s`
#for i in `seq 1 20`; do
#    if wait_entity_save ; then
#        break
#    fi
#    sleep 1
#done
#echo


#gm_op CLOSE_GATE ; sleep 1
#gm_op CLOSE_GAME ; sleep 1
#gm_op CLOSE_DB_MANAGER ; sleep 1
#gm_op CLOSE_GAME_MANAGER; sleep 1
