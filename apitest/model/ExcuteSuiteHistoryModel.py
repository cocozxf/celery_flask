import app

database = app.db


class ExcuteSuiteHistory(database.Model):
    __tablename__ = "t_excute_suite"
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    suite_id = database.Column(database.Integer, comment='关联t_api_suite表主键id')
    excute_id = database.Column(database.String(255), default=None)
    excute_suite_name = database.Column(database.String(255), default=None)
    excute_status = database.Column(database.String(255), default=None)
    pass_count = database.Column(database.Integer, default=None)
    fail_count = database.Column(database.Integer, default=None)
    total_count = database.Column(database.Integer, default=None)
    create_time = database.Column(database.DateTime, default=None)
    excute_time = database.Column(database.String(255), comment='执行完成时间')
