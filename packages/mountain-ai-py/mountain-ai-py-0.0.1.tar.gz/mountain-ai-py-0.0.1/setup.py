#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='mountain-ai-py',
      python_requires='>=3.6',
      version='0.0.1',
      description='a python client for mountain-ai',
      author='ShenBing',
      author_email='shenbinglife@163.com',
      url='',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      install_requires = [
          "requests"
      ],
      classifiers=(
          "Programming Language :: Python :: 3",
          'Programming Language :: Python :: 3.7',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
      )
  )