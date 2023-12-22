# 简介

Text Clustering 文本聚类

## 目录说明

+ data：数据文件，主要为静态数据文件，配置文件等
+ models：模型文件
+ logs：服务日志文件，需要动态回滚删除
+ server：服务部署的代码
+ src: 源代码文件

## 文本聚类算法

## 依赖环境

sklearn
torch
sentence_transformers
transformers
uwsgi
flask
gevent

```
# uwsgi安装
conda install -c conda-forge uwsgi 
```

## 服务部署

使用uwsgi+flask部署，设置端口号和进程个数。

```
cd server
sh run.sh &
```

### uwsgi服务停止

```
cd server
uwsgi stop ../logs/uwsgi.pid
```

### uwsgi服务重启

```
cd server
uwsgi --reload ../logs/uwsgi.pid
```

查看uwsgi有关的进程

```
ps -ef |grep uwsgi
```
