import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import request
from blog.ext import db
from blog.util import json_response
class Base:
  id = db.Column(db.Integer, primary_key=True)
  created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  modified_at = db.Column(db.DateTime)

  @property
  def dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}
  
  # Model.query.get(id).dict will get Attribute error when id not exist
  @classmethod
  def get(cls, id):
    res = cls.query.get(id)
    return res.dict if res else None
  
  @classmethod
  def list(cls):
    page = request.args.get('page', type=int)
    size = request.args.get('size', type=int)
    if (page is None):
      raise abort(400, 'page expect type [int]')
    if (size is None):
      raise abort(400, 'size expect type [int]')
    res = cls.query.offset((page - 1) * size).limit(size).all()
    return {
      'page': page,
      'size': size,
      'total': cls.query.count(),
      'rows': list(map(lambda e: e.dict, res))
    }
    
# 管理员
class Operator(db.Model, Base):
  username = db.Column(db.String(30), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password_hash = db.Column(db.String(120), nullable=False)

  @property
  def password(self):
    return None
  
  @password.setter
  def password(self, value):
    self.password_hash = generate_password_hash(value)
  
  @property
  def dict(self):
    res = super().dict
    del res['password_hash']
    return res

  def check_password(self, value):
    return check_password_hash(self.password_hash, value)

class Category(db.Model, Base):
  name = db.Column(db.String(100), unique=True, nullable=False)

# 博文
class Post(db.Model, Base):
  title = db.Column(db.String(100), nullable=False)
  body = db.Column(db.Text, nullable=False)
  category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
  category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))
  published_at = db.Column(db.DateTime)
  liked = db.Column(db.Integer, default=0)
  shared = db.Column(db.Integer, default=0)
  viewed = db.Column(db.Integer, default=0)

  @property
  def dict(self):
    res = super().dict
    res['category'] = self.category.name
    return res

class Comment(db.Model, Base):
  post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
  content = db.Column(db.String(140), nullable=False)