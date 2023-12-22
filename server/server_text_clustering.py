# -*- coding: utf-8 -*-
# @Time    : 2021/11/11 17:51
# @Author  : hebin
# @Email   : binhetech@163.com
# @File    : server_text_clustering.py
# @Software: PyCharm
import copy

import gevent
import numpy as np
from gevent import monkey

monkey.patch_all()

import sys
import os

import time
import json

import logging
import logging.handlers
from flask import Flask, jsonify, request

path = os.path.dirname(__file__)
sys.path.append(path)
sys.path.append("../")
sys.path.append("../src")

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

from text_clustering import TextClustering


class FlaskApp(Flask):

    def __init__(self, *args, **kwargs):
        """初始化方法
        :param args:
        :param kwargs:
        """
        super(FlaskApp, self).__init__(*args, **kwargs)
        # 获取日志存储工具
        log_dir = "../logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.logger = logging.getLogger(log_dir)
        self.logger.setLevel(logging.INFO)
        self.estimator = TextClustering()
        # 设置日志回滚周期为30天
        handler = logging.handlers.TimedRotatingFileHandler(filename=os.path.join(log_dir, "log_text_clustering"), when="midnight",
                                                            interval=1, backupCount=30)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def predict(self, input):
        try:
            output = self.estimator.process(input)
            result = {"status": 0, "message": "ok", "output": output}
        except Exception as e:
            result = {"status": -1, "message": repr(e), "output": []}
        return result

    def embedding(self, input):
        try:
            output = self.estimator.get_embedding(input)
            result = {"status": 0, "message": "ok", "output": output}
        except Exception as e:
            result = {"status": -1, "message": repr(e), "output": []}
        return result

    def logging(self, request, response, responseTime, status):
        '''
        用于发送日志到日志服务器
        Args:
            request: 请求信息
            response: 返回信息
            responseTime: 响应时间
            status: 日志等级
        Return:
            None
        '''
        log = {"level": status, "appName": "weibo.search.rec.textclustering",
               "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time())),
               "tags": [{"version": 1.0}],
               "pid": os.getpid(), "method": request.method.lower(), "statusCode": response.status_code, "req": {}}
        # request
        log["req"]["url"] = request.url
        log["req"]["method"] = request.method.lower()
        log["req"]["headers"] = {k.lower(): v for k, v in dict(request.headers).items()}
        log["req"]["remoteAddress"] = request.remote_addr
        log["req"]["userAgent"] = request.user_agent.string
        log["req"]["referrer"] = request.referrer
        log["req"]["contentLength"] = request.content_length
        log["req"]["content"] = dict(request.form)
        # response
        content = copy.deepcopy(response.json)
        log["res"] = {}
        log["res"]["statusCode"] = response.status_code
        log["res"]["responseTime"] = responseTime
        log["res"]["contentLength"] = response.content_length
        log["res"]["content"] = content
        log["message"] = response.json["message"]
        self.logger.info(json.dumps(log))


app = FlaskApp(__name__)


@app.route("/text_clustering/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        t0 = time.time()
        form = json.loads(request.data)

        response = {}
        status = "info"  # 代码运行状态, 等于当前日志等级

        # 若表单为空, 返回错误信息日志
        if not form:
            status = "error"
            response = {"message": "Error: the request form is empty!",
                        "status": -1}

        texts = []
        if status == "info":
            if "input" in form:
                texts = form["input"]
            else:
                status = "error"
                response = {"message": "Error: the request doesn't have key 'texts'!",
                            "status": -1}

        if status == "info":
            try:
                response = app.predict(texts)
                if response["status"] == 0:
                    response["message"] = "ok"
            except KeyError as e:
                response = {"message": "Error: can not find the key %s! " % (str(e)),
                            "status": -1}
        response_time = int((time.time() - t0) * 1000)
        response["time"] = response_time
        response = jsonify(response)

        # 将返回结果按照指定日志格式输出
        app.logging(request, response, response_time, status)
        return response
    else:
        return jsonify({"message": "Error: please use POST method!", "status": -4, })


@app.route("/text_clustering/embedding", methods=["POST"])
def embedding():
    if request.method == "POST":
        t0 = time.time()
        form = json.loads(request.data)

        response = {}
        status = "info"  # 代码运行状态, 等于当前日志等级

        # 若表单为空, 返回错误信息日志
        if not form:
            status = "error"
            response = {"message": "Error: the request form is empty!",
                        "status": -1}

        texts = []
        if status == "info":
            if "input" in form:
                texts = form["input"]
            else:
                status = "error"
                response = {"message": "Error: the request doesn't have key 'texts'!",
                            "status": -1}

        if status == "info":
            try:
                response = app.embedding(texts)
                if response["status"] == 0:
                    response["message"] = "ok"
            except KeyError as e:
                response = {"message": "Error: can not find the key %s! " % (str(e)),
                            "status": -1}
        response_time = int((time.time() - t0) * 1000)
        response["time"] = response_time
        response = jsonify(response)

        # 将返回结果按照指定日志格式输出
        app.logging(request, response, response_time, status)
        return response
    else:
        return jsonify({"message": "Error: please use POST method!", "status": -4, })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=19602)
