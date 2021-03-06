from flask import Flask
from redis import StrictRedis
import config
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = config.SECRET_KEY
app.config['DEBUG'] = 'true'

red = StrictRedis()

from gethem import views
