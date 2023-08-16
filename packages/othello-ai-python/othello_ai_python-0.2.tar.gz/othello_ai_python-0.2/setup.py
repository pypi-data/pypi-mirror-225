from setuptools import setup, find_packages

setup(
    name='othello_ai_python',
    version='0.2',
    packages=find_packages(),
    install_packages=[
        'math',
        'pygame',
        'numpy',
        'keras>=3.0',
        'os',
        'random',
        'json',
        'sys',
        'io',
        'time',
        'concurrent'
    ],
)
