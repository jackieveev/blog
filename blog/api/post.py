from flask import Blueprint
from flask import request
from blog.ext import db
from blog.model import Post
from flask import request
from blog.util import json_response

post_bp = Blueprint('post', __name__, url_prefix='/post')

@post_bp.route('/', strict_slashes=False, methods=['POST'])
def create_post():
  post = Post(title = '怕是打开楞alkdj', body='sadklklllsjaldjflsajdfljaskdf', category_id=1)
  db.session.add(post)
  db.session.commit()
  return json_response(post.id)

@post_bp.route('/<id>', methods=['GET'])
def get_post(id):
  return json_response(Post.get(id))

@post_bp.route('/<id>', methods=['DELETE'])
def delete_post(id):
  post = Post.query.get(id)
  if (post):
    db.session.delete(post)
    db.session.commit()
  return json_response(id)