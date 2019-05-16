from flask import Blueprint, request, json, abort, make_response

from app.recognition.exceptions import EncodingsNotFoundException
from app.recognition.models import Sample, BiometricPattern
from app.recognition.services import match_samples, get_encodings, test_samples_liveness

api_recognition = Blueprint('recognition', __name__)

_error_liveness = 'Samples did not pass the liveness test.'
_error_encodings_not_found = 'Could not detect faces in given samples.'


@api_recognition.route('', methods=['POST'])
def recognize():
    data = json.loads(request.data)

    samples = [Sample(path) for path in data.get('samples')]
    liveness_status = data.get('livenessStatus')
    patterns = (BiometricPattern(user_id, paths) for user_id, paths in data.get('patterns').items())

    if not liveness_status and not test_samples_liveness(samples):
        abort(make_response(_error_liveness, 401))

    try:
        return match_samples(samples, patterns).to_json()
    except EncodingsNotFoundException:
        abort(make_response(_error_encodings_not_found, 400))


@api_recognition.route('/encodings', methods=['POST'])
def encodings():
    data = json.loads(request.data)

    samples = [Sample(path) for path in data.get('samples')]
    liveness_status = data.get('livenessStatus')
    pattern_dir = data.get('patternDir')

    if not liveness_status and not test_samples_liveness(samples):
        abort(make_response(_error_liveness, 401))

    return get_encodings(samples, pattern_dir).to_json()
