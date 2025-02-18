from flask import Blueprint
from app import add2, my_celery
from celery.result import AsyncResult

route_index = Blueprint("index_page", __name__)


@route_index.route("/")
def index():
    results = add2.delay(3, 5)
    return results.id


@route_index.route("/result")
def result():
    async_result = AsyncResult(id="e3cddcd9-0490-45b8-897b-7e7a753e839b", app=my_celery)
    if async_result.successful():
        result = async_result.get()
        print(result)
        return str(result)
    elif async_result.failed():
        print("执行失败")
        return str(async_result.get())
