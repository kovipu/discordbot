from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

basic_auth = BasicAuth(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    usernum = db.Column(db.Integer, unique=True)
    permissions = db.Column(db.Integer)

    def __init__(self, name, usernum, permissions=0):
        self.name = name
        self.usernum = usernum
        self.permissions = permissions

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<User {}>'.format(self.name)

admin = Admin(app, name='discordbot', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))

db.create_all()

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

def run():
    app.run()
