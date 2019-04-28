from setuptools import setup, find_packages

setup(
    name='bioauth-service-facerecognition',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'flask',
        'dlib',
        'face-recognition',
        'face-recognition-models',
        'numpy',
    ],
)
