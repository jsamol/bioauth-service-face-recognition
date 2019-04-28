from typing import Optional, Iterator

from app.recognition.models import Sample, BiometricPattern


def test_sample(sample: Sample, patterns: Iterator[BiometricPattern]) -> Optional[str]:
    return None
