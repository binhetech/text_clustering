#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project : bert_score 
# @file : text_clustering.py
# @Author : binhe
# @time : 2023/12/22 10:37
# @Software: PyCharm
import os
import numpy as np
import torch
from sklearn.cluster import AgglomerativeClustering
from sentence_transformers import SentenceTransformer

# 可用的GPU设备号，索引从0开始
os.environ["CUDA_VISIBLE_DEVICES"] = "2"


def call_clustering(cluster_ins, texts, embeddings):
    clustering = cluster_ins.fit(embeddings)
    output = {}
    for i, j in zip(texts, clustering.labels_):
        j = str(j)
        if j not in output:
            output[j] = {"label": j, "texts": []}
        output[j]["texts"].append(i)
    output = sorted(output.values(), key=lambda x: int(x["label"]))
    # print("call_clustering:{}".format(len(output)))
    return output


class TextClustering(object):
    def __init__(self, model_path='../models/text2vec-base-chinese'):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        model = SentenceTransformer(model_path)
        self.model = model.to(self.device)
        # distance_threshold越大，则簇数越少，每簇的样本数就越多
        self.cluster_ins = AgglomerativeClustering(n_clusters=None, affinity='cosine', linkage='complete',
                                                   distance_threshold=0.2)
        print("init completed:{}".format(self.device))

    def get_embedding(self, sentences):
        # Our sentences we like to encode
        # sentences = ['This framework generates embeddings for each input sentence',
        #              'Sentences are passed as a list of string.',
        #              'The quick brown fox jumps over the lazy dog.']

        # Sentences are encoded by calling model.encode()
        embeddings = self.model.encode(sentences)
        return embeddings

    def process(self, texts):
        embs = self.get_embedding(texts)
        output = call_clustering(self.cluster_ins, texts, embs)
        return output


if __name__ == '__main__':
    texts = ["1", "2", "3", "4", "5", "6"]
    X = np.array([[1, 2], [1, 4], [1, 4],
                  [4, 2], [1, 4], [4, 0]])
    cluster_ins = AgglomerativeClustering(n_clusters=None, affinity='cosine', linkage='complete',
                                          distance_threshold=0.2)
    y = call_clustering(cluster_ins, texts, X)
    print(y)

    tc = TextClustering()
    texts = ["中国", "美国", "香蕉", "番茄", "苹果"]
    output = tc.process(texts)
    print(output)
