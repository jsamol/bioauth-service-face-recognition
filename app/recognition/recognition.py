from typing import Optional, Iterator

import face_recognition

from app.recognition.models import Sample, BiometricPattern

_EPSILON = 0.7


def test_sample(sample: Sample, patterns: Iterator[BiometricPattern]) -> Optional[str]:
    sample_image = face_recognition.load_image_file(sample.file_path)
    sample_biden_encoding = face_recognition.face_encodings(sample_image)[0]

    for pattern in patterns:
        pattern_images = [face_recognition.load_image_file(file_path) for file_path in pattern.file_paths]
        pattern_biden_encodings = [face_recognition.face_encodings(image)[0] for image in pattern_images]

        results = face_recognition.compare_faces(pattern_biden_encodings, sample_biden_encoding)
        positive_results = list(filter(None, results))

        if len(positive_results) / len(results) > _EPSILON:
            return pattern.user_id

    return None
