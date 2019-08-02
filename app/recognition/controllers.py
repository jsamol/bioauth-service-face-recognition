from flask import Blueprint, request, json, abort, make_response

from app.recognition.exceptions import EncodingsNotFoundException
from app.recognition.models import Sample, BiometricPattern
from app.recognition.services import match_samples, get_encodings, test_samples_liveness

api_recognition = Blueprint('face', __name__)

ERROR_LIVENESS = 'Samples did not pass the liveness test.'
ERROR_ENCODINGS_NOT_FOUND = 'Could not detect faces in given samples.'


@api_recognition.route('/identification', methods=['POST'])
def identify():
    data = json.loads(request.data)

    samples = [Sample(path) for path in data.get('samples')]
    liveness_status = data.get('livenessStatus')
    patterns = (BiometricPattern(user_id, paths) for user_id, paths in data.get('patterns').items())

    if not liveness_status and not test_samples_liveness(samples):
        abort(make_response(ERROR_LIVENESS, 400))

    try:
        return match_samples(samples, patterns).to_json()
    except EncodingsNotFoundException:
        abort(make_response(ERROR_ENCODINGS_NOT_FOUND, 400))


@api_recognition.route('/encodings', methods=['POST'])
def get_encodings():
    data = json.loads(request.data)

    samples = [Sample(path) for path in data.get('samples')]
    liveness_status = data.get('livenessStatus')
    pattern_dir = data.get('patternDir')

    if not liveness_status and not test_samples_liveness(samples):
        abort(make_response(ERROR_LIVENESS, 400))

    return get_encodings(samples, pattern_dir).to_json()
