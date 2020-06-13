from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import yaml
from src.utils.constants import YAMLPATH
app = Flask(__name__)

# mysql configuration
stream = open(YAMLPATH, 'r')
data = yaml.load(stream)
db = data['db']
username = data['username']
password = data['password']

db_url = 'mysql+pymysql://{user}:{pw}@localhost/{db}'.format(user=username, pw=password,
                                                     db=db)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)