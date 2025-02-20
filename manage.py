from app import app
# from flask_script import Server
import www



def mian():
    app.run(host="0.0.0.0", port=5003, threaded=True)


if __name__ == '__main__':
    try:
        import sys

        sys.exit(mian())
    except Exception as e:
        import traceback

        traceback.print_exc()
