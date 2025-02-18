import app

# ORM
class User(app.db.Model):
    __tablename__ = "t_user"
    id = app.db.Column(app.db.Integer, primary_key=True, )
    username = app.db.Column(app.db.String(255), unique=True)
    password = app.db.Column(app.db.String(255), unique=True)
    create_time = app.db.Column(app.db.DateTime, unique=True)
