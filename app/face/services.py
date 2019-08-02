from typing import Iterator, List

from app.face import recognition
from app.face.liveness import test_liveness
from app.face.models import Sample, BiometricPattern, MatchResult, EncodingsResult


def match_samples(samples: List[Sample], patterns: Iterator[BiometricPattern]) -> MatchResult:
    matched_user_id = recognition.test_samples(samples, patterns)
    return MatchResult(matched_user_id)


def get_encodings(samples: List[Sample], pattern_dir: str) -> EncodingsResult:
    encoding_paths = recognition.get_encodings(samples, pattern_dir)
    return EncodingsResult(encoding_paths)


def test_samples_liveness(samples: List[Sample]) -> bool:
    return test_liveness(samples)
