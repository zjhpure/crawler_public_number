#! /bin/bash

ROOT=/data/crawler/crawler_public_number

assist() {
    echo """
         start                   使用生产配置启动进程
         stop                    关闭进程
         start_api               使用生产配置启动API进程
         stop_api                关闭API进程
         """
}

start() {
    rm -rf ${ROOT}/cfg/cfg.py
    cp ${ROOT}/cfg/cfg_prod.py ${ROOT}/cfg/cfg.py
    nohup python3 -u ${ROOT}/start.py &
}

stop() {
    pid=$(ps -ef | grep ${ROOT}/start.py | grep -v grep | awk '{print $2}')
    [ -n "${pid}" ] && kill -9 ${pid}
    echo "已关闭：${pid}"
}

start_api() {
    rm -rf ${ROOT}/cfg/cfg.py
    cp ${ROOT}/cfg/cfg_prod.py ${ROOT}/cfg/cfg.py
    nohup python3 -u ${ROOT}/api.py &
}

stop_api() {
    pid=$(ps -ef | grep ${ROOT}/api.py | grep -v grep | awk '{print $2}')
    [ -n "${pid}" ] && kill -9 ${pid}
    echo "已关闭：${pid}"
}

case $1 in
        start)
                start
                ;;
        stop)
                stop
                ;;
        start_api)
                start_api
                ;;
        stop_api)
                stop_api
                ;;
        *)
                assist
                ;;
esac
