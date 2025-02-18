import app
database = app.db

class ApiSuite(database.Model):
    __tablename__ = "t_api_suite"
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    suite_name = database.Column(database.String(255), default=None)
    suite_desc = database.Column(database.String(255), default=None)
    suite_schedule = database.Column(database.Integer, default=None)
    create_time = database.Column(database.DateTime, default=None)