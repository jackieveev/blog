from flask import request, session, abort
from sqlalchemy.exc import IntegrityError
from blog.app import app
from blog.model import Operator
from blog.util import json_response
from .post import post_bp
from .category import category_bp

for bp in [post_bp, category_bp]:
  app.register_blueprint(bp, url_prefix='/api/%s' % bp.name)

@app.route('/api/login', methods=['POST'])
def login():
  operator = Operator.query.filter_by(username=request.json['username']).first()
  if operator:
    if operator.check_password(request.json['password']):
      data = operator.dict
      session['user'] = data
      return json_response(data)
    return abort(400, 'wrong password')
  return abort(404, 'user not exist')

@app.route('/api/logout', methods=['GET'])
def logout():
  session.pop('user')
  return 'logout successfully'

# app hook
# 在每个请求进来前：
# 1、除了login，都要求登录
# 2、...
@app.before_request
def before_request():
  if not request.path.startswith('/api/login') and not request.path.startswith('/api/logout') and 'user' not in session:
    abort(401)