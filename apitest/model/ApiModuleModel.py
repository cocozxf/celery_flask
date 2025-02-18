import app
database = app.db
# 模块管理信息数据库类
class ApiModule(database.Model):
    __tablename__ = "t_api_module"
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    project_id = database.Column(database.Integer, nullable=False)
    module_name = database.Column(database.String(255), default=None)
    module_desc = database.Column(database.String(255), default=None)
    create_time = database.Column(database.DateTime, default=None)