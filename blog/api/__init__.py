from blog.app import app
from .post import post_bp
from .category import category_bp
from flask import request, session

for bp in [post_bp, category_bp]:
  bp.url_prefix = '/api%s' % bp.url_prefix
  app.register_blueprint(bp)

@app.route('/api/login', methods=['POST'])
def login():
  session['user'] = {'name': 'admin', 'role': 0}
  return 'login'

@app.route('/api/logout', methods=['GET'])
def logout():
  session.pop('user')
  return 'logout'

# app hook
# 在每个请求进来前：
# 1、除了login，都要求登录
# 2、...
@app.before_request
def before_request():
  pass
  # if (not request.path.startswith('/login') and not request.path.startswith('/logout') and 'user' not in session):
  #   return 'login required'
  # if ('user' in session):
  #   print(session['user'])

# app hook
# 所有未知错误都返回
# @app.errorhandler(Exception)
# def app_error(e):
#   print(e)
#   return 'Internal Server Error'