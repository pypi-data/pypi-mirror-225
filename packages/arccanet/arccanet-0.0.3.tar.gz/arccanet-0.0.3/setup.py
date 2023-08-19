from setuptools import setup

setup(
    name='arccanet',
    version='0.0.3',
    author='Arcca Tech Team',
    author_email='rodrigo.almeida@arcca.io',
    packages=['arccanet'],
    description='Base package for building arccanet backend',
    install_requires=[
        "Django==3.2.5",
        "djangorestframework==3.12.4",
        "djangorestframework-simplejwt==4.7.2",
    ],
)
