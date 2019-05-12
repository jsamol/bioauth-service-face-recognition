from typing import Iterator, List

from app.recognition import recognition
from app.recognition.models import Sample, BiometricPattern, MatchResult, EncodingsResult


def match_samples(samples: List[Sample], patterns: Iterator[BiometricPattern]) -> MatchResult:
    matched_user_id = recognition.test_samples(samples, patterns)
    return MatchResult(matched_user_id)


def get_encodings(samples: List[Sample], pattern_dir: str) -> EncodingsResult:
    encoding_paths = recognition.get_encodings(samples, pattern_dir)
    return EncodingsResult(encoding_paths)
