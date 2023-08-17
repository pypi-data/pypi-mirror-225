#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Gary
# Datetime: 2023/1/6 17:26
# IDE: PyCharm
import logging
from elasticsearch import Elasticsearch, helpers
from elasticsearch import ConnectionError, SSLError, RequestError, NotFoundError


class ESManager:
    def __init__(self, url: str, user: str, passwd: str):
        self.__url = url
        self.__user = user
        self.__passwd = passwd

    @property
    def client(self):
        """
            建立 ElasticSearch 连接：
                1. 默认为免密连接；
                2. 也可以指定用户名和密码。
        :return:
        """
        try:
            return Elasticsearch(
                self.__url,
                http_auth=(self.__user, self.__passwd)
            )
        except (ConnectionError, SSLError) as err:
            logging.error(msg="\033[31m" + str(err) + "\033[0m")

    def bulk(self, actions: list, index: str):
        """
            创建 ElasticSearch 索引：
                1. 通过 bulk() 方法可以在单个连接中执行多个操作，极大地提升索引性能。
        :param actions:
        :param index:
        :return:
        """
        try:
            helpers.bulk(
                client=self.client,
                actions=actions,
                index=index,
                raise_on_error=True
            )
        except (ConnectionError, SSLError) as err:
            logging.error(msg="\033[31m" + str(err) + "\033[0m")

    def get_es_tpl(self, tpl_name: str):
        """
            根据模板名称获取 ElasticSearch 模板信息：
        :param tpl_name:
        :return:
        """
        try:
            tpl = self.client.indices.get_template(name=tpl_name)
            if tpl:
                return tpl.get(tpl_name)
        except (RequestError, NotFoundError) as err:
            logging.error(msg="\033[31m" + str(err) + "\033[0m")

    def put_template(self, tpl_name: str, body: dict):
        """
            推送 ElasticSearch 模板：
        :param tpl_name:
        :param body:
        :return:
        """
        try:
            tpl = self.get_es_tpl(tpl_name=tpl_name)
            # 当指定的模板存在时，则 Merge mappings 到指定的模板
            tpl.update(body) if tpl else None
            self.client.indices.put_template(
                name=tpl_name,
                body=tpl if tpl else body,
                # "create" 设置为 False 时，如果不存在这个模板则创建，如果存在则更新
                create=False
            )
        except (RequestError, NotFoundError) as err:
            logging.error(msg="\033[31m" + str(err) + "\033[0m")
