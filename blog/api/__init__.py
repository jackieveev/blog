from flask import request, session, abort
from blog.app import app
from blog.model import Operator
from blog.util import json_response
from .post import post_bp
from .category import category_bp

for bp in [post_bp, category_bp]:
  bp.url_prefix = '/api%s' % bp.url_prefix
  app.register_blueprint(bp, url_prefix='/api/%s' % bp.name)

@app.route('/api/login', methods=['POST'])
def login():
  # session['user'] = {'name': 'admin', 'role': 0}
  operator = Operator.query.filter_by(username=request.json['username']).first()
  if operator:
    if operator.check_password(request.json['password']):
      return 'success'
    return 'incorrect password'
  return 'user not exist'

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
  if (not request.path.startswith('/login') and not request.path.startswith('/logout') and 'user' not in session):
    abort(401)
  print('gogogo')

# app hook
# 所有未知错误都返回
# @app.errorhandler(Exception)
# def app_error(e):
#   print(e)
#   return 'Internal Server Error'