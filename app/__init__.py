from flask import Flask

from app.face import api_face

API_URI = '/api/v1'

app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(api_face, url_prefix=f'{API_URI}/face')
