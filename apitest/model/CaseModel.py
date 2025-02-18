import app

database = app.db


class Case(database.Model):
    __tablename__ = "t_case"
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    api_case_id = database.Column(database.Integer, nullable=False, comment="关联用例ID")
    suite_id = database.Column(database.Integer, nullable=False, comment="关联任务ID")
    create_time = database.Column(database.DateTime, comment="创建时间")
