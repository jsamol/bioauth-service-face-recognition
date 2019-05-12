from typing import Iterator, List

from app.recognition import recognition
from app.recognition.models import Sample, BiometricPattern, MatchResult


def match_samples(samples: List[Sample], patterns: Iterator[BiometricPattern]) -> MatchResult:
    matched_user_id = recognition.test_samples(samples, patterns)
    return MatchResult(matched_user_id)
