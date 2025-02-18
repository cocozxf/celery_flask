import shutil
from flask import Blueprint, request

from apitest.model.ApiInfoModel import ApiInfo
from core.resp_model import respModel
import app
from apitest.model.ApiCollectionModel import ApiCollection
from datetime import datetime
from apitest.model.ApiCaseModel import ApiCase

# 模块信息
from apitest.model.ApiHistoryModel import ApiHistoryModel
from core.tools import login_required

module_name = "ApiCollection"  # 模块名称
module_model = ApiCollection
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
            # ====筛选条件(如果有筛选条件，在这里拓展 - filter)
            # 添加名称模糊搜索条件
            collection_name = request.json.get("collection_name", "")
            if len(collection_name) > 0:
                filter_list.append(module_model.collection_name.like(f'%{collection_name}%'))
            # 添加 项目筛选条件
            project_id = request.json.get("project_id", 0)
            if type(project_id) is not str and project_id > 0:
                filter_list.append(module_model.project_id == project_id)
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
    """ 删除数据  删除的同时，需要处理掉中间表"""
    try:
        with app.app.app_context():
            module_model.query.filter_by(id=request.args.get("id")).delete()
            app.db.session.commit()
        return respModel.ok_resp(msg="删除成功")
    except Exception as e:
        print(e)
        return respModel.error_resp(msg=f"服务器错误,删除失败：{e}")


# 这里开始远程调用逻辑，生成两个文件夹,文件夹名字用UUID为后缀
import json, os, subprocess, uuid, yaml


@module_route.route(f"/{module_name}/excuteTest", methods=["GET"])
@login_required
def execute_test():
    try:
        # 获取配置中指定的 临时文件生成地址
        cases_dir = app.app.config['CASES_ROOT_DIR']
        # 获取要执行的测试用例ID
        collection_id = request.args.get("id")
        with app.app.app_context():
            session = app.db.session
            # 1. 查询指定ID的集合数据
            collection = session.query(ApiCollection).filter_by(id=collection_id).first()
            # 2. 检查 collection_params 参数
            collection_params = [{}]  # 初始化一个空
            # 如果有 collection_params 代表 可能需要 多次执行该套件
            if collection.collection_params:
                collection_params = json.loads(collection.collection_params)

            # 该次执行唯一ID
            execute_uuid = uuid.uuid4().__str__()
            # 3.0 创建 该次 测试套件执行对应的文件夹
            collection_dir = os.path.join(cases_dir, execute_uuid)
            os.makedirs(collection_dir, exist_ok=True)
            # 3.1 先组装 环境变量 数据
            context_data = {}
            if collection.collection_env:
                context_data = json.loads(collection.collection_env)

            # 3.2 把 测试用例 数据转变为yaml 保存到 测试套件执行对应的文件夹
            # 获取集合关联的 ApiCase 数据
            api_cases = session.query(ApiCase).filter_by(collection_id=collection.id).all()
            print(len(api_cases))
            # 生成每个 ApiCase 对应的 YAML 文件
            # 填充测试用例信息
            test_case_data = {
                "context": context_data,
                "desc": collection.collection_name,
                "steps": []
            }
            if collection_params[0]:
                test_case_data["ddts"] = collection_params
            tmp_steps = {}
            for index in range(len(api_cases)):
                api_case = api_cases[index]
                run_order = api_case.run_order
                api_info = session.query(ApiInfo).get(api_case.api_info_id)
                # 填充测试用例信息

                # 先组装 Debug变量 数据 生成 context.yaml 文件
                if api_info.debug_vars:
                    for d in json.loads(str(api_info.debug_vars).replace("'", '"')):
                        context_data.update({d["key"]: d["value"]})
                test_case_data["steps"].append({})
                test_case_data["steps"][index]["run_order"] = run_order
                test_case_data["steps"][index]["desc"] = api_info.api_name
                test_case_data["steps"][index]["url"] = api_info.request_url
                test_case_data["steps"][index]["method"] = api_info.request_method
                test_case_data["steps"][index]["api_type"] = api_info.is_login
                test_case_data["steps"][index]["cookie_name"] = api_info.cookie_name
                # 0. 如果存在请求头，则添加请求头
                if api_info.request_headers:
                    requests_header = {}
                    for d in json.loads(api_info.request_headers):
                        requests_header.update({d["key"]: d["value"]})
                    if len(requests_header.items()) > 0:
                        test_case_data["steps"][index]["header"] = requests_header
                # 1. 仅在 data 不为空时添加
                if api_info.request_form_datas:
                    requests_datas = {}
                    for d in json.loads(api_info.request_form_datas):
                        requests_datas.update({d["key"]: d["value"]})
                    if len(requests_datas.items()) > 0:
                        test_case_data["steps"][index]["data"] = requests_datas
                # 2. 仅在 www_form_datas 不为空时添加
                if api_info.request_www_form_datas:
                    requests_datas = {}
                    for d in json.loads(api_info.request_www_form_datas):
                        requests_datas.update({d["key"]: d["value"]})
                    if len(requests_datas.items()) > 0:
                        test_case_data["steps"][index]["data"] = requests_datas
                # 3.仅在 params 不为空时添加
                if api_info.request_params:
                    requests_params = {}
                    for d in json.loads(api_info.request_params):
                        requests_params.update({d["key"]: d["value"]})
                    if len(requests_params.items()) > 0:
                        test_case_data["steps"][index]["params"] = requests_params
                # 4.仅在 json_data 不为空时添加
                if api_info.requests_json_data:
                    test_case_data["steps"][index]["json"] = api_info.requests_json_data
                # 5.如果存在 检查点，则添加
                if api_info.assert_vars:
                    test_case_data["steps"][index]["assert_options"] = json.loads(api_info.assert_vars)
                # 6.如果存在 json提取，则添加
                if api_info.extract_vars:
                    test_case_data["steps"][index]["extract_options"] = json.loads(api_info.extract_vars)
            newsteps = test_case_data.get("steps")
            # 冒泡排序
            n = len(newsteps)
            for i in range(n):
                for j in range(0, n - i - 1):
                    if newsteps[j]["run_order"] > newsteps[j + 1]["run_order"]:
                        newsteps[j], newsteps[j + 1] = newsteps[j + 1], newsteps[j]
            test_case_data["steps"] = newsteps

            # 将测试用例数据写入 YAML 文件，格式为 执行顺序_名称.yaml
            case_file_name = uuid.uuid4()
            test_case_filename = f"test_{case_file_name}.yaml"
            test_case_yaml_file = os.path.join(collection_dir, test_case_filename)
            with open(test_case_yaml_file, "w", encoding="utf-8") as test_case_file:
                yaml.dump(test_case_data, test_case_file, default_flow_style=False, encoding='utf-8',
                          allow_unicode=True)

            report_dir = app.app.config['REPORT_ROOT_DIR']
            report_file = report_dir + "/" + str(case_file_name) + ".html"
            # 执行测试
            remote_command = f"apirun --cases={collection_dir} --html={report_file} -sv --capture=tee-sys "

            # 文件生成后生成完毕后，
            # report_root_dir = app.app.config['REPORT_ROOT_DIR']
            # report_data_path = os.path.join(report_root_dir, f"{execute_uuid}-data")  # 测试数据
            # report_html_path = os.path.join(report_root_dir, execute_uuid)  # 测试html报告
            # # 1. 执行测试
            # remote_command = f"huace-apirun --cases={collection_dir} -sv --capture=tee-sys --alluredir={report_data_path} "
            command_output = subprocess.check_output(remote_command, shell=True, universal_newlines=True,
                                                     encoding='utf-8')
            history_desc = command_output.split("\n")[-2].replace("=", "")
            # TODO 这里可以根据 command_output 命令输出的内容去做一些统计
            # # 2. 生成html测试报告
            # os.system(f"allure generate {report_data_path} -c -o {report_html_path}")  # 等于你在命令行里面执行 allure
            # # 3. 删除一些临时文件，保留html测试报告即可
            # shutil.rmtree(collection_dir)  # 测试套件临时yaml文件 collection_dir
            # shutil.rmtree(report_file)  # 测试工具执行后的测试结果数据

            report = ApiHistoryModel(id=0, collection_id=collection.id, collection_name=collection.collection_name,
                                     suite_id=None, history_desc=history_desc,
                                     history_detail=report_dir + "/" + str(case_file_name),
                                     create_time=datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S'),
                                     suite_create_time=None)
            session.add(report)
            session.commit()
        return respModel.ok_resp_simple(msg="执行完毕，点击查看测试报告")

    except Exception as e:
        print(e)
        return respModel.error_resp(msg=f"服务器错误,删除失败：{e}")
