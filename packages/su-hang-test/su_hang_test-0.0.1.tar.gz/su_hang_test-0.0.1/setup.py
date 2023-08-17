#!/usr/bin/python3
# coding: utf-8

from setuptools import setup

setup(
    name='su_hang_test',
    version='0.0.1',
    author='Sherlock1024',
    author_email='holmes1024@outlook.com',
    url='https://baidu.com',
    description='hello world',
    packages=['helloworld'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'hello=helloworld:hello',
            'world=helloworld:world'
        ]
    }
)