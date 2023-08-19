# -*- coding:utf-8 -*-


from setuptools import setup, find_packages

setup(
    name='zhuque-dataloader',
    version='0.3.2',
    description='zhuque graph platform dataloader component',
    author='yanrisheng',
    author_email='yanrs@zhejianglab.com',
    #packages=find_packages(where="wg_load"),
    packages=find_packages(),
    py_modules=['loader'],
    requires=[],  # 定义依赖
    license='GPL 3.0'
)


# python setup.py sdist
# python setup.py bdist_wheel
# twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
