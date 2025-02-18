"""
模块管理模块数据的查询、新增、编辑删除
"""
from flask import Blueprint, request, jsonify

from apitest.model.ApiProjectModel import ApiProject
from core.resp_model import respModel
import app
from apitest.model.ApiModuleModel import ApiModule  # 请替换为你的ApiModule模型类
from datetime import datetime
from core.tools import login_required

module_name = "ApiModule"  # 模块名称
module_model = ApiModule
module_route = Blueprint(f"route_{module_name}", __name__)


@module_route.route(f"/{module_name}/queryByPage", methods=["POST"])
@login_required
def queryByPage():
    """ 查询数据(支持模糊搜索) """
    try:
        # 分页查询
        try:
            page = int(request.json.get("page", 1))
            page_size = int(request.json.get("page_size", 10))
        except ValueError:
            # 处理非数字参数
            return jsonify({"error": "Invalid page or page_size"}), 40
        with app.app.app_context():
            filter_list = []
            # 添加 项目筛选条件
            project_id = request.json.get("project_id", 0)
            if type(project_id) is not str and project_id > 0:
                filter_list.append(module_model.project_id == project_id)
            # 添加模块名称模糊搜索条件
            module_name = request.json.get("module_name", "").strip()
            if module_name:
                module_escaped = module_name.replace('%', '\\%').replace('_', '\\_')
                filter_list.append(module_model.module_name.like(f"%{module_escaped}%", escape='\\'))

            # 数据库查询
            datas = module_model.query.filter(*filter_list).limit(page_size).offset((page - 1) * page_size).all()
            for obj in datas:
                id = getattr(obj, "project_id")
                tmp = ApiProject.query.filter_by(id=id).first()
                project_name = vars(tmp).get("project_name")
                setattr(obj, "project_name", project_name)
            total = module_model.query.filter(*filter_list).count()
            return respModel().ok_resp_list(lst=datas, total=total)
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
        print(e)
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
