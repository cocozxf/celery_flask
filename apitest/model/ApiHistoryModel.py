import app

database = app.db


class ApiHistoryModel(database.Model):
    __tablename__ = "t_api_history"

    id = database.Column(database.Integer, primary_key=True, comment='记录编号')
    collection_id = database.Column(database.Integer, comment='关联t_api_collection表主键id')
    collection_name = database.Column(database.String(255), comment='用例名称')
    suite_id = database.Column(database.Integer, comment='关联任务id')
    history_desc = database.Column(database.String(255), comment='运行记录简述')
    history_detail = database.Column(database.String(255), comment='运行详细记录')
    create_time = database.Column(database.DateTime, comment='创建时间')
    suite_create_time = database.Column(database.DateTime, comment='任务创建时间')
