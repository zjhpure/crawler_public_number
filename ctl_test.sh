#! /bin/bash

assist() {
    echo """
         start                   使用测试配置启动进程
         stop                    关闭进程
         start_api               使用测试配置启动API进程
         stop_api                关闭API进程
         """
}

start() {
    rm -rf ./cfg/cfg.py
    cp ./cfg/cfg_test.py ./cfg/cfg.py
    nohup python3 -u ./start.py &
}

stop() {
    pid=$(ps -ef | grep ./start.py | grep -v grep | awk '{print $2}')
    [ -n "${pid}" ] && kill -9 ${pid}
    echo "已关闭：${pid}"
}

start_api() {
    rm -rf ./cfg/cfg.py
    cp ./cfg/cfg_test.py ./cfg/cfg.py
    nohup python3 -u ./api.py &
}

stop_api() {
    pid=$(ps -ef | grep ./api.py | grep -v grep | awk '{print $2}')
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
