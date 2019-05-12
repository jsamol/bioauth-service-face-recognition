"""
The algorithm is based on https://github.com/ee09115/spoofing_detection
"""

from typing import List

import cv2
import numpy as np
from sklearn.externals import joblib

from app.recognition.models import Sample

_liveness_classifier_path = 'app/recognition/trained_models/ycrcb_luv_extraTreesClassifier.pkl'
_haarcascade_path = 'app/recognition/trained_models/haarcascade_frontalface_default.xml'

_epsilon = 0.7


def test_liveness(samples: List[Sample]) -> bool:
    liveness_classifier = joblib.load(_liveness_classifier_path)
    face_cascade = cv2.CascadeClassifier(_haarcascade_path)

    images = (cv2.imread(sample.file_path) for sample in samples)

    sample_votes = []
    measures = []

    for index, image in enumerate(images):
        img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = _detect_faces(img_grey, face_cascade)

        measures.append([])

        for i, (x, y, width, height) in enumerate(faces):
            roi = image[y:y + height, x:x + width]

            img_ycrcb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCR_CB)
            img_luv = cv2.cvtColor(roi, cv2.COLOR_BGR2LUV)

            ycrcb_hist = _calc_hist(img_ycrcb)
            luv_hist = _calc_hist(img_luv)

            feature_vector = np.append(ycrcb_hist.ravel(), luv_hist.ravel())
            feature_vector = feature_vector.reshape(1, len(feature_vector))

            prediction = liveness_classifier.predict_proba(feature_vector)
            probability = prediction[0][1]

            measures[index].append(probability)
        sample_votes.append((np.mean(measures[index]) < _epsilon))

    return np.mean(sample_votes) > (0.5 * len(sample_votes))


def _detect_faces(img, face_cascade):
    return face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(110, 110))


def _calc_hist(img):
    histogram = [0] * 3
    for i in range(3):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])
        histr *= 255.0 / histr.max()
        histogram[i] = histr
    return np.array(histogram)
