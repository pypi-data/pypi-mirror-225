#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description:   
@Date       :2023/08/17 19:12:06
@Author     :bangjie
@version    :1.0
'''

import setuptools

setuptools.setup(
    name="mbjmath",
    version="0.0.1",

    packages=["mbjmath", "mbjmath.arithmetic"],

    package_data={
        "mbjmath": ["__init__.py"],
        "mbjmath.arithmetic": ["__init__.py", "basic.py"]
    },
)