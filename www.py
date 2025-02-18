from app import app
from core.BaseController import route_index
from login.api import LoginController
from sysmanage.api import UserController
from apitest.api import ApiInfoController
from apitest.api import ApiProjectContoller
from apitest.api import ApiModuleController
from apitest.api import ApiCollectionController
from apitest.api import ApiCaseController
from apitest.api import ApiHistoryController
from apitest.api import CaseController
from apitest.api import ApiSuiteController

# 注册模块 WEB API 接口路由信息
app.register_blueprint(route_index, url_prefix="/")

app.register_blueprint(LoginController.module_route)

app.register_blueprint(UserController.module_route)

app.register_blueprint(ApiInfoController.module_route)

app.register_blueprint(ApiProjectContoller.module_route)
app.register_blueprint(ApiModuleController.module_route)
app.register_blueprint(ApiCollectionController.module_route)

app.register_blueprint(ApiCaseController.module_route)

app.register_blueprint(ApiHistoryController.module_route)
app.register_blueprint(CaseController.module_route)

app.register_blueprint(ApiSuiteController.module_route)
