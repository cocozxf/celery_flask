# 镜像 ：  https://pypi.tuna.tsinghua.edu.cn/simple
# 准备的包： flask flask_sqlalchemy flask_script pymysql flask_cors

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from celery import Celery
import celeryconfig
import time


def register_celery(celery, app):
    class ContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask


class Application(Flask):
    def __init__(self, import_name):
        super(Application, self).__init__(import_name)  # 父类启动
        self.config.from_pyfile('config/dev_settings.py')  # 加载配置
        db.init_app(self)
        register_celery(my_celery, app=self)
        # jwt.init_app(self)


def make_celery(app_name):
    celery = Celery(app_name,
                    broker=celeryconfig.broker_url,
                    backend=celeryconfig.result_backend)
    celery.config_from_object(celeryconfig)
    return celery


my_celery = make_celery(__name__)
db = SQLAlchemy()
app = Application(__name__)
CORS(app, resources=r'/*',expose_headers=['Set-Cookie'])


@my_celery.task()
def add2(x, y):
    time.sleep(5)
    return x + y


import json, os, subprocess, uuid, yaml
from apitest.model.ApiCollectionModel import ApiCollection
from apitest.model.ApiHistoryModel import ApiHistoryModel
from apitest.model.ApiInfoModel import ApiInfo
from core.resp_model import respModel
from apitest.model.ApiSuiteModel import ApiSuite
from datetime import datetime
from apitest.model.CaseModel import Case
from apitest.model.ApiCaseModel import ApiCase


@my_celery.task()
def excuteTset(cases_dir, suite_id, suite_create_time):
    start_time = time.time()
    session = db.session
    # 1.查询指定ID的任务数据
    suite = session.query(ApiSuite).filter_by(id=suite_id).first()
    # 2.获取任务关联的用例数据
    collection_cases = session.query(Case).filter_by(suite_id=suite.id).all()
    total_count = len(collection_cases)
    for collection_case in collection_cases:
        # 1. 查询指定ID的集合数据
        collection = session.query(ApiCollection).filter_by(id=collection_case.api_case_id).first()
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
            test_case_data["steps"][index]["desc"] = api_info.api_name,
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

        report_dir = app.config['REPORT_ROOT_DIR']
        report_file = report_dir + "/" + str(case_file_name) + ".html"
        # 1.执行测试
        remote_command = f"apirun --cases={collection_dir} --html={report_file} -sv --capture=tee-sys "
        command_output = subprocess.check_output(remote_command, shell=True, universal_newlines=True)
        history_desc = command_output.split("\n")[-2].replace("=", "")
        # TODO 这里可以根据 command_output 命令输出的内容去做一些统计
        # # 2. 删除一些临时文件，保留html测试报告即可
        # shutil.rmtree(collection_dir)  # 测试套件临时yaml文件 collection_dir
        # shutil.rmtree(report_file)  # 测试工具执行后的测试结果数据
        report = ApiHistoryModel(id=0, collection_id=collection.id, collection_name=collection.collection_name,
                                 suite_id=suite_id, history_desc=history_desc,
                                 history_detail=report_dir + "/" + str(case_file_name),
                                 create_time=datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S'),
                                 suite_create_time=suite_create_time)
        session.add(report)
        session.commit()
    end_time = time.time()
    excute_time = float(end_time - start_time)
    return "{}s".format(str(round(excute_time, 2))), total_count
