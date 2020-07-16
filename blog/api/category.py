from flask import Blueprint
from flask import request
from blog.ext import db
from blog.model import Category
from blog.util import json_response

category_bp = Blueprint('category', __name__, url_prefix='/category')

@category_bp.route('/', strict_slashes=False, methods=['POST'])
def create_post():
  category = Category(name=request.json['name'])
  db.session.add(category)
  db.session.commit()
  return json_response(category.id)

@category_bp.route('/list', methods=['GET'])
def get_category_list():
  return 'list'

@category_bp.route('/<id>', methods=['DELETE'])
def delete_category(id):
  category = Category.query.get(id)
  if (category):
    db.session.delete(category)
    db.session.commit()
  return json_response(id)