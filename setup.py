# -*-coding:utf-8 -*-
"""
Created on 2016-8-16

@author: Danny<manyunkai@hotmail.com>
DannyWork Project
"""

from __future__ import unicode_literals

from setuptools import setup, find_packages

setup(
    name='pywxpay',
    version='1.0.0',
    keywords=(
        'WeChat',
        'Pay'
    ),
    description='WeChat Pay development based on Python.',
    license='MIT License',
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],

    author='Danny',
    author_email='danny@dannysite.com',

    packages=find_packages(),
    platforms='any',
)
