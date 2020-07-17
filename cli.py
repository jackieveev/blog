import click
from blog.app import app
from blog.model import Operator
from blog.ext import db

@app.cli.command('create-operator')
@click.option('--name')
@click.option('--password')
@click.option('--email')
def create_operator(name, password, email):
  operator = Operator(username = name, email = email, password=password)
  db.session.add(operator)
  db.session.commit()
  print('create operator [%s] successfully!' % name)