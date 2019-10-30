from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES, AUDIO

app = Flask(__name__)
images = UploadSet('images', IMAGES)
audios = UploadSet('audios', AUDIO)
app.config['SECRET_KEY'] = '68307df7029781e7602f3c4e2522b875'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOADED_IMAGES_DEST'] = os.path.join(app.root_path, 'static', 'images')
app.config['UPLOADED_AUDIOS_DEST'] = os.path.join(app.root_path, 'static', 'audio')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
configure_uploads(app, (images, audios))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from musicapp import routes