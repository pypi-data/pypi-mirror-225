from setuptools import setup, find_packages

setup(
    name='othello-ai-python',
    version='0.1',
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
    ],
)
