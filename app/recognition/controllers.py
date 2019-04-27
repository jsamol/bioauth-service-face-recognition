from flask import Blueprint

api_recognition = Blueprint('recognition', __name__)


@api_recognition.route('', methods=['POST'])
def recognize():
    return "1"
