from flask import Blueprint
from flask import request, abort
from blog.ext import db
from blog.model import Post
from blog.util import json_response

post_bp = Blueprint('post', __name__)

@post_bp.route('/', strict_slashes=False, methods=['POST'])
def create_post():
  try:
    post = Post(title=request.json['title'],
                body=request.json['body'],
                category_id=request.json['category_id'])
  except KeyError as e:
    abort(400, 'missing params: %s' % e)
  else:
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