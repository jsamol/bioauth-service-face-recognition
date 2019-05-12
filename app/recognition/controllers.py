from flask import Blueprint, request, json, jsonify, abort, Response

from app.recognition.exceptions import EncodingsNotFoundException
from app.recognition.models import Sample, BiometricPattern
from app.recognition.services import match_samples

api_recognition = Blueprint('recognition', __name__)


@api_recognition.route('', methods=['POST'])
def recognize():
    data = json.loads(request.data)

    samples = [Sample(path) for path in data.get('samples')]
    patterns = (BiometricPattern(user_id, paths) for user_id, paths in data.get('patterns').items())

    try:
        return jsonify(match_samples(samples, patterns).serizalize())
    except EncodingsNotFoundException as e:
        return Response(response='Could not detect faces in given samples.', status=400)
