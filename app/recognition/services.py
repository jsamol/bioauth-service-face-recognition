from typing import Iterator

from app.recognition import recognition
from app.recognition.models import Sample, BiometricPattern, MatchResult


def match_sample(sample: Sample, patterns: Iterator[BiometricPattern]) -> MatchResult:
    matched_user_id = recognition.test_sample(sample, patterns)
    return MatchResult(matched_user_id)
