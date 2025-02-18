from datetime import timedelta, datetime

from flask import Blueprint, request, make_response
import app
from sysmanage.model.user import User
from core.JwtUtil import JwtUtils
from core.resp_model import respModel

module_route = Blueprint("route_login", __name__)


@module_route.route("/login", methods=["POST"])
def login():
    with app.app.app_context():
        user = User.query.filter_by(username=request.json["username"], password=request.json["password"]).first()
    if user:
        token = JwtUtils.create_token(request.json["username"], request.json["password"])
        res = make_response(respModel().ok_resp(obj=user, msg="登录成功", dic_t={"token": token}))
        expires = datetime.utcnow()+timedelta(minutes=60)
        res.headers['Access-Control-Allow-Headers'] = 'X-Custom-Header, Authorization,Set-Cookie'
        res.set_cookie('l-token', token,expires=expires)
        return res
    else:
        return respModel().error_resp("The login failed due to an incorrect username or password.")
