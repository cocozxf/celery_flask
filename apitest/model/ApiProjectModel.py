import app
database = app.db
# 项目管理信息数据库类
class ApiProject(database.Model):
    __tablename__ = "t_api_project"
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    project_name = database.Column(database.String(255))
    project_desc = database.Column(database.String(255))
    create_time = database.Column(database.DateTime)