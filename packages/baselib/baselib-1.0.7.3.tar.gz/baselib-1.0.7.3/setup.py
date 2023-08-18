# -*- coding:utf-8 -*-
# from distutils.core import setup
from setuptools import find_packages
from setuptools import setup


def read_desc(filename="README.md"):
    try:
        from pathlib import Path
        desc = Path(filename).read_text(encoding="utf-8")
    except BaseException:
        with open(filename, "r") as fid:
            desc = fid.read()
    return desc


setup(
    name='baselib',
    version="1.0.7.3",
    description='base common lib for python',
    long_description=read_desc(),
    long_description_content_type="text/markdown",
    author='coreylam',
    author_email='coreylam@163.com',
    url='https://github.com/coreylam/base_common_lib',
    license='GPL',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[],
    python_requires=">=2.7",
)
