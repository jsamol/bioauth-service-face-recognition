import random

from flask import Blueprint, request, json

from app.recognition.models import Sample, BiometricPattern
from app.recognition.services import match_sample

api_recognition = Blueprint('recognition', __name__)


@api_recognition.route('', methods=['POST'])
def recognize():
    data = json.loads(request.data)

    sample = random.choice([Sample(path) for path in data.get('samples')])
    patterns = (BiometricPattern(user_id, paths) for user_id, paths in data.get('patterns').items())

    return match_sample(sample, patterns)
