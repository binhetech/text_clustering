#!/usr/bin/env bash
source /data2/minisearch/hebin3/py369/bin/activate

# 设置服务ip及端口号
MODULE="微博搜索-text_clustering服务"
IP="0.0.0.0"
PORT="19602"
UWSGI_INI=./uwsgi_text_clustering.ini
sed -i "s/^http-socket.*/http-socket = $IP:$PORT/g" $UWSGI_INI

# 设置服务的进程数
PROCESSES="2"
sed -i "s/^processes.*/processes = $PROCESSES/g" $UWSGI_INI
sed -i "s/^async.*/async = $PROCESSES/g" $UWSGI_INI

uwsgi $UWSGI_INI
echo "$MODULE 已在 $IP:$PORT 启动!"
