from flask import Blueprint
from flask import Request
from blog.app import app
from blog.ext import db
from blog.model import Operator

operator_bp = Blueprint('operator', __name__, url_prefix='/operator')

@operator_bp.route('/', strict_slashes=False, methods=['POST'])
def create_post():
  l = len(Operator.query.all()) + 1
  operator = Operator(username = 'admin%s'%l, email = 'jackieveev@gmail.com%s'%l, password='123456')
  db.session.add(operator)
  db.session.commit()
  return 'create'