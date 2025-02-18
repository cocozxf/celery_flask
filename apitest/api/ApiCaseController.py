from flask import Blueprint, request

from apitest.model.ApiInfoModel import ApiInfo
from core.resp_model import respModel
import app
from apitest.model.ApiCaseModel import ApiCase  # 请根据您的模型路径进行调整
from datetime import datetime

# 模块信息
from core.tools import login_required

module_name = "ApiCase"  # 模块名称，根据实际情况修改
module_model = ApiCase
module_route = Blueprint(f"route_{module_name}", __name__)


@module_route.route(f"/{module_name}/queryByPage", methods=["POST"])
@login_required
def queryByPage():
    """ 查询数据(支持模糊搜索) """
    try:
        # 分页查询
        page = int(request.json["page"])
        page_size = int(request.json["pageSize"])
        with app.app.app_context():
            filter_list = []
            collection_id = int(request.json["collection_id"])
            filter_list.append(module_model.collection_id == collection_id)
            cases = module_model.query.filter(*filter_list).limit(page_size).offset((page - 1) * page_size).all()
            total = module_model.query.filter(*filter_list).count()
            # datas 里面加入接口信息
            # 获取当前页的 ApiCase 信息
            results = []
            for case in cases:
                api_info = ApiInfo.query.filter_by(id=case.api_info_id).first()
                result = respModel().get_custom_attributes(api_info)
                result.update(respModel().get_custom_attributes(case))
                results.append(result)
            return respModel().ok_resp_simple_list(lst=results, total=total)
    except Exception as e:
        print(e)
        return respModel.error_resp(f"服务器错误,请联系管理员:{e}")


@module_route.route(f"/{module_name}/queryById", methods=["GET"])
@login_required
def queryById():
    """ 查询数据(单条记录) """
    try:
        data_id = int(request.args.get("id"))
        with app.app.app_context():
            # 数据库查询
            data = module_model.query.filter_by(id=data_id).first()
        if data:
            return respModel().ok_resp(obj=data)
        else:
            return respModel.ok_resp(msg="查询成功,但是没有数据")
    except Exception as e:
        print(e)
        return respModel.error_resp(f"服务器错误,请联系管理员:{e}")


@module_route.route(f"/{module_name}/insert", methods=["POST"])
@login_required
def insert():
    """ 新增数据 """
    print(request.json)
    try:
        with app.app.app_context():
            request.json["id"] = None  # ID自增长
            data = module_model(**request.json, create_time=datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S'))
            app.db.session.add(data)
            # 获取新增后的ID并返回
            app.db.session.flush()
            data_id = data.id
            app.db.session.commit()
        return respModel.ok_resp(msg="添加成功", dic_t={"id": data_id})
    except Exception as e:
        return respModel.error_resp(msg=f"添加失败:{e}")


@module_route.route(f"/{module_name}/update", methods=["PUT"])
@login_required
def update():
    """ 修改数据 """
    try:
        with app.app.app_context():
            module_model.query.filter_by(id=request.json["id"]).update(request.json)
            app.db.session.commit()
        return respModel.ok_resp(msg="修改成功")
    except Exception as e:
        print(e)
        return respModel.error_resp(msg=f"修改失败，请联系管理员:{e}")


@module_route.route(f"/{module_name}/delete", methods=["DELETE"])
@login_required
def delete():
    """ 删除数据 """
    try:
        with app.app.app_context():
            module_model.query.filter_by(id=request.args.get("id")).delete()
            app.db.session.commit()
        return respModel.ok_resp(msg="删除成功")
    except Exception as e:
        print(e)
        return respModel.error_resp(msg=f"服务器错误,删除失败：{e}")

# 添加其他逻辑
