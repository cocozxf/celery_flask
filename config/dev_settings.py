# 开发环境--需要的配置
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://cocozxf:admin@192.168.27.1:3306/platfrom?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True
# 打印sql语句
SQLALCHEMY_ECHO = True
SECRET_KEY = "1234567812345678"
CASES_ROOT_DIR = r"/report_dir"
REPORT_ROOT_DIR = r"/report"