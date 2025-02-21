* 后端运行flask程序
  * nohup python3.9 manage.py >output.log 2>&1 &
  * nohup celery -A app.my_celery worker -l INFO -P eventlet >celeryoutput.log 2>&1 &