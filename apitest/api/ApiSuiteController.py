import json
import shutil
from flask import Blueprint, request
from celery.result import AsyncResult
from apitest.model.ApiCollectionModel import ApiCollection
from apitest.model.ApiInfoModel import ApiInfo
from apitest.model.ExcuteSuiteHistoryModel import ExcuteSuiteHistory
from core.resp_model import respModel
from app import app, db, excuteTset, my_celery

from apitest.model.ApiSuiteModel import ApiSuite
from datetime import datetime
from apitest.model.CaseModel import Case
from apitest.model.ApiCaseModel import ApiCase

# 模块信息
from apitest.model.ApiHistoryModel import ApiHistoryModel
from core.tools import login_required

module_name = "ApiSuite"  # 模块名称
module_model = ApiSuite
module_route = Blueprint(f"route_{module_name}", __name__)


@module_route.route(f"/{module_name}/queryByPage", methods=["POST"])
@login_required
def queryByPage():
    """ 查询数据(支持模糊搜索) """
    try:
        # 分页查询
        page = int(request.json["page"])
        page_size = int(request.json["pageSize"])
        with app.app_context():
            filter_list = []
            # ====筛选条件(如果有筛选条件，在这里拓展 - filter)
            # 添加名称模糊搜索条件
            suite_name = request.json.get("suite_name", "")
            if len(suite_name) > 0:
                filter_list.append(module_model.suite_name.like(f'%{suite_name}%'))
            # # 添加 项目筛选条件
            # project_id = request.json.get("project_id", 0)
            # if type(project_id) is not str and project_id > 0:
            #     filter_list.append(module_model.project_id == project_id)
            # =====结束
            # 数据库查询
            datas = module_model.query.filter(*filter_list).limit(page_size).offset((page - 1) * page_size).all()
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
        with app.app_context():
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
        with app.app_context():
            request.json["id"] = None  # ID自增长
            data = module_model(**request.json, create_time=datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S'))
            db.session.add(data)
            # 获取新增后的ID并返回
            db.session.flush()
            data_id = data.id
            db.session.commit()
        return respModel.ok_resp(msg="添加成功", dic_t={"id": data_id})
    except Exception as e:
        print(e)
        return respModel.error_resp(msg=f"添加失败:{e}")


@module_route.route(f"/{module_name}/update", methods=["PUT"])
@login_required
def update():
    """ 修改数据 """
    try:
        with app.app_context():
            module_model.query.filter_by(id=request.json["id"]).update(request.json)
            db.session.commit()
        return respModel.ok_resp(msg="修改成功")
    except Exception as e:
        print(e)
        return respModel.error_resp(msg=f"修改失败，请联系管理员:{e}")


@module_route.route(f"/{module_name}/delete", methods=["DELETE"])
@login_required
def delete():
    """ 删除数据  删除的同时，需要处理掉中间表"""
    try:
        with app.app_context():
            module_model.query.filter_by(id=request.args.get("id")).delete()
            db.session.commit()
        return respModel.ok_resp(msg="删除成功")
    except Exception as e:
        print(e)
        return respModel.error_resp(msg=f"服务器错误,删除失败：{e}")


@module_route.route(f"/{module_name}/excuteSuite", methods=["post"])
@login_required
def execute_suite():
    try:
        create_time = datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S')
        # 获取要执行的测试套件集合ID
        suite_id = request.json["id"]
        suite_name = request.json["suite_name"]
        # 获取配置中指定的 临时文件生成地址
        cases_dir = app.config['CASES_ROOT_DIR']
        with app.app_context():
            session = db.session
            result = excuteTset.delay(cases_dir, suite_id, create_time)
            excute_id = result.id
            excute = ExcuteSuiteHistory(id=0, suite_id=suite_id, excute_id=excute_id, excute_suite_name=suite_name,
                                        excute_status=None, pass_count=None,
                                        fail_count=None, total_count=None,
                                        create_time=create_time, excute_time=None)
            session.add(excute)
            session.commit()
            return respModel.ok_resp_simple(msg="开始执行测试任务")

    except Exception as e:
        print(e)
        return respModel.error_resp(msg=f"服务器错误,执行失败：{e}")


@module_route.route(f"/{module_name}/queryexcuteResult", methods=["POST"])
@login_required
def result():
    try:
        with app.app_context():
            # 分页查询
            page = int(request.json["page"])
            page_size = int(request.json["pageSize"])
            filter_list = []
            # ====筛选条件(如果有筛选条件，在这里拓展 - filter)
            # 添加名称模糊搜索条件
            suite_name = request.json.get("suite_name", "")
            if len(suite_name) > 0:
                filter_list.append(suite_name.like(f'%{suite_name}%'))
            # =====结束
            # 数据库查询
            datas = ExcuteSuiteHistory.query.filter(*filter_list).limit(page_size).offset((page - 1) * page_size).all()
            total = ExcuteSuiteHistory.query.filter(*filter_list).count()
            ex_datas = []
            for data in datas:
                create_time = data.create_time
                suite_id = data.suite_id
                # collection_cases = Case.query.filter(Case.suite_id == suite_id).all()
                # total_count = len(collection_cases)
                pass_count = 0
                fail_count = 0
                his_datas = ApiHistoryModel.query.filter(ApiHistoryModel.suite_create_time == create_time).all()
                if len(his_datas) > 0:
                    for his_data_obj in his_datas:
                        history_desc = his_data_obj.history_desc
                        if "pass" in history_desc and "fail" not in history_desc:
                            pass_count += 1
                        else:
                            fail_count += 1
                tmpbody = {}
                async_result = AsyncResult(id=data.excute_id, app=my_celery)
                if async_result:
                    if async_result.successful():
                        excute_status = "COMPLETE"
                        excute_time, total_count = async_result.get()
                        tmpbody["excute_status"] = excute_status
                        tmpbody["excute_time"] = excute_time
                        tmpbody["total_count"] = total_count
                    elif async_result.failed():
                        excute_status = "FAILED"
                        tmpbody["excute_status"] = excute_status
                        tmpbody["excute_time"] = data.excute_time
                        tmpbody["total_count"] = data.total_count
                        print('执行失败')
                    elif async_result.status == 'PENDING':
                        excute_status = "PENDING"
                        tmpbody["excute_status"] = excute_status
                        tmpbody["excute_time"] = data.excute_time
                        tmpbody["total_count"] = data.total_count
                        print('任务等待中被执行')
                    elif async_result.status == 'RETRY':
                        excute_status = "RETRY"
                        tmpbody["excute_status"] = excute_status
                        tmpbody["excute_time"] = data.excute_time
                        tmpbody["total_count"] = data.total_count
                        print('任务异常后正在重试')
                    elif async_result.status == 'STARTED':
                        excute_status = "STARTED"
                        tmpbody["excute_status"] = excute_status
                        tmpbody["excute_time"] = data.excute_time
                        tmpbody["total_count"] = data.total_count
                        print('任务已经开始被执行')
                    tmpbody["id"] = data.id
                    tmpbody["suite_id"] = data.suite_id
                    tmpbody["excute_id"] = data.excute_id
                    tmpbody["excute_suite_name"] = data.excute_suite_name
                    tmpbody["pass_count"] = pass_count
                    tmpbody["fail_count"] = fail_count
                    tmpbody["create_time"] = data.create_time
                    ExcuteSuiteHistory.query.filter_by(id=data.id).update({**tmpbody})
                    db.session.commit()
                    ex_datas.append(tmpbody)
                else:
                    tmpbody["id"] = data.id
                    tmpbody["suite_id"] = data.suite_id
                    tmpbody["excute_id"] = data.excute_id
                    tmpbody["excute_suite_name"] = data.excute_suite_name
                    tmpbody["excute_status"] = data.excute_status
                    tmpbody["pass_count"] = data.pass_count
                    tmpbody["fail_count"] = data.fail_count
                    tmpbody["total_count"] = data.total_count
                    tmpbody["create_time"] = data.create_time
                    tmpbody["excute_time"] = str(data.excute_time)

                    ex_datas.append(json.dumps(tmpbody))
            ex_datas.reverse()
            return respModel().ok_resp_list(lst=ex_datas, total=total)
    except Exception as e:
        print(e)
        return respModel.error_resp(f"服务器错误,请联系管理员:{e}")
