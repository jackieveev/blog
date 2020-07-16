from flask import Flask

app = Flask(__name__)

app.config.from_pyfile('config.py')

@app.teardown_appcontext
def teardown_appcontext(exception=None):
  print('app context end')