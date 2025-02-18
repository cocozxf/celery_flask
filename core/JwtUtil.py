import jwt
import app
import datetime

class JwtUtils(object):

    @staticmethod
    def create_token(username,password):
        key = app.app.config["SECRET_KEY"]
        # 要吧什么东西转换成token
        payload ={
            "username":username,
            "password":password,
            "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=30) #设置过期时间为五分钟
        }
        token = jwt.encode(payload,key,algorithm="HS256")
        return token

    @staticmethod
    def verify_token(token):
        key = app.app.config["SECRET_KEY"]
        try:
            payload = jwt.decode(token,key,algorithms=['HS256'])
            return payload
        except jwt.InvalidTokenError:
            return None