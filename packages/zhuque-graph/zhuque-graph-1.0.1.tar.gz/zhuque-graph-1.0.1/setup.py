# -*- coding:utf-8 -*-


from setuptools import setup, find_packages

setup(
    name='zhuque-graph',
    version='1.0.1',
    description='zhuque graph platform',
    author='1',
    author_email='yanrs@zhejianglab.com',
    packages=find_packages(where="./nn"),
    requires=[],  # 定义依赖
    license='GPL 3.0'
)


# python setup.py sdist
# python setup.py bdist_wheel
# twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
