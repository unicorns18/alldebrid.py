from setuptools import setup

setup(
    name='alldebrid.py',
    version='1.0.0',
    description='Wrapper for the alldebrid API.',
    packages=['alldebrid'],
    install_requires=[
        'Requests==2.30.0'
    ],
)