"""
项目工具
"""
from functools import wraps

from flask import request

from core.JwtUtil import JwtUtils
from core.resp_model import respModel


def login_required(f):
    @wraps(f)
    def decorated_function():
        cookies = request.headers.get("cookie")
        tmplist = cookies.split(";")
        global ltoken
        for value in tmplist:
            if "l-token" in value:
                ltoken = value[8:]
        userValidation = JwtUtils.verify_token(ltoken)
        if userValidation:
            return f()
        else:
            return respModel.error_401resp("The current user session has expired.")

    return decorated_function
