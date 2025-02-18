# 模板代码
""""
返回值模板
"""
import inspect
from typing import Any


class respModel():

    @staticmethod
    def ok_resp(obj=None, msg=None, dic_t=None):
        rsp = {}
        rsp["code"] = 200
        rsp["msg"] = msg
        data = {}
        if obj:
            data = respModel().get_custom_attributes(obj)
        if dic_t:
            data.update(dic_t)
        rsp["data"] = data
        return rsp

    @staticmethod
    def ok_resp_list(obj=None, msg=None, lst=None, total=0):
        rsp = {}
        rsp["code"] = 200
        rsp["msg"] = msg
        rsp["total"] = total
        lst1 = []
        if lst:
            for obj in lst:
                if isinstance(obj, dict):
                    dic = obj
                else:
                    dic = respModel().get_custom_attributes(obj)
                lst1.append(dic)
        rsp["data"] = lst1
        return rsp

    @staticmethod
    def ok_resp_simple(lst=None, msg=None):
        rsp = {}
        rsp["code"] = 200
        rsp["msg"] = msg
        rsp["data"] = lst
        return rsp

    @staticmethod
    def ok_resp_simple_list(lst=None, msg=None, total=0):
        rsp = {}
        rsp["code"] = 200
        rsp["msg"] = msg
        rsp["data"] = lst
        rsp["total"] = total
        return rsp

    @staticmethod
    def ok_resp_text(msg=None, data=None):
        rsp = {}
        rsp["code"] = 200
        rsp["msg"] = msg
        rsp["data"] = data
        return rsp

    # 新定义一个response模块，处理树形数据返回的。。。
    @staticmethod
    def ok_resp_tree(treeData, msg):
        rsp = {}
        rsp["code"] = 200
        rsp["msg"] = msg
        rsp["data"] = treeData
        return rsp

    @staticmethod
    def error_resp(msg):
        rsp = {}
        rsp["code"] = -1
        rsp["msg"] = msg
        return rsp

    @staticmethod
    def error_401resp(msg):
        rsp = {}
        rsp["code"] = 401
        rsp["msg"] = msg
        return rsp

    # def get_custom_attributes02(self, obj):
    #     custom_attributes = {}
    #     # 获取对象的所有属性
    #     attributes = vars(obj)
    #     # 过滤掉内置属性和方法
    #     for attribute, value in attributes.items():
    #         if not attribute.startswith('__') and not callable(value) and not attribute.startswith('_'):
    #             custom_attributes[attribute] = value
    #     return custom_attributes


    def get_custom_attributes(self, obj: Any, include_protected: bool = False) -> dict:
        """获取对象自定义属性

        :param include_protected: 是否包含单下划线开头属性
        """

        exclude_names = ['query', 'registry','metadata']
        attrs = {}

        try:
            # 兼容没有__dict__的对象
            members = inspect.getmembers(obj)
        except AttributeError:
            return attrs

        for name, value in members:
            # 排除魔术方法

            if name.startswith('__') and name.endswith('__'):
                continue

                # 根据参数决定是否排除保护属性
            if not include_protected and name.startswith('_'):
                continue

                # 精确判断可调用对象类型
            if inspect.isroutine(value):
                continue

                # 排除模块、类等特殊类型
            if inspect.ismodule(value) or inspect.isclass(value):
                continue
            if name in exclude_names:
                continue
            attrs[name] = value

        return attrs
