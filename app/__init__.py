from flask import Flask

from app.recognition import api_recognition

API_URI = '/api/v1'

app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(api_recognition, url_prefix=f'{API_URI}/face')
