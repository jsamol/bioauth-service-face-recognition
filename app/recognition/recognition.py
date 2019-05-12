import pickle
import time
from typing import Optional, Iterator, List

import face_recognition

from app.recognition.exceptions import EncodingsNotFoundException
from app.recognition.models import Sample, BiometricPattern

_EPSILON = 0.7


def test_samples(samples: List[Sample], patterns: Iterator[BiometricPattern]) -> Optional[str]:
    sample_images = (face_recognition.load_image_file(sample.file_path) for sample in samples)
    sample_biden_encodings = (face_recognition.face_encodings(image) for image in sample_images)

    sample_biden_encoding = next((encodings for encodings in sample_biden_encodings if len(encodings) > 0), [None])[0]

    if sample_biden_encoding is None:
        raise EncodingsNotFoundException()

    for pattern in patterns:
        pattern_images = [face_recognition.load_image_file(file_path) for file_path in pattern.file_paths]
        pattern_biden_encodings = [face_recognition.face_encodings(image)[0] for image in pattern_images]

        results = face_recognition.compare_faces(pattern_biden_encodings, sample_biden_encoding)
        positive_results = list(filter(None, results))

        if len(positive_results) / len(results) > _EPSILON:
            return pattern.user_id

    return None


def get_encodings(samples: List[Sample], pattern_dir: str) -> List[str]:
    sample_images = [face_recognition.load_image_file(sample.file_path) for sample in samples]
    sample_biden_encodings = [encodings[0] for encodings in
                              filter(lambda encodings: len(encodings) > 0,
                                     [face_recognition.face_encodings(image) for image in sample_images])]

    encoding_paths = []
    for index, encoding in enumerate(sample_biden_encodings):
        encoding_paths.append(f'{pattern_dir}/face_{int(time.time())}.dat')
        with open(encoding_paths[index], 'wb') as file:
            pickle.dump(encoding, file)

    return encoding_paths
