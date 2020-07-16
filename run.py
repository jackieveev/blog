from blog import app
from blog.ext import db

db.create_all()
app.run(debug=True)