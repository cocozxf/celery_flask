"""
接口信息数据的查询、新增、编辑删除及调试接口
"""
import json
import os
import shutil
import subprocess
import uuid
from flask import Blueprint, request
import yaml

from apitest.model.ApiModuleModel import ApiModule
from apitest.model.ApiProjectModel import ApiProject
from core.resp_model import respModel
import app
from apitest.model.ApiInfoModel import ApiInfo
from datetime import datetime

from core.tools import login_required

module_name = "ApiInfo"
module_model = ApiInfo
module_route = Blueprint(f"route_{module_name}", __name__)


@module_route.route(f"/{module_name}/queryByPage", methods=["POST"])
@login_required
def queryByPage():
    try:
        page = int(request.json["page"])
        page_size = int(request.json["pageSize"])
        with app.app.app_context():
            filter_list = []
            # 添加 项目筛选条件
            project_id = request.json.get("project_id", 0)
            if type(project_id) is not str and project_id > 0:
                filter_list.append(module_model.project_id == project_id)
            # 添加 模块筛选条件
            module_id = request.json.get("module_id", 0)
            if type(module_id) is not str and module_id > 0:
                filter_list.append(module_model.module_id == module_id)
            # 添加名称模糊搜索条件
            api_name = request.json.get("api_name", "").strip()
            if len(api_name) > 0:
                filter_list.append(module_model.api_name.like(f'%{api_name}%'))
            # 数据库查询
            datas = module_model.query.filter(*filter_list).limit(page_size).offset((page - 1) * page_size).all()
            for obj in datas:
                project_id = getattr(obj, "project_id")
                module_id = getattr(obj, "module_id")
                tmpproject = ApiProject.query.filter_by(id=project_id).first()
                tmpmodule = ApiModule.query.filter_by(id=module_id).first()
                project_name = vars(tmpproject).get("project_name")
                module_name = vars(tmpmodule).get("module_name")
                setattr(obj, "project_name", project_name)
                setattr(obj, "module_name", module_name)
            total = module_model.query.filter(*filter_list).count()
            return respModel().ok_resp_list(lst=datas, total=total)
    except Exception as e:
        print(e)
        return respModel.error_resp(f"服务器错误,请联系管理员:{e}")


@module_route.route(f"/{module_name}/queryById", methods=["GET"])
@login_required
def queryById():
    try:
        data_id = int(request.args.get("id"))
        with app.app.app_context():
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
    try:
        with app.app.app_context():
            module_model.query.filter_by(id=request.args.get("id")).delete()
            app.db.session.commit()
        return respModel.ok_resp(msg="删除成功")
    except Exception as e:
        print(e)
        return respModel.error_resp(msg=f"服务器错误,删除失败：{e}")


"""
它怎么调工具? -- 命令？ 
解决问题：yaml文件的生成  
 * json.loads  -- 把json字符串格式的字符串 ，变成json对象
 * 123456 -- for -- 1 ,2,3,4,5,6 
 * key : value JSON对象 字典 -- class teacher <==> name:xiaoming ,age:18 
 * 列表 -- str {'key':'host','value':'shop-xo.hctestedu'}
解决问题：传递对应的文件位置信息
 *通过约定自动创建yaml文件 
解决问题: 发送命令去运行
 * 发送命令怎么解决？
 * subprocess.check_output 它去发送windows命令，有返回值
"""


@module_route.route(f"/{module_name}/debug", methods=["POST"])
@login_required
def debug_execute():
    try:
        # 接收前端传递过来的 ApiInfo
        api_info = module_model(**request.json, create_time=datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S'))
        # 获取配置中指定的 临时文件生成地址
        cases_dir = app.app.config['CASES_ROOT_DIR']
        # 该次执行唯一ID
        execute_uuid = uuid.uuid4().__str__()
        # 1.0 创建 该次执行对应的文件夹
        run_tmp_dir = os.path.join(cases_dir, execute_uuid)
        os.makedirs(run_tmp_dir, exist_ok=True)
        # 1.1 先组装 Debug变量 数据 生成 context.yaml 文件
        context_data = {}
        if api_info.debug_vars:
            for d in json.loads(str(api_info.debug_vars).replace("'", '"')):
                context_data.update({d["key"]: d["value"]})
        # context_yaml_file = os.path.join(run_tmp_dir, "context.yaml")
        # with open(context_yaml_file, "w", encoding="utf-8") as context_file:
        #     yaml.dump(context_data, context_file, default_flow_style=False, encoding='utf-8', allow_unicode=True)

        # 1.2 把数据转变为yaml 保存到 测试套件执行对应的文件夹
        # 填充测试用例信息
        test_case_data = {
            "desc": api_info.api_name,
            "context": context_data,
            "steps": [
                {
                    "url": api_info.request_url,
                    "method": api_info.request_method,
                    "api_type": api_info.is_login,
                    "cookie_name": api_info.cookie_name
                }
            ]
        }

        # 0. 如果存在请求头，则添加请求头
        if api_info.request_headers:
            requests_header = {}
            for d in json.loads(str(api_info.request_headers).replace("'", '"')):
                requests_header.update({d["key"]: d["value"]})
            if len(requests_header.items()) > 0:
                test_case_data["steps"][0]["header"] = requests_header
        # 1. 仅在 data 不为空时添加
        if api_info.request_form_datas:
            requests_datas = {}
            for d in json.loads(str(api_info.request_form_datas).replace("'", '"')):
                requests_datas.update({d["key"]: d["value"]})
            if len(requests_datas.items()) > 0:
                test_case_data["steps"][0]["data"] = requests_datas
        # 2. 仅在 www_form_datas 不为空时添加
        if api_info.request_www_form_datas:
            requests_datas = {}
            for d in json.loads(str(api_info.request_www_form_datas).replace("'", '"')):
                requests_datas.update({d["key"]: d["value"]})
            if len(requests_datas.items()) > 0:
                test_case_data["steps"][0]["data"] = requests_datas
        # 3.仅在 params 不为空时添加
        if api_info.request_params:
            requests_params = {}
            for d in json.loads(str(api_info.request_params).replace("'", '"')):
                requests_params.update({d["key"]: d["value"]})
            if len(requests_params.items()) > 0:
                test_case_data["steps"][0]["params"] = requests_params
        # 4.仅在 json_data 不为空时添加
        if api_info.requests_json_data:
            test_case_data["steps"][0]["json"] = api_info.requests_json_data
        # 5.如果存在 检查点，则添加
        if api_info.assert_vars:
            test_case_data["steps"][0]["assert_options"] = api_info.assert_vars
        # 6.如果存在 json提取，则添加
        if api_info.extract_vars:
            test_case_data["steps"][0]["extract_options"] = api_info.extract_vars

        # 将测试用例数据写入 YAML 文件，格式为 执行顺序_名称.yaml
        case_file_name = uuid.uuid4()
        test_case_filename = f"test_{case_file_name}.yaml"
        test_case_yaml_file = os.path.join(run_tmp_dir, test_case_filename)
        with open(test_case_yaml_file, "w", encoding="utf-8") as test_case_file:
            yaml.dump(test_case_data, test_case_file, default_flow_style=False, encoding='utf-8', allow_unicode=True)
        report_dir = app.app.config['REPORT_ROOT_DIR']
        report_file = report_dir + "/" + str(case_file_name) + ".html"
        # 执行测试
        remote_command = f"apirun --cases={run_tmp_dir} --html={report_file} -sv --capture=tee-sys "
        command_output1 = subprocess.check_output(remote_command, shell=True, universal_newlines=True,
                                                  encoding='utf-8', errors='ignore')
        # print(type(command_output1))
        # command_output_dict = json.loads(command_output1, encoding='utf-8')
        # command_output = json.dumps(command_output_dict, ensure_ascii=False, encoding='utf-8')
        # 删除一些临时文件，保留html测试报告即可
        # shutil.rmtree(run_tmp_dir)# 测试套件临时yaml文件 collection_dir
        # os.rmdir()
        return respModel.ok_resp(msg="执行结束", dic_t={"output": command_output1})
    except Exception as e:
        print(e)
        return respModel.error_resp(msg=f"执行出现错误：{e}")
