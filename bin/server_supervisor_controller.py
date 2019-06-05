# -*- coding: utf-8 -*-
"""控制服务器脚本，使用supervisor管理"""
import sys
import os
import xmlrpclib
import time
class Global(object):
    "全局常量"
    #启动的超时时间
    TIME_OUT = 180
    #server根目录
    SERVER_PATH = ""
    #配置文件
    CONFIG_FILE = ""

    #日志文件
    LOG_PATH = ""

    #supervisor对应的server
    SUPERVISOR_HTTP_SERVER = None

    #http address
    HTTP_SERVER = "http://localhost:9001/RPC2"

    #key:group_name value:(name, log_file)
    GROUP_DICT = {}

    #log中启动成功logtag
    START_SUC_LOG_TAG = "<!--XSUPERVISOR:BEGIN-->SUCCESSFUL<!--XSUPERVISOR:END-->"
    START_GAME_SUC_LOG_TAG = "<!--XSUPERVISOR:BEGIN-->GAME READY<!--XSUPERVISOR:END-->"

    #log中关闭成功的logtag
    STOP_SUC_LOG_TAG = ""
    STOP_GAME_SUC_LOG_TAG ="<!--XSUPERVISOR:BEGIN-->GAME SAVED<!--XSUPERVISOR:END-->"


def LOG_INFO(s):
    print "INFO:" + s

def LOG_ERROR(s):
    print "ERROR:" + s

def exit_fail(tag):
    LOG_ERROR("***** Failed to %s server *******" % tag)
    exit(1)

def exit_suc(tag):
    LOG_INFO("***** Server %s successfully ******" % tag)
    exit(0)

def is_str_in_file(s, path):
    cmd = "grep '%s' %s | wc -l" % (s, path)
    res_list = os.popen(cmd).readlines()
    if int(res_list[0]) > 0:
        return True
    else:
        return False


def _start_supervisord():
    """启动supervisord """
    LOG_INFO("----------------------start supervisord-----------------------")
    LOG_INFO("supervisord config file: %s" % Global.CONFIG_FILE)
    os.system('supervisord -c %s' % (Global.CONFIG_FILE))

def _start_supervisorctl():
    """启动supervisorctl """
    LOG_INFO("----------------------start supervisorctl---------------------")
    LOG_INFO("supervisorctl config file: %s" % Global.CONFIG_FILE)
    os.system('supervisorctl -c %s start all' % (Global.CONFIG_FILE))

def _stop_supervisord():
    """关闭supervisord"""
    LOG_INFO("---------------------stop supervisord--------------------------")
    LOG_INFO("supervisord config file: %s" % Global.CONFIG_FILE)
    cmd = "kill -s 9 `ps aux | grep supervisord | grep %s | awk '{print $2}'`" % Global.CONFIG_FILE
    os.popen(cmd)

def _stop_supervisorctl():
    """关闭supervisorctl"""
    LOG_INFO("---------------------stop supervisorctl------------------------")
    LOG_INFO("supervisorctl config file:%s" % Global.CONFIG_FILE)
    os.system('supervisorctl -c %s stop all' % (Global.CONFIG_FILE))

def _check_game_start():
    """检查process是否起来"""
    _init_process_log_info()
    for group_name, process_list in Global.GROUP_DICT.iteritems():
        LOG_INFO("check group started... group_name=%s" % group_name)
        if not all(map(lambda process_info: _check_server_process_start(*process_info), process_list)):
            return False

    return True

def _check_server_process_start(process_name, log_file_name):
    """检查当前某个进程是否启动成功"""
    LOG_INFO("checking %s started ...." % process_name)
    suc_tag = Global.START_GAME_SUC_LOG_TAG if log_file_name.find("game") != -1 and log_file_name.find("manager") == -1 else Global.START_SUC_LOG_TAG
    #check log exist
    flag = False
    start_time = time.time()
    while not flag and time.time() - start_time <= Global.TIME_OUT:
        time.sleep(0.5)
        flag = os.path.exists(log_file_name)
    if not flag:
        LOG_ERROR("Cant find log file=%s" % log_file_name)
        return False

    #check log info
    flag = False
    start_time= time.time()
    while not flag and time.time() - start_time <= Global.TIME_OUT:
        time.sleep(0.5)
        has_err = is_str_in_file("Traceback", log_file_name)
        if has_err:
            LOG_ERROR("Found Traceback in log file: %s" % log_file_name)
            return False
        flag = is_str_in_file(suc_tag, log_file_name)

    if not flag:
        LOG_ERROR("check server process[%s] start failed" % process_name)
        return False

    return True

def _init_process_log_info():
    """初始化所有process的log信息，用于检查"""
    all_process_info = Global.SUPERVISOR_HTTP_SERVER.supervisor.getAllProcessInfo()
    for process_info in all_process_info:
        group, name, file_log = process_info["group"], process_info["name"], process_info["logfile"]
        if Global.GROUP_DICT.get(group) is None:
            Global.GROUP_DICT[group] = []

        Global.GROUP_DICT[group].append((name, file_log))

def _check_game_stop():
    """检查服务器进程是否成功关闭"""
    _init_process_log_info()
    for group_name, process_list in Global.GROUP_DICT.iteritems():
        LOG_INFO("check group stop startd... group_name=%s" % group_name)
        if not all(map(lambda process_info: _check_server_process_stop(*process_info), process_list)):
            return False
    return True

def _check_server_process_stop(process_name, log_file_name):
    """检查单个服务器进程是否关闭成功"""
    LOG_INFO("checking %s stop started ..." % process_name)
    suc_tag = Global.STOP_GAME_SUC_LOG_TAG if log_file_name.find("game") != -1 and log_file_name.find("manager") == -1 else Global.STOP_SUC_LOG_TAG
    #非game服不用检验, 直接true
    if suc_tag != Global.STOP_GAME_SUC_LOG_TAG:
        return True

    #check log exist
    if not os.path.exists(log_file_name):
        LOG_ERROR("cant find log file=%s" % log_file_name)
        return False
    
    flag = False
    start_time = time.time()
    while not flag and time.time() - start_time <= Global.TIME_OUT:
        time.sleep(0.5)
        flag = is_str_in_file(suc_tag, log_file_name)

    if not flag:
        LOG_ERROR("check server process[%s] stop failed" % process_name)
        return False

    return True

def _get_supervisor_state(supervisor):
    """
    ret value like this {"statecode": 1, "statename": "RUNNING"}
    statecode           statename               Description
    2                   FATAL                   Supervisor has experienced a serious error
    1                   RUNNING                 Supervisor is working normally
    0                   RESTARTING              Supervisor is in the process of restarting
    -1                  SHUTDOWN                Supervisor is in the process of shutting down
    """
    try:
        ret = supervisor.getState()
    except:
        ret = None
    return ret

def is_program_running():
    """检查当前服务器的supervisor是否启动"""
    server = xmlrpclib.Server(Global.HTTP_SERVER)
    Global.SUPERVISOR_HTTP_SERVER = server
    ret = _get_supervisor_state(server.supervisor)
    if not ret or ret.get("statecode") == -1:
        return False
    return True

def init_path():
    """初始化server路径和log路径"""
    serverPath = os.environ.get("SERVERROOT")
    if serverPath is None:
        LOG_ERROR("cant find server root path in environment vars")
        return False
    Global.SERVER_PATH = serverPath

    Global.LOG_PATH = serverPath + "/log/supervisor"
    if not os.path.exists(Global.LOG_PATH):
        try:
            os.makedirs(Global.LOG_PATH)
        except Exception, e:
            LOG_ERROR("create log dir error, err=%s" % str(e))
            return False

    LOG_INFO("init path success")
    return True


def rotate_log():
    """日志滚动"""
    log_history = []
    for i in xrange(10):
        log_history.append([])
    new_log = []
    for name in os.listdir(Global.LOG_PATH):
        path = Global.LOG_PATH + '/' + name
        base = Global.LOG_PATH
        if os.path.isfile(path) and name.endswith('.log'):
            if name.startswith('old_'):
                log_idx = int(name[4])
                log_history[log_idx].append((base, name))
            else:
                new_log.append((base, name))
    #remove oldest logs
    for base, name in log_history[9]:
        path = base + '/' + name
        os.remove(path)

    #rotate log name
    for idx in xrange(8, -1, -1):
        for base, name in log_history[idx]:
            new_name = 'old_%d_%s' % (idx + 1, name[6:])
            src = base + '/' + name
            dst = base + '/' + new_name
            if not os.path.exists(src):
                LOG_ERROR("cant find path=%s" % src)
            os.rename(src, dst)

    #rename new log
    for base, name in new_log:
        src = base + '/' + name
        new_name = "old_0_%s" % name
        dst = base + '/' + new_name
        os.rename(src, dst)

    return True

def start_init():
    """启动初始化"""
    if is_program_running():
        _stop_supervisord()

    if not init_path():
        LOG_ERROR("init env path and log path failed")
        return False

    if not rotate_log():
        LOG_ERROR("rotate log failed")
        return False

    return True

def stop_init():
    """关闭初始化"""
    if not init_path():
        LOG_ERROR("init env path and log path failed")
        return False

    return True

def run_server_supervisor():
    """启动supervisor两个组件和服务器进程，并检查是否启动成功"""
    _start_supervisord()
    _start_supervisorctl()
    return _check_game_start()

def stop_server_supervisor():
    """关闭supervisor"""
    ret = _check_game_stop()
    _stop_supervisorctl()
    _stop_supervisord()
    return ret

def start_flow():
    if not start_init():
        return False
    if not run_server_supervisor():
        return False
    return True

def stop_flow():
    if not is_program_running():
        return True
    if not stop_init():
        return False
    if not stop_server_supervisor():
        return False
    return True

if __name__ == "__main__":
    if len(sys.argv) != 3 or (sys.argv[1] != "START" and sys.argv[1] != "STOP"):
        print "Usage: %s START|STOP config_file" % sys.argv[0]
        exit_fail("START|STOP")
    else:
        Global.CONFIG_FILE = sys.argv[2]
        if sys.argv[1] == "START" and start_flow():
            exit_suc(sys.argv[1])
        elif sys.argv[1] == "STOP" and stop_flow():
            exit_suc(sys.argv[1])
        else:
            print "Usage: %s START|STOP config_file" % sys.argv[0]
            exit_fail(sys.argv[1])
