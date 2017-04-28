from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView

from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
from os import makedirs, listdir

from flask_basicauth import BasicAuth

from flask_admin import Admin


# create application
app = Flask(__name__)
app.config.from_pyfile('config.py')

# create database
db = SQLAlchemy(app)

# enable basic authentication
basic_auth = BasicAuth(app)


# create models
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


# add a link to the admin panel to the index page
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


# build the database
db.create_all()

# create admin
admin = Admin(app, name='discordbot', template_mode='bootstrap3')

# user database view
admin.add_view(ModelView(User, db.session))

# add static files view
path = op.join(op.dirname(__file__), 'static')
if not op.exists(path):
    makedirs(path)
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))


def list_files():
    """List files that have been uploaded from the admin UI"""
    return listdir(path)


def get_file(filename):
    """Fetch a file that has been uploaded from the admin UI"""
    try:
        return open(op.join(path, op.basename(filename)), 'rb')
    except:
        return 'File not found'
