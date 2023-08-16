#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

# python.exe setup.py sdist bdist_wheel
# twine upload dist/*


def get_install_requires():
    reqs = [
        'pillow>=9.5.0',
        'httpx>=0.24.0',
        'toml>=0.10.2',
        'nonebot2>=2.0.0',
        'nonebot_adapter_onebot>=2.2.3',
        'nonebot_plugin_apscheduler>=0.2.0'
    ]
    return reqs


setup(name='nonebot_plugin_kanonbot',
      version='0.0.1-beta5',
      description='nonebot plugin kanonbot',
      author='SuperGuGuGu',
      author_email='13680478000@163.com',
      url='https://github.com/SuperGuGuGu/nonebot_plugin_kanonbot',
      packages=find_packages(),
      python_requires=">=3.8",
      install_requires=get_install_requires(),
      # package_data={'': ['*.csv', '*.txt', '.toml']},
      include_package_data=True
      )
