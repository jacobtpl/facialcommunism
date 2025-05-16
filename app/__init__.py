from flask import Flask, session
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'facial-communism-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'

from app import routes
