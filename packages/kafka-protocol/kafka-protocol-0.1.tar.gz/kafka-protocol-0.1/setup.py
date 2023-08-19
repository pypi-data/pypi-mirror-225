#!/usr/bin/env python
import sys
from distutils.core import setup

setup(
    name="kafka-protocol",
    version="0.1",
    author="Aivars Kalvans",
    author_email="aivars.kalvans@gmail.com",
    url="https://github.com/aivarsk/kafka-protocol",
    description="Kafka Protocol in Puthon",
    long_description=open('README.rst').read(),
    license='MIT',
    packages=["kafkaprotocol"],
    keywords=['kafka', 'apache kafka'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development',
    ],
)
