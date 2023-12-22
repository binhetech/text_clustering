## 1. 简介

Text Clustering 文本聚类

## 2. 目录说明

+ data：数据文件，主要为静态数据文件，配置文件等
+ models：模型文件
+ logs：服务日志文件，需要动态回滚删除
+ server：服务部署的代码
+ src: 源代码文件

## 3. 文本聚类算法

### 3.1 文本嵌入表征

+ BERT whiten
+ SentenceTransformer
+ SimCSE
+ ...

### 3.2 聚类算法

+ kmeans
+ 层次聚类
+ DBSCAN

## 4. 依赖环境

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

## 5. 服务部署

使用uwsgi+flask部署，设置端口号和进程个数。

```
cd server
sh run.sh &
```

### 5.1 uwsgi服务停止

```
cd server
uwsgi --stop ../logs/uwsgi.pid
```

### 5.2 uwsgi服务重启

```
cd server
uwsgi --reload ../logs/uwsgi.pid
```

查看uwsgi有关的进程

```
ps -ef |grep uwsgi
```
