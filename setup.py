import os
from setuptools import find_packages, setup


VERSION = '0.0.1'


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as fh:
            return fh.read()
    except IOError:
        return ''


setup(
    name='python-datauri',
    version=VERSION,
    url='https://github.com/fcurella/python-datauri/',
    maintainer='Flavio Curella',
    maintainer_email='flavio.curella@gmail.com',
    description="A li’l class for data URI manipulation in Python",
    long_description=read('README.md'),
    license='MIT',
    packages=find_packages(exclude=['*.tests']),
    platforms=["any"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
