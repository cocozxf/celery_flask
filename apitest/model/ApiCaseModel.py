import app
database = app.db

class ApiCase(database.Model):
    __tablename__ = "t_api_case"
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    api_info_id = database.Column(database.Integer, nullable=False, comment="关联接口ID")
    collection_id = database.Column(database.Integer, nullable=False, comment="关联集合ID")
    run_order = database.Column(database.Integer, nullable=False, comment="运行顺序")
    create_time = database.Column(database.DateTime, comment="创建时间")