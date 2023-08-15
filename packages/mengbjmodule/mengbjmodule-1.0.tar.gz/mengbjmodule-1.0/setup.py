#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description:   
@Date       :2023/08/15 14:26:48
@Author     :bangjie
@version    :1.0
'''

from setuptools import setup, find_packages

setup(
    name='mengbjmodule',
    version='1.0',
    packages=find_packages(),
    install_requires=[], # 依赖列表

    entry_points={
        'console_scripts': [
            'mycli=mengbjmodule:main',
        ]
    }
)